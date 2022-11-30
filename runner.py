import argparse
import sys, time, os, glob, time
from datetime import datetime, timezone, timedelta
import logging as log
import pathlib
import progressbar
import requests, bs4

sys.path.extend(['..', '.'])
from utils import get_lines, print_stats

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


def get_commands():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rs', action='store_true', help='run_samples')
    parser.add_argument('--so', action='store_true', help='samples_only')
    parser.add_argument('-1', '--p1', action='store_true', help='only part 1')
    parser.add_argument('-2', '--p2', action='store_true', help='only part 2')
    parser.add_argument('-s', '--s', action='store_true', help='submit')
    parser.add_argument('-y', '--yes', action='store_true', help='no prompt')
    parser.add_argument('-i', '--info', action='store_true', help='print info')
    args = parser.parse_args()
    cmds = []
    if not args.p1 and not args.p2:
        cmds.append('run1')
        cmds.append('run2')
    else:
        if args.p1:
            cmds.append('run1')
        else:
            cmds.append('run2')

    if args.s:
        if 'run2' in cmds:
            cmds.append('submit2')
        elif 'run1' in cmds:
            cmds.append('submit1')
    if args.yes:
        cmds.append('no_prompt')

    if args.info: cmds.append('print_stats')
    if args.rs: cmds.append('run_samples')
    if args.so: cmds.append('samples_only')
    return cmds


def run_samples(p1_fn, p2_fn, cmds, FILE):
    for fname, data in get_samples(FILE):
        print(fname)
        if 'run1' in cmds:
            print('p1: ', p1_fn(data))
        if 'run2' in cmds:
            print('p2: ', p2_fn(data))


def run(YEAR, DAY, p1_fn, p2_fn, cmds, FILE=None):
    target = get_target(YEAR, DAY)
    fmt_str = '%(asctime)-15s %(filename)8s:%(lineno)-3d %(message)s'
    log.basicConfig(level=log.DEBUG, format=fmt_str)
    force = 'force_fetch' in cmds
    v = fetch(YEAR, DAY, log, wait_until_date=target, force=force)
    if FILE != None:
        writeInputToFolder(FILE, v)
    if 'print_stats' in cmds:
        print_stats(v)

    if 'run1' in cmds:
        res = p1_fn(v)
        print('part_1: {}'.format(res))
        if 'submit1' in cmds:
            submit(YEAR, DAY, 1, res, 'no_prompt' in cmds)
    if 'run2' in cmds:
        res = p2_fn(v)
        print('part_2: {}'.format(res))
        if 'submit2' in cmds:
            submit(YEAR, DAY, 2, res, 'no_prompt' in cmds)

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
