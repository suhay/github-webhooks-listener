from multiprocessing import Process
from release import processRelease


async def parse(repo, payload):
    if payload['repository']['name'] == repo and 'action' in payload.keys():
        if payload['action'] == 'released' and 'release' in payload.keys():
            p = Process(target=processRelease,
                        args=(repo, payload))
            print(p.pid)
            p.start()
