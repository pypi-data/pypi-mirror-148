#! /usr/bin/env python
from io import TextIOWrapper
import logging
import os
import multiprocessing
import time
import pathlib

# NOTE
# this seems to be OS specific
# getting the project to run on OSX (Apple) required this
# not sure if this is the case for Windows
# Linux does not seem to have this issue? Tested on Arch
multiprocessing.set_start_method("fork")

cached_storage_path = None

# make read destructive
def get_pid_file_path(pid) -> pathlib.Path:
    return pathlib.Path(".hermes_pids/%d" % pid)

# return the pid of the running thread
def get_pid() -> int:
    return os.getpid()

def create_new_path() -> pathlib.Path:
    # create a dummy path
    if not os.path.exists("experiments"):
        logging.info("Creating new directory %s" % pathlib.Path("experiments"))
        os.mkdir(pathlib.Path("experiments"))

    if not os.path.exists(pathlib.Path("experiments/unassigned")):
        logging.info("Creating new directory %s" % pathlib.Path("experiments/unassigned"))
        os.mkdir(pathlib.Path("experiments/unassigned"))

    return pathlib.Path(pathlib.Path("experiments/unassigned"))

def get_path() -> pathlib.Path:
    global cached_storage_path
    if cached_storage_path is None:
        pid = get_pid()
        pid_path = get_pid_file_path(pid)

        # if the file has not yet been created wait
        # wait for half a second -> then create path
        start = time.time()
        while not os.path.exists(pid_path):
            if time.time() - start > 0.2:
                # we are sure that no experiment file is present
                # -> we create a new one
                cached_storage_path = create_new_path()
                return cached_storage_path

            time.sleep(0.01)
        
        if os.path.exists(pid_path):
            with open(pid_path, "r") as f:
                cached_storage_path = pathlib.Path(f.read())
                # make read destructive
                os.remove(pid_path)
        else:
            # we should never get here
            raise FileNotFoundError

        return cached_storage_path
    else:
        return cached_storage_path

# write a file to the correct path given by the pid file
def open_file(name, *args, **kwargs) -> TextIOWrapper:
    path = get_path().joinpath(pathlib.Path(name))
    return open(path, *args, **kwargs)
