import json
import subprocess
import os
from pybars import Compiler

compiler = Compiler()


def processRelease(repo, payload):
    base_path = os.environ.get("SITES")
    file_name = repo + '.json'
    file_path = base_path + '/' + file_name

    with open(file_path) as f:
        data = json.load(f)

    if 'release' in data.keys() and 'path' in data.keys():
        commands = []
        if 'build' in data['release'].keys():
            source = data['release']['build']
            template = compiler.compile(source)
            commands.append(template(payload))

        if 'deploy' in data['release'].keys():
            source = data['release']['deploy']
            template = compiler.compile(source)
            commands.append(template(payload))

        if 'cleanup' in data['release'].keys():
            source = data['release']['cleanup']
            template = compiler.compile(source)
            commands.append(template(payload))

        subprocess.check_call(
            ['git', 'fetch', '--all', '--tags'], cwd=data['path'])
        subprocess.check_call(
            ['git', 'checkout', 'tags/' + payload['release']['tag_name']], cwd=data['path'])

        with subprocess.Popen(' && '.join(commands), cwd=data['path'], executable='/bin/bash', shell=True) as process:
            print('Runing process: ' + process.pid)
            try:
                process.communicate(timeout=300)
            except subprocess.TimeoutExpired:
                print('Process was killed by timeout: 300 seconds')
                raise
            finally:
                process.kill()
                process.communicate()
                print('Release complete!')

    return
