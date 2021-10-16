import json
import subprocess
import os.path

from os import path
from pathlib import Path
from pybars import Compiler

compiler = Compiler()

def processRelease(repo, payload):
    base_path = Path(__file__).parent
    file_name = repo + '.json'
    file_path = (base_path / '..' / 'sites' / file_name).resolve()

    with open(file_path) as f:
      data = json.load(f)

    if 'release' in data.keys() and 'path' in data.keys():
      commands = []
      
      cwd = data['cwd']

      if path.exists(base_path / '..' / '.nvmrc'):
        commands.append('. ' + cwd + '/.nvm/nvm.sh')
        commands.append('nvm use')
      elif 'node' in data.keys():
        commands.append('. ' + cwd + '/.nvm/nvm.sh')
        commands.append('nvm use ' + data['node'])

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

      subprocess.check_call(['git', 'fetch', '--all', '--tags'], cwd=data['path'])
      subprocess.check_call(['git', 'checkout', 'tags/' + payload['release']['tag_name']], cwd=data['path'])

      with subprocess.Popen(' && '.join(commands), cwd=data['path'], executable='/bin/bash', shell=True, stdout=subprocess.PIPE) as process:
        try:
          process.communicate(timeout=300)
          while True:
            line = process.stdout.readline()
            if line == '' and process.poll() is not None:
              break
            if line:
              print(line.rstrip())
        except subprocess.TimeoutExpired:
          print('Process was killed by timeout: 300 seconds')
          raise
        finally:
          print('Process complete')
          process.kill()
          process.communicate()
          print('Release complete!')

    return