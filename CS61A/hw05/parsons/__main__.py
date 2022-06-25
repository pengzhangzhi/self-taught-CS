import sys
import os
from local_server import open_in_browser
from client.utils import auth 
from client.cli.ok import parse_input
args = parse_input()
args.parsons = True
if not auth.authenticate(args):
    exit(1)
open_in_browser(args)
