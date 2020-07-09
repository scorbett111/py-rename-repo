import sys

def splice_argv(index=None, splice=None):
    return sys.argv[index:index+splice]

def remove_argv(index=None, remove=None):
    sys.argv = sys.argv[:index] + sys.argv[index+remove:]
    return sys.argv
