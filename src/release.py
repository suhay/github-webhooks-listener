import json
import subprocess
import os.path

from os import path
from pathlib import Path


def processRelease(repo, payload):
    base_path = Path(__file__).parent
    file_name = repo + '.json'
    file_path = (base_path / '..' / 'sites' / file_name).resolve()

    with open(file_path) as f:
      data = json.load(f)

    if 'release' in data.keys() and 'path' in data.keys():
      commands = []

      if path.exists(base_path / '..' / '.nvmrc'):
        commands.append('. ~/.nvm/nvm.sh')
        commands.append('nvm use')
      
      if 'build' in data['release'].keys():
        commands.append(data['release']['build'])

      if 'deploy' in data['release'].keys():
        commands.append(data['release']['deploy'])

      subprocess.check_call(['git', 'fetch', '--all', '--tags'], cwd=data['path'])
      subprocess.check_call(['git', 'checkout', 'tags/' + payload['release']['tag_name']], cwd=data['path'])

      with subprocess.Popen(' && '.join(commands), cwd=data['path'], executable='/bin/bash', shell=True) as process:
        try:
          process.communicate(timeout=120)
        except subprocess.TimeoutExpired:
          print('Process was killed by timeout: 120 seconds.')
          raise
        finally:
          if process.poll() is None:
            process.kill()
            process.communicate()

    return