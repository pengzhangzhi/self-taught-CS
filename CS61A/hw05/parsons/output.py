import sys
import os
class DisableStdout:
    stdout_ref = None
    null_file = None
    def __init__(self):
        if DisableStdout.stdout_ref is None:
            DisableStdout.stdout_ref = sys.stdout

    def __enter__(self):
        f = open(os.devnull, 'w')
        sys.stdout = f
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = DisableStdout.stdout_ref