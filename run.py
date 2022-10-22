#!python

import argparse
import os
import sys

PYTHONCMD = sys.executable
print(f"Python解释器路径: {PYTHONCMD}")

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--rebuild', help='强制重新构建', action="store_true")
args, unknown_args = parser.parse_known_args()

if args.rebuild:
    os.system("rm -rf venv")
    print("will rebuild venv")

os.system(f"{PYTHONCMD} --version")

if not os.path.exists("venv"):
    os.system(f"""
    {PYTHONCMD} -m virtualenv venv
    source venv/bin/activate
    pip -V
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  -r requirements.txt
    deactivate
    """)

if not os.path.exists("static/albums/screenshot"):
    screenshot = f"{os.environ.get('HOME')}/Desktop/screenshot"
    if not os.path.exists(screenshot):
        os.mkdir(screenshot)
    os.symlink(screenshot, "static/albums/screenshot")

os.system(f"""
source venv/bin/activate
python main.py {' '.join(unknown_args)}
""")
