""" Populaton utilities
"""
import requests
import urllib.parse
import hashlib
import warnings
from pathlib import Path
import contextlib
import joblib

def hash_stim(stim, blocksize=65536):
    """ Hash a pliers stimulus """
    if isinstance(stim, Path):
        stim = stim.as_posix()
    if isinstance(stim, str):
        from pliers.stimuli import load_stims
        from os.path import isfile
        assert isfile(stim)
        stim = load_stims(stim)

    hasher = hashlib.sha1()

    if hasattr(stim, "data"):
        return hash_data(stim.data)
    else:
        filename = stim.history.source_file \
                    if stim.history \
                    else stim.filename
        with open(filename, 'rb') as afile:
            buf = afile.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(blocksize)

    return hasher.hexdigest()


def hash_data(data):
    """" Hashes data or string """
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif hasattr(data, 'to_string'):
        data = data.to_string().encode('utf-8')
    hasher = hashlib.sha1()
    hasher.update(data)

    return hasher.hexdigest()


@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
    """Context manager to patch joblib to report into tqdm progress
    bar given as argument"""

    def tqdm_print_progress(self):
        if self.n_completed_tasks > tqdm_object.n:
            n_completed = self.n_completed_tasks - tqdm_object.n
            tqdm_object.update(n=n_completed)

    original_print_progress = joblib.parallel.Parallel.print_progress
    joblib.parallel.Parallel.print_progress = tqdm_print_progress

    try:
        yield tqdm_object
    finally:
        joblib.parallel.Parallel.print_progress = original_print_progress
        tqdm_object.close()