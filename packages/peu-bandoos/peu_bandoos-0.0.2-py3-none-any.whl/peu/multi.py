"""
Utility module to run experiments in parallel using multiprocessing
"""
from multiprocessing import Pool
import os
from tqdm import tqdm


def tracked_multiproc_unordered(unit, tasks, processes=None, do_extend=False):
    """Run unit over task in multiprocessing Pool.
    Runs unit in parallel over `processes` (default os.cpu_count())
    no ordering guarantees if processes>1.
    Reports progress of the mapping via tqdm.
    """
    results = []
    with Pool(processes=(processes or os.cpu_count())) as pool:
        for result in tqdm(pool.imap_unordered(unit, tasks), total=len(tasks)):
            if do_extend:
                results.extend(result)
            else:
                results.append(result)
        pool.close()  # no more work
        pool.join()
    return results
