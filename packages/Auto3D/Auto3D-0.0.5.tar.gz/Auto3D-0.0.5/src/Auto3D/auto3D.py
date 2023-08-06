#!/usr/bin/env python
"""
Generating 3-dimensional structures from SMILES based on user's demands.
"""

import argparse
import os
import shutil
import sys
import time
import torch
import math
import psutil, tarfile
import glob
import pandas as pd
import multiprocessing as mp
from .isomer_engine import rd_isomer, tautomer_engine
from .isomer_engine import oe_isomer
from .ranking import ranking
from .utils import housekeeping, check_input
from .utils import hash_taut_smi,  my_name_space
from .batch_opt.batchopt import optimizing
from send2trash import send2trash
try:
    mp.set_start_method('spawn')
except:
    pass


def create_chunk_meta_names(path, dir):
    """Output name is based on chunk input path and directory
    path: chunck input smi path
    dir: chunck job folder
    """
    dct = {}
    output_name = os.path.basename(path).split('.')[0].strip() + '_3d.sdf'
    output = os.path.join(dir, output_name)
    optimized_og = output.split('.')[0] + '0.sdf'

    output_taut = os.path.join(dir, 'smi_taut.smi')
    smiles_enumerated = os.path.join(dir, 'smiles_enumerated.smi')
    smiles_reduced = smiles_enumerated.split('.')[0] + '_reduced.smi'
    smiles_hashed = os.path.join(dir, 'smiles_enumerated_hashed.smi')
    enumerated_sdf = os.path.join(dir, 'smiles_enumerated.sdf')
    sorted_sdf = os.path.join(dir, 'enumerated_sorted.sdf')
    housekeeping_folder = os.path.join(dir, 'verbose')
    # dct["output_name"] = output_name
    dct["output"] = output
    dct["optimized_og"] = optimized_og
    dct["output_taut"] = output_taut
    dct["smiles_enumerated"] = smiles_enumerated
    dct["smiles_reduced"] = smiles_reduced
    dct["smiles_hashed"] = smiles_hashed
    dct["enumerated_sdf"] = enumerated_sdf
    dct["sorted_sdf"] = sorted_sdf
    dct["housekeeping_folder"] = housekeeping_folder
    dct["path"] = path
    dct["dir"] = dir
    return dct

def isomer_wraper(chunk_info, args, queue):
    """
    chunk_info: (path, dir) tuple for the chunk
    args: auto3D arguments
    queue: mp.queue
    """
    for i, path_dir in enumerate(chunk_info):
        print(f"\n\nIsomer generation for job{i+1}")
        path, dir = path_dir
        meta = create_chunk_meta_names(path, dir)

        # Tautomer enumeratioin
        if args.enumerate_tautomer:
            output_taut = meta["output_taut"]
            taut_mode = args.taut_engine
            print("Enumerating tautomers for the input...", end='')
            taut_engine = tautomer_engine(taut_mode, path, output_taut)
            taut_engine.run()
            hash_taut_smi(output_taut, output_taut)
            path = output_taut
            print(f"Tautomers are saved in {output_taut}")

        smiles_enumerated = meta["smiles_enumerated"]
        smiles_reduced = meta["smiles_reduced"]
        smiles_hashed = meta["smiles_hashed"]
        enumerated_sdf = meta["enumerated_sdf"]
        max_confs = args.max_confs
        duplicate_threshold = args.threshold
        mpi_np = args.mpi_np
        cis_trans = args.cis_trans
        isomer_program = args.isomer_engine
        # Isomer enumeration step
        if isomer_program == 'omega':
            mode_oe = args.mode_oe
            oe_isomer(mode_oe, path, smiles_enumerated, smiles_reduced, smiles_hashed,
                    enumerated_sdf, max_confs, duplicate_threshold, cis_trans)
        elif isomer_program == 'rdkit':
            engine = rd_isomer(path, smiles_enumerated, smiles_reduced, smiles_hashed, 
                            enumerated_sdf, dir, max_confs, duplicate_threshold, mpi_np, cis_trans)
            engine.run()
        else: 
            raise ValueError('The isomer enumeration engine must be "omega" or "rdkit", '
                            f'but {args.isomer_engine} was parsed. '
                            'You can set the parameter by appending the following:'
                            '--isomer_engine=rdkit')

        queue.put((enumerated_sdf, path, dir))
    queue.put("Done")


def optim_rank_wrapper(args, queue):
    job = 1
    while True:
        sdf_path_dir = queue.get()
        if sdf_path_dir == "Done":
            break
        print(f"\n\nOptimizing on job{job}")
        enumerated_sdf, path, dir = sdf_path_dir
        meta = create_chunk_meta_names(path, dir)

        # Optimizing step
        opt_steps = args.opt_steps
        opt_tol = args.convergence_threshold
        config = {"opt_steps": opt_steps, "opttol": opt_tol}
        optimized_og = meta["optimized_og"]
        optimizing_engine = args.optimizing_engine
        if args.use_gpu:
            idx = args.gpu_idx
            device = torch.device(f"cuda:{idx}")
        else:
            device = torch.device("cpu")
        optimizer = optimizing(enumerated_sdf, optimized_og,
                               optimizing_engine, device, config)
        optimizer.run()

        # Ranking step
        output = meta["output"]
        duplicate_threshold = args.threshold
        k = args.k
        window = args.window
        rank_engine = ranking(optimized_og,
                              output, duplicate_threshold, k=k, window=window)
        rank_engine.run()

        # Housekeeping
        housekeeping_folder = meta["housekeeping_folder"]
        os.mkdir(housekeeping_folder)
        housekeeping(dir, housekeeping_folder, output)
        #Conpress verbose folder
        housekeeping_folder_gz = housekeeping_folder + ".tar.gz"
        with tarfile.open(housekeeping_folder_gz, "w:gz") as tar:
            tar.add(housekeeping_folder, arcname=os.path.basename(housekeeping_folder))
        shutil.rmtree(housekeeping_folder)
        if not args.verbose:
            send2trash(housekeeping_folder_gz)
        job += 1


def options(path, k=False, window=False, verbose=False, job_name="",
    enumerate_tautomer=False, tauto_engine="rdkit",
    isomer_engine="rdkit", cis_trans=True, mode_oe="classic", mpi_np=4, max_confs=1000,
    use_gpu=True, gpu_idx=0, optimizing_engine="AIMNET",
    opt_steps=10000, convergence_threshold=0.003, threshold=0.3):
    """Arguments for Auto3D main program
    path: A input.smi containing SMILES and IDs. Examples are listed in the input folder
    k: Outputs the top-k structures for each SMILES.
    window: Outputs the structures whose energies are within window (kcal/mol) from the lowest energy
    verbose: When True, save all meta data while running.
    job_name: A folder name to save all meta data.
    
    enumerate_tautomer: When True, enumerate tautomers for the input
    taut_engine: Programs to enumerate tautomers, either 'rdkit' or 'oechem
    isomer_engine: The program for generating 3D isomers for each SMILES. This parameter is either rdkit or omega.
    cis_trans: When True, cis/trans and r/s isomers are enumerated.
    mode_oe: "The mode that omega program will take. "It can be either 'classic', 'macrocycle' ""'rocs', 'pose' or 'dense'. "
                            "By default, the 'classic' mode is used. "
                            "For detailed information about each mode, see "
                            "https://docs.eyesopen.com/applications/omega/omega/omega_overview.html"
    mpi_np: Number of CPU cores for the isomer generation step.
    max_confs: Maximum number of isomers for each SMILES
    """
    d = {}
    args = my_name_space(d)
    args['path'] = path
    args['k'] = k
    args['window'] = window
    args['verbose'] = verbose
    args['job_name'] = job_name
    args["enumerate_tautomer"] = enumerate_tautomer
    args["tauto_engine"] = tauto_engine
    args["isomer_engine"] = isomer_engine
    args["cis_trans"] = cis_trans
    args["mode_oe"] = mode_oe
    args["mpi_np"] = mpi_np
    args["max_confs"] = max_confs
    args["use_gpu"] = use_gpu
    args["gpu_idx"] = gpu_idx
    args["optimizing_engine"] = optimizing_engine
    args["opt_steps"] = opt_steps
    args["convergence_threshold"] = convergence_threshold
    args["threshold"] = threshold
    return args

def main(args:dict):
    """Take the arguments from options and run Auto3D"""


    chunk_line = mp.Manager().Queue(4)   #A queue managing two wrappers


    start = time.time()
    job_name = time.strftime('%Y%m%d-%H%M%S')

    path = args.path
    k = args.k
    window = args.window
    if (not k) and (not window):
        sys.exit("Either k or window needs to be specified. "
                "Usually, setting '--k=1' satisfies most needs.")
    if args.job_name == "":
        args.job_name = job_name
    job_name = args.job_name

    basename = os.path.basename(path)
    # initialiazation
    dir = os.path.dirname(os.path.abspath(path))
    job_name = job_name + "_" + basename.split('.')[0].strip()
    job_name = os.path.join(dir, job_name)
    os.mkdir(job_name)
    check_input(args)


    ## Devide jobs based on memory
    smiles_per_G = 42  #Allow 40 SMILES per GB memory
    if args.use_gpu:
        gpu_idx = int(args.gpu_idx)
        t = int(math.ceil(torch.cuda.get_device_properties(gpu_idx).total_memory/(1024**3)))
    else:
        t = psutil.virtual_memory().total/(1024**3)
    chunk_size = t * smiles_per_G

    #Get indexes for each chunk
    df = pd.read_csv(path, sep=" ", header=None)
    data_size = len(df)
    num_chunks = int(data_size // chunk_size + 1)
    print(f"There are {len(df)} SMILES, available memory is {t} GB.")
    print(f"The task will be divided into {num_chunks} jobs.")
    chunk_idxes = [[] for _ in range(num_chunks)]
    for i in range(num_chunks):
        idx = i
        while idx < data_size:
            chunk_idxes[i].append(idx)
            idx += num_chunks

    #Save each chunk as smi
    chunk_info = []
    basename = os.path.basename(path).split(".")[0].strip()
    for i in range(num_chunks):
        dir = os.path.join(job_name, f"job{i+1}")
        os.mkdir(dir)
        new_basename = basename + "_" + str(i+1) + ".smi"
        new_name = os.path.join(dir, new_basename)
        df_i = df.iloc[chunk_idxes[i], :]
        df_i.to_csv(new_name, header=None, index=None, sep=" ")
        path = new_name

        print(f"Job{i+1}, number of inputs: {len(df_i)}")
        chunk_info.append((path, dir))

    # if __name__ == "__main__":
    p1 = mp.Process(target=isomer_wraper, args=(chunk_info, args, chunk_line))
    p2 = mp.Process(target=optim_rank_wrapper, args=(args, chunk_line,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    #Combine jobs into a single sdf
    data = []
    paths = os.path.join(job_name, "job*/*.sdf")
    files = glob.glob(paths)
    for file in files:
        with open(file, "r") as f:
            data_i = f.readlines()
        data += data_i
    combined_basename = basename + "_out.sdf"
    path_combined = os.path.join(job_name, combined_basename)
    with open(path_combined, "w+") as f:
        for line in data:
            f.write(line)

    # Program ends
    end = time.time()
    print("Energy unit: Hartree if implicit.")
    print(f'Program running time: {end - start} seconds')
    return path_combined


if __name__ == "__main__":
    chunk_line = mp.Manager().Queue(4)   #A queue managing two wrappers
    print("""
        _              _             _____   ____  
       / \     _   _  | |_    ___   |___ /  |  _ \ 
      / _ \   | | | | | __|  / _ \    |_ \  | | | |
     / ___ \  | |_| | | |_  | (_) |  ___) | | |_| |
    /_/   \_\  \__,_|  \__|  \___/  |____/  |____/ 
        // Automatically generating the lowest-energy 3D structure                                       
    """)

    start = time.time()
    job_name = time.strftime('%Y%m%d-%H%M%S')

    parser = argparse.ArgumentParser(prog='auto3D',
                        description=('This program takes in a SMILES(s)'
                                    ' and returns the optimal 3D structure(s)'),
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('path', type=str,
                        help=('A input.smi containing SMILES and IDs. '
                            'Examples are listed in the input folder'))
    parser.add_argument('--k', type=int, default=False,
                        help='Outputs the top-k structures for each SMILES.')
    parser.add_argument('--window', type=float, default=False,
                        help=('Outputs the structures whose energies are within '
                            'window (kcal/mol) from the lowest energy'))
    parser.add_argument('--verbose', default=True, type=lambda x: (str(x).lower() == 'true'),
                        help='When True, save all meta data while running.')
    parser.add_argument('--job_name', type=str, default=job_name,
                        help="A folder name to save all meta data.")

    # parameters for isomer enumeration step
    parser.add_argument('--enumerate_tautomer', default=False, type=lambda x: (str(x).lower() == 'true'),
                        help="When True, enumerate tautomers for the input")
    parser.add_argument('--taut_engine', type=str, default='rdkit',
                        help="Programs to enumerate tautomers, either 'rdkit' or 'oechem'")
    parser.add_argument('--isomer_engine', type=str, default='rdkit',
                        help=('The program for generating 3D isomers for each '
                            'SMILES. This parameter is either '
                            'rdkit or omega. rdkit is free for everyone, '
                            'while omega reuqires a license.'))
    parser.add_argument('--cis_trans', default=True, type=lambda x: (str(x).lower() == 'true'),
                        help='When True, cis/trans and r/s isomers are enumerated.')
    parser.add_argument('--mode_oe', type=str, default='classic',
                        help=("The mode that omega program will take. "
                            "It can be either 'classic', 'macrocycle' "
                            "'rocs', 'pose' or 'dense'. "
                            "By default, the 'classic' mode is used. "
                            "For detailed information about each mode, see "
                            "https://docs.eyesopen.com/applications/omega/omega/omega_overview.html"))
    parser.add_argument('--mpi_np', type=int, default=4,
                        help="Number of CPU cores for the isomer generation step.")
    parser.add_argument('--max_confs', type=int, default=1000,
                        help="Maximum number of isomers for each SMILES")
    parser.add_argument('--use_gpu', default=True, type=lambda x: (str(x).lower() == 'true'),
                        help="If True, the program will use GPU.")
    parser.add_argument('--gpu_idx', default=0, type=int, 
                        help="GPU index. It only works when --use_gpu=True")
    parser.add_argument('--optimizing_engine', type=str, default='AIMNET',
                        help=("Choose either 'ANI2x', 'ANI2xt', or 'AIMNET' for energy "
                            "calculation and geometry optimization."))
    parser.add_argument('--opt_steps', type=int, default=10000,
                        help="Maximum optimization steps for each structure.")
    parser.add_argument('--convergence_threshold', type=float, default=0.003,
                        help="Optimization is considered as converged if maximum force is below this threshold.")
    parser.add_argument('--threshold', type=float, default=0.3,
                        help=("If the RMSD between two conformers are within threhold, "
                            "they are considered as duplicates. One of them will be removed."))

    args = parser.parse_args()
    path = args.path
    k = args.k
    window = args.window
    if (not k) and (not window):
        sys.exit("Either k or window needs to be specified. "
                "Usually, setting '--k=1' satisfies most needs.")
    job_name = args.job_name



    basename = os.path.basename(path)
    # initialiazation
    dir = os.path.dirname(os.path.abspath(path))
    job_name = job_name + "_" + basename.split('.')[0].strip()
    job_name = os.path.join(dir, job_name)
    os.mkdir(job_name)
    check_input(args)


    ## Devide jobs based on memory
    smiles_per_G = 42  #Allow 40 SMILES per GB memory
    if args.use_gpu:
        gpu_idx = int(args.gpu_idx)
        t = int(math.ceil(torch.cuda.get_device_properties(gpu_idx).total_memory/(1024**3)))
    else:
        t = psutil.virtual_memory().total/(1024**3)
    chunk_size = t * smiles_per_G

    #Get indexes for each chunk
    df = pd.read_csv(path, sep=" ", header=None)
    data_size = len(df)
    num_chunks = int(data_size // chunk_size + 1)
    print(f"There are {len(df)} SMILES, available memory is {t} GB.")
    print(f"The task will be divided into {num_chunks} jobs.")
    chunk_idxes = [[] for _ in range(num_chunks)]
    for i in range(num_chunks):
        idx = i
        while idx < data_size:
            chunk_idxes[i].append(idx)
            idx += num_chunks

    #Save each chunk as smi
    chunk_info = []
    basename = os.path.basename(path).split(".")[0].strip()
    for i in range(num_chunks):
        dir = os.path.join(job_name, f"job{i+1}")
        os.mkdir(dir)
        new_basename = basename + "_" + str(i+1) + ".smi"
        new_name = os.path.join(dir, new_basename)
        df_i = df.iloc[chunk_idxes[i], :]
        df_i.to_csv(new_name, header=None, index=None, sep=" ")
        path = new_name

        print(f"Job{i+1}, number of inputs: {len(df_i)}")
        chunk_info.append((path, dir))

    p1 = mp.Process(target=isomer_wraper, args=(chunk_info, args, chunk_line))
    p2 = mp.Process(target=optim_rank_wrapper, args=(args, chunk_line,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    #Combine jobs into a single sdf
    data = []
    paths = os.path.join(job_name, "job*/*.sdf")
    files = glob.glob(paths)
    for file in files:
        with open(file, "r") as f:
            data_i = f.readlines()
        data += data_i
    combined_basename = basename + "_out.sdf"
    path_combined = os.path.join(job_name, combined_basename)
    with open(path_combined, "w+") as f:
        for line in data:
            f.write(line)

    # Program ends
    end = time.time()
    print("Energy unit: Hartree if implicit.")
    print(f'Program running time: {end - start} seconds')
