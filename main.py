import argparse
import os
import sys
from multiprocessing import Process

PYTHONCMD = sys.executable
print(f"Python解释器路径: {PYTHONCMD}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clip', help='剪贴板功能的api地址', default=False)
    parser.add_argument('-f', '--frpc', help='frp的服务端地址', default=False)
    args = parser.parse_args()

    if args.clip:
        from clip import start

        start(args.clip)

    if args.frpc:
        frpc = Process(target=os.system,
                       args=(f"frpc tcp -s {args.frpc} -l 5000 -r 3001 -n clip_{os.environ.get('USER')}",))
        frpc.start()

    os.system(f"exec {PYTHONCMD} -u app.py")
