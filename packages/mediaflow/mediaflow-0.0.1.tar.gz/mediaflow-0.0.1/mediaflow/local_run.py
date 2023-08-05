#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


def walk_predictor_path(inpath, data):
    so_path = {
        r
        for r, d, f in os.walk(inpath) for ff in f
        if ff.endswith('.so') or ('.so.' in ff)
    }
    # FIXME: current dir is added to LD_LIBRARY_PATH, need better solution
    if len(so_path) > 0:
        if data in so_path:
            env = ':'.join(so_path) + ':'
        else:
            env = data + ':' + ':'.join(so_path) + ':'
    else:
        env = data + ':'
    return env


def parse_library_path(in_path):
    if os.path.exists(in_path):
        library_path = walk_predictor_path(in_path, in_path)
    else:
        library_path = ''
    return library_path


# local run the mediaflow example, which some processors has a lot of dynamic lib
# so here, walk all the dyanamic lib and add their directory to the ENV LD_LIBARY_PATH
def main():
    if len(sys.argv) != 2:
        raise Exception('Bad parameters list.')

    run_file = sys.argv[1]

    currrent_worker_directory = os.getcwd()
    env = parse_library_path(currrent_worker_directory)
    oldenv = os.getenv('LD_LIBRARY_PATH')
    if oldenv is not None:
        if oldenv.startswith(':'):
            env += oldenv
        else:
            env += ':' + oldenv
    os.environ['LD_LIBRARY_PATH'] = env

    exe = os.readlink('/proc/self/exe')
    os.system('%s %s' % (exe, run_file))


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        exit(1)
