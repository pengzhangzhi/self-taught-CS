import os
import sys
from threading import Timer
from typing import List
old_client_path = '/Users/tommyjoseph/desktop/okpy-work/ok-client'
show_cases_path = '/Users/Akshit/ok-client-tommy'
show_cases_path = '/Users/tommyjoseph/desktop/okpy-work/show-all-cases/ok-client'
prod_path = 'ok'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.path.abspath(prod_path)))
# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.path.abspath(show_cases_path)))
# in the future, ok-client modules will all be stored in single ok file 

import client.exceptions as ex
from client.sources.common import core
from client.api.assignment import load_assignment
from client.cli.common import messages
from output import DisableStdout 
from load import load_config, path_to_name, problem_name_from_file
from constants import *

from multiprocessing import Semaphore
import webbrowser
import logging
from datetime import datetime
import logging
import json
import re
from flask import Response, request, Flask, render_template, jsonify, redirect, url_for, send_file

log = logging.getLogger('client') # Get top-level logger

# serialize grading and analytics to avoid undesired logs in stdout due to 
# interleaving of multiple analytics events or grading and analytics
sema = Semaphore(1)

# app = Flask(__name__, template_folder=f'templates', static_folder=f'static')
app = Flask(__name__)
cache = {}
                
@app.route('/code_skeleton/<path:problem_name>')
def code_skeleton(problem_name):
    return parsons(problem_name, code_skeleton=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/code_arrangement/<path:problem_name>')
def parsons(problem_name, code_skeleton=False):
    problem_config = load_config(problem_name)
    language = problem_config.get('language', 'python')

    code_lines = problem_config['code_lines'] + \
             '\nprint(\'DEBUG:\', !BLANK)' * 2 + '\n# !BLANK' * 2
    repr_fname = f'{PARSONS_FOLDER_PATH}/{problem_name.lower()}{PARSONS_REPR_SUFFIX}'
    if os.path.exists(repr_fname):
        with open(repr_fname, "r", encoding="utf8") as f:
            code_lines = f.read()

    cur_prob_index = cache[PROBLEM_NAMES].index(problem_name)

    not_last_prob = cur_prob_index < len(cache[PROBLEM_NAMES]) - 1
    not_first_prob = cur_prob_index > 0
    is_required = problem_name in cache[REQUIRED_PROBLEMS]
    return render_template('parsons.html',
                         problem_name=problem_name,
                         algorithm_description=problem_config[
                             'algorithm_description'],
                         problem_description=problem_config[
                             'problem_description'],
                         test_cases=problem_config['test_cases'],
                         # TODO(nweinman): Better UI for this (and comment
                         # lines as well)
                         code_lines=code_lines,
                         next_problem=None,
                         back_url=None,
                         code_skeleton=code_skeleton,
                         language=language,
                         not_first_prob=not_first_prob,
                         not_last_prob=not_last_prob,
                         is_required=is_required
                         )

@app.route('/next_problem/<path:problem_name>', methods=['GET'])
def next_problem(problem_name):
    new_prob_name = cache[PROBLEM_NAMES][cache[PROBLEM_NAMES].index(problem_name) + 1]
    return redirect(url_for('code_skeleton', problem_name=new_prob_name))


@app.route('/prev_problem/<path:problem_name>', methods=['GET'])
def prev_problem(problem_name):
    new_prob_name = cache[PROBLEM_NAMES][cache[PROBLEM_NAMES].index(problem_name) - 1]
    return redirect(url_for('code_skeleton', problem_name=new_prob_name))

@app.route('/get_problems/', methods=['GET'])
def get_problems():
    try:
        with open(PARSONS_CORRECTNESS, "r", encoding="utf8") as f:
            probs_correct = json.loads(f.read())
    except FileNotFoundError:
        probs_correct = {pname : False for pname in cache[PROBLEM_NAMES]}
        with open(PARSONS_CORRECTNESS, "w", encoding="utf8") as f:
            f.write(json.dumps(probs_correct))

    req_names = [f'{pname} {CHECK_MARK if probs_correct[pname] else RED_X}' for pname in cache[REQUIRED_PROBLEMS]]
    req_paths = [f'/code_skeleton/{pname}' for pname in cache[REQUIRED_PROBLEMS]]
    opt_names = [f'{pname} {CHECK_MARK if probs_correct[pname] else RED_X}' for pname in cache[OPTIONAL_PROBLEMS]]
    opt_paths = [f'/code_skeleton/{pname}' for pname in cache[OPTIONAL_PROBLEMS]]

    required = {'names': req_names, 'paths': req_paths} 
    optional = {'names': opt_names, 'paths': opt_paths}
    return {'required': required, 'optional': optional}

@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def catch_all(u_path):
    if os.path.exists(u_path):
        combined = os.path.join('..', u_path)
        return send_file(combined)
    return f'Sorry, nothing at {u_path}'


def error_handling_and_synch(f):
    def decorated():
        sema.acquire()
        try:
            result = f()
        except ex.LoadingException as e:
            sema.release()
            return Response(f"Error while loading assignment: {str(e)}", status=400)
        except AssertionError as e:
            sema.release()
            return Response(f"{str(e)}", status=400)
        sema.release()
        return result
    decorated.__name__ = f.__name__
    return decorated


@app.route('/submit/', methods=['POST'])
@error_handling_and_synch
def submit():
    problem_name = request.form['problem_name']
    submitted_code = request.form['submitted_code']
    parsons_repr_code = request.form['parsons_repr_code']
    fname = f'{PARSONS_FOLDER_PATH}/{problem_name.lower()}.py'
    write_parsons_prob_locally(fname, submitted_code, parsons_repr_code, True)
    test_results = grade_and_backup(problem_name)
    return jsonify({'test_results': test_results})

@app.route('/analytics_event', methods=['POST'])
@error_handling_and_synch
def analytics_event():
    """
    {
        problem_name: string,
        event: 'start' | 'stop'
    }
    Triggered when user starts interacting with the problem and when they stop (e.g. switch tabs). 
    This data can be used to get compute analytics about time spent on parsons.
    """
    e, problem_name = request.json['event'], request.json['problem_name']
    msgs = messages.Messages()
    args = cache['args']
    args.question = [problem_name]
    with DisableStdout():
        assign = load_assignment(args.config, args)
    if e == 'start':
        msgs['action'] = 'start'
    elif e == 'stop':
        msgs['action'] = 'stop'

    msgs['problem'] = problem_name
    analytics_protocol = assign.protocol_map['analytics']
    backup_protocol = assign.protocol_map['backup']
    with DisableStdout():
        analytics_protocol.run(msgs)
        backup_protocol.run(msgs)

    msgs['timestamp'] = str(datetime.now())
    return jsonify({})

def find_next_unindented_line(lines: List[str], start: int):
    """
    Finds the next piece of unindented code in the file. Ignores emtpy lines and lines
    that start with a space or tab. Returns len(lines) if no unindented line found.
    """
    j = start
    while j < len(lines) and (lines[j] == '' or lines[j].startswith((' ', '\t', '\n'))):
        j += 1
    return j

def write_parsons_prob_locally(path, code, parsons_repr_code, write_repr_code):
    start_line = -1
    in_docstring = False
    lines: List[str]= []
    with open(path, "r", encoding="utf8") as f:
        lines = [line for line in f]
    for i, line in enumerate(lines):
        if '"""' in line.strip():
            if in_docstring:
                start_line = i + 1
                break
            in_docstring = True

    assert start_line >= 0, f"Problem not found in file {path}. This can be due to missing doctests."

    code_lines = code.split("\n")
    assert "def" in code_lines[0] or "class" in code_lines[0], "First code block must be the `def` statement or `class` declaration"

    code_lines.pop(0) # remove function def or class declaration statement, is relied on elsewhere
    line = find_next_unindented_line(code_lines, 0)
    indent_in_code = line != len(code_lines)
    assert not indent_in_code, "All lines in a function or class definition should be indented at least once. It looks like you have a line that has no indentation." 

    problem_lines_to_preserve = lines[:start_line]
    end_of_replace_lines = find_next_unindented_line(lines, start_line)
    extra_lines_to_preserve = lines[end_of_replace_lines:]

    with open(path, "w", encoding="utf8") as f:
        for line in problem_lines_to_preserve:
            f.write(line)
        for line in code_lines:
            f.write(line + "\n")
        for line in extra_lines_to_preserve:
            f.write(line)

    # write parsons repr code
    # used our own representation instead of Nate's most_recent_parsons()
    if write_repr_code:
        repr_fname = f'{path[:-3]}{PARSONS_REPR_SUFFIX}'
        with open(repr_fname, "w", encoding="utf8") as f:
            f.write(parsons_repr_code)

def store_correctness(prob_name, is_correct):
    try:
        with open(PARSONS_CORRECTNESS, "r", encoding="utf8") as f:
            probs_correct = json.loads(f.read())
    except OSError:
        probs_correct = {pname : False for pname in cache[PROBLEM_NAMES]}
    probs_correct[prob_name] = is_correct

    with open(PARSONS_CORRECTNESS, "w", encoding="utf8") as f:
        f.write(json.dumps(probs_correct))

def load_assignment_if_possible(args):
    """
    A syntax error in a source file leads to ok not being able to load an assignment.
    For parsons files, we can get around this by replacing a parsons program with dummy
    code. This function will do that if necessary and return the assignment, or raise
    the relevant LoadingException if a different error occurs (such as a syntax error 
    in the main python file).
    """
    # remove syntax errors so assignment can load
    num_retries = MAX_NUM_RETRIES
    reloaded = []
    assign = None
    while num_retries > 0:
        try:
            assign = load_assignment(args.config, args)
            break
        except ex.LoadingException as e:
            # TODO: LoadingException unique with syntax error (vs missing .ok, for example)
            if PARSONS_FOLDER_NAME not in str(e):
                raise
            fname = str(e).split(" ")[-1]
            rel_path = fname.split("/")[1]
            problem_name = rel_path[:-3]
            reloaded.append(problem_name)
            # replaces syntax-error code with error-free dummy code 
            write_parsons_prob_locally(fname, "def dummy():\n    print('Syntax Error')\n", None, False)
            num_retries -= 1
    return assign

def grade_and_backup(problem_name):
    args = cache['args']
    args.question = [problem_name]
    msgs = messages.Messages()
    old_stdout = sys.stdout
    sys.stdout = out = open(PARSONS_OUTFILE, 'w')
    assign = load_assignment(args.config, args)

    for name, proto in assign.protocol_map.items():
        log.info('Execute {}.run()'.format(name))
        proto.run(msgs)
    out.close()
    sys.stdout = old_stdout
    msgs['timestamp'] = str(datetime.now())
    feedback = {}
    feedback['passed'] = assign.specified_tests[0].console.cases_passed
    feedback['failed'] = assign.specified_tests[0].console.cases_total - feedback['passed']

    # get output from doctests
    with open(PARSONS_OUTFILE, "r", encoding="utf8") as f:
        all_lines = f.readlines()
        # still need to fix ok-client show all cases to not print extra ------
        # feedback['doctest_logs'] = "".join(all_lines[3:-10])
        log_lines  = all_lines[9:-10]

    if is_syntax_error(feedback):
        log_lines = get_useful_syntax_error_logs(log_lines, problem_name)

    feedback['doctest_logs'] = "".join(log_lines)
    # passed == 0 and failed == 0 can be a result of SyntaxError so we check passed >= 1 instead
    store_correctness(problem_name, feedback['passed'] >= 1 and feedback['failed'] == 0)
    return feedback

def get_useful_syntax_error_logs(logs, problem_name):
    file_index = -1
    traceback_index = -1
    for i in range(len(logs) - 1, -1, -1):
        if "File" in logs[i]:
            file_index = i
            break
    for i in range(len(logs)):
        if "Traceback" in logs[i]:
            traceback_index = i
            break
    if file_index == -1 or traceback_index == -1:
        return logs
    
    docstring_lines = count_docstring_lines(problem_name)
    logs[file_index]
    match = re.search(r"line ([0-9]+)", logs[file_index])
    if not match:
        return logs

    original_line_num = int(match.group(1))
    logs[file_index] = re.sub(r"line ([0-9]+)", f"line {original_line_num - docstring_lines}", logs[file_index])

    return logs[:traceback_index + 1] + logs[file_index:]

def count_docstring_lines(problem_name):
    fname = f'{PARSONS_FOLDER_PATH}/{problem_name.lower()}.py'
    num_lines = 0
    with open(fname, "r", encoding="utf8") as f:
        for i, line in enumerate(f):
            if '"""' in line:
                i += 1
                break
        num_lines = 2
        for _, line in enumerate(f, start=i):
            if '"""' in line:
                break
            num_lines += 1
    return num_lines

def is_syntax_error(feedback):
    return feedback['passed'] == 0 and feedback['failed'] == 0

def open_browser():
    webbrowser.open_new(f'http://127.0.0.1:{PORT}/')

def open_in_browser(args):
    cache['args'] = args 
    # parsons folder must exist
    assert os.path.isdir(PARSONS_FOLDER_PATH), "parsons folder does not exist"
    Timer(1, open_browser).start()
    run_server(PORT)

def setup():
    args = cache['args']

    try:
        with DisableStdout():
            assign = load_assignment_if_possible(args)
    except ex.LoadingException as e:
        print(f"Error while loading assignment: {str(e)}. This is likely due to a syntax error in the mentioned file.")
        exit(1)

    # can assume proper structure since okpy checks for it
    assert assign.parsons != core.NoValue, "parsons param not found in .ok file"
    cache[REQUIRED_PROBLEMS] = []
    cache[OPTIONAL_PROBLEMS] = []

    for pgroup_name, v in assign.parsons.items():
        req_lst = v.get('required', [])
        opt_lst = v.get('optional', [])
        cache[REQUIRED_PROBLEMS].extend(req_lst)
        cache[OPTIONAL_PROBLEMS].extend(opt_lst)

    cache[PROBLEM_NAMES] = cache[REQUIRED_PROBLEMS] + cache[OPTIONAL_PROBLEMS]

def run_server(port):
    global PORT
    # disable flask logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    for port in range(PORT, PORT + 10):
        try:
            PORT = port
            print("Press Ctrl + C to kill the process.")
            setup()
            app.run(port=port)
            exit(0)
        except OSError as e:
            print(e)
            print(f"Port {port} is currently in use, trying a different port...")
