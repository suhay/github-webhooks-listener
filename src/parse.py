from multiprocessing import Process
from release import processRelease
import sys


async def parse(repo, payload):
    if payload['repository']['name'] == repo and 'action' in payload.keys():
        if payload['action'] == 'released' and 'release' in payload.keys():
            p = Process(target=processRelease,
                        args=(repo, payload))
            print(p.pid)
            p.start()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        repo = sys.argv[1]
        payload = sys.argv[2]
        parse(repo, payload)
    elif len(sys.argv) == 2:
        repo = sys.argv[0]
        payload = sys.argv[1]
        parse(repo, payload)
