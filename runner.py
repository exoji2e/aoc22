import argparse
import sys, time, os, glob, time, errno, shutil
from datetime import datetime, timezone, timedelta
import logging as log
import pathlib
import progressbar
import requests, bs4
import pyperclip
import shutil

sys.path.extend(['..', '.'])
from utils import get_lines, print_stats

class Tie:
    def __init__(self, out_streams):
        self.out_streams = out_streams
    def write(self, s):
        for o in self.out_streams:
            o.write(s)
    def close(self):
        for o in self.out_streams:
            o.close()
    def flush(self):
        for o in self.out_streams:
            o.flush()


def copy_to_clipboard(s):
    pyperclip.copy(str(s))

def submit_real(year, day, level, answer):
    from secret import session
    jar = requests.cookies.RequestsCookieJar()
    jar.set('session', session)
    url = 'https://adventofcode.com/{}/day/{}/answer'.format(year, day)
    byte_ans = str(answer).encode('utf-8')
    assert level == 1 or level == 2
    byte_level = b'1' if level == 1 else b'2'
    data = {
        b'answer' : byte_ans,
        b'level' : byte_level
    }
    r = requests.post(url, data=data, cookies=jar)

    if not r.status_code == 200:
        return 'StatusCode: {}\n{}'.format(r.status_code, r.text)

    html = bs4.BeautifulSoup(r.text, 'html.parser')
    return html.find('article').text


def submit(year, day, level, answer, no_prompt):
    print('About to submit: "{}" on part {}, day {} {}'.format(answer, level, day, year))
    print('Confirm submit? y/N')
    ans = 'y' if no_prompt else input()
    if ans.lower() == 'y':
        print('Submitting {}'.format(answer))
        text = submit_real(year, day, level, answer)
        if "That's the right answer" in text:
            print('AC!')
        print('>> ' + text)
        return text
    else:
        print('Skipping submit')


def dl(fname, day, year):
    from secret import session
    jar = requests.cookies.RequestsCookieJar()
    jar.set('session', session)
    url = 'https://adventofcode.com/{}/day/{}/input'.format(year, day)
    r = requests.get(url, cookies=jar)
    if 'Puzzle inputs' in r.text:
        log.w('Session cookie expired?')
        return r.text
    if "Please don't repeatedly request this endpoint before it unlocks!" in r.text:
        log.w('Output not available yet')
        return r.text
    if r.status_code != 200:
        log.w('Not 200 as status code')
        return r.text
    with open(fname,'w') as f:
        f.write(r.text)
    return 0

def mkdirs(f):
    try:
        os.makedirs(f)
    except: pass

def symlink_force(target, link_name):
    try:
        os.remove(link_name)
        os.symlink(target, link_name)
    except: pass

def wait_until(date_time):
    now = datetime.now().astimezone()
    tE = date_time.timestamp()
    t0 = now.timestamp()
    M = int(tE-t0) + 1
    if M <= 0: return
    widgets=[
        ' [', progressbar.CurrentTime(), '] ',
        progressbar.Bar(),
        ' (', progressbar.ETA(), ') ',
    ]
    print(f'waiting from {now} until {date_time}')
    bar = progressbar.ProgressBar(max_value=int(tE-t0), widgets=widgets)
    while time.time() < tE:
        cT = time.time()
        bar.update(min(M, int(cT - t0)))
        time.sleep(1)
    bar.finish()

def get_input_file_name(year, day):
    return 'cache/{}-{}.in'.format(year, day)


def fetch(year, day, log, force=False, wait_until_date=-1):
    filename = get_input_file_name(year, day)
    mkdirs('cache')
    exists = os.path.isfile(filename)
    if not exists or force:
        if wait_until_date != -1:
            wait_until(wait_until_date)

        out = dl(filename, day, year)
        if out != 0:
            return out
    return open(filename, 'r').read().strip('\n')


def get_samples(FILE):
    parent = get_folder(FILE)
    d = '{}/samples'.format(parent)
    mkdirs(d)
    samples = []
    for fname in sorted(glob.glob('{}/*.in'.format(d))):
        inp = open(fname, 'r').read().strip('\n')
        if len(inp) < 2: continue
        name = pathlib.Path(fname).name
        samples.append((name, inp))
    return samples

def get_target(YEAR, DAY):
    target = datetime(YEAR, 12, DAY, 5, tzinfo=timezone.utc).astimezone()
    return target + timedelta(milliseconds=200)

def writeInputToFolder(FILE, content):
    parent = pathlib.Path(FILE).parent.absolute()
    input_dst = '{}/input.in'.format(parent)
    with open(input_dst,'w') as f:
        f.write(content)

def get_folder(FILE):
    return pathlib.Path(FILE).parent.absolute()



class Options:
    def __init__(self, args):
        def getPartsToRun(args):
            if args.p1 and not args.p2:
                return True, False
            if not args.p1 and args.p2:
                return False, True
            return True, True
        self.p1, self.p2 = getPartsToRun(args)
        self.submit = args.s
        self.auto_yes = args.yes
        self.copy = not args.no_copy
        self.print_stats = args.info
        self.force_fetch = args.force_fetch
        if args.pipe:
            self.run_options = 'PIPE'
        elif args.in_file:
            self.run_options = 'IN_FILE'
            self.in_file = args.in_file
        elif args.so:
            self.run_options = 'SAMPLES_ONLY'
        elif args.rs:
            self.run_options = 'RUN_BOTH'
        else:
            self.run_options = 'RUN_INPUT'
    def print_info(self):
        return self.run_options == 'RUN_INPUT' and self.print_stats
    def submit1(self):
        return self.submit and not self.p2
    def submit2(self):
        return self.submit and self.p2
    def run_samples(self):
        return self.run_options in ['RUN_BOTH', 'SAMPLES_ONLY']
    def run_input(self):
        return self.run_options in ['RUN_BOTH', 'RUN_INPUT']
    def run_in_file(self):
        return self.run_options == 'IN_FILE'
    def run_pipe(self):
        return self.run_options == 'PIPE'
    def __repr__(self):
        return f'{self.run_options}; p1:{self.p1} p2:{self.p2}'

def get_commands():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rs', action='store_true', help='run_samples')
    parser.add_argument('--so', action='store_true', help='samples_only')
    parser.add_argument('-p', '--pipe', action='store_true', help='read input from stdin')
    parser.add_argument('-f', '--in_file', default=None, help='in_file')
    parser.add_argument('-1', '--p1', action='store_true', help='only part 1')
    parser.add_argument('-2', '--p2', action='store_true', help='only part 2')
    parser.add_argument('-s', '--s', action='store_true', help='submit')
    parser.add_argument('-n', '--no_copy', action='store_true', help='skip copying')
    parser.add_argument('-y', '--yes', action='store_true', help='no prompt')
    parser.add_argument('-i', '--info', action='store_true', help='print info')
    parser.add_argument('--force_fetch', action='store_true', help='force fetch')
    args = parser.parse_args()
    return Options(args)


def run_samples(p1_fn, p2_fn, options, FILE):
    for fname, data in get_samples(FILE):
        run_sample(data, p1_fn, p2_fn, fname, options)

def run_sample(data, p1_fn, p2_fn, name, options):
    if options.p1:
        print(f'[{name}] p1: "{ p1_fn(data) }"')
    if options.p2:
        print(f'[{name}] p2: "{ p2_fn(data) }"')


def print_and_copy(part, res, copy):
    if copy:
        copy_to_clipboard(res)
    copy_msg = ('- copied to clipboard' if copy else '')
    print(f'part_{part}: "{res}" {copy_msg}')

def run(YEAR, DAY, p1_fn, p2_fn, options, FILE):
    target = get_target(YEAR, DAY)
    fmt_str = '%(asctime)-15s %(filename)8s:%(lineno)-3d %(message)s'
    log.basicConfig(level=log.DEBUG, format=fmt_str)
    input_data = fetch(YEAR, DAY, log, wait_until_date=target, force=options.force_fetch)
    if FILE != None:
        writeInputToFolder(FILE, input_data)
    if options.print_info():
        print_stats(input_data)

    if options.p1:
        res = p1_fn(input_data)
        print_and_copy(1, res, options.copy)
        if options.submit1():
            submit(YEAR, DAY, 1, res, options.auto_yes)
    if options.p2:
        res = p2_fn(input_data)
        print_and_copy(2, res, options.copy)
        if options.submit2():
            submit(YEAR, DAY, 2, res, options.auto_yes)

def creteClone(file):
    file = pathlib.Path(file)
    file_name = file.name
    d = datetime.now()
    timeStr = d.isoformat().replace(':', '-').split('.')[0]
    folder = f'runs/{timeStr}'
    mkdirs(folder)
    symlink_force(f'{folder}', 'last_run')
    shutil.copyfile(file, f'{folder}/{file_name}')
    stdout_file = open(f'{folder}/out.txt', 'w')
    sys.stdout = Tie([sys.__stdout__, stdout_file])



def main(YEAR, DAY, p1_fn, p2_fn, options, FILE=None):
    creteClone(FILE)
    if options.run_samples():
        run_samples(p1_fn, p2_fn, options, FILE)
    if options.run_input():
        run(YEAR, DAY, p1_fn, p2_fn, options, FILE)
    if options.run_in_file():
        data = open(options.in_file).read()
        run_sample(data, p1_fn, p2_fn, options.in_file, options)
    if options.run_pipe():
        data = sys.stdin.read()
        run_sample(data, p1_fn, p2_fn, 'PIPE', options)


def create_day(day):
    padded = '{:02d}'.format(day)
    file_path = f'{padded}/day{padded}.py'
    samples = f'{padded}/samples'
    mkdirs(padded)
    mkdirs(samples)
    with open(file_path, 'w') as t:
        with open('template.py') as s:
            t.write(s.read().replace('datetime.date.today().day', str(day)))
    sample1 = f'{samples}/1.in'
    with open(sample1, 'w') as f:
        f.write('')
