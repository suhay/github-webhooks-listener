import json
import subprocess


async def processRelease(repo, payload):
    with open('../sites/' + repo + '.json') as f:
      data = json.load(f)

    if 'release' in data.keys() and 'path' in data.keys():
      commands = ['. ~/.nvm/nvm.sh', 'nvm use']
      
      if 'build' in data['release'].keys():
        commands.append(data['release']['build'])

      if 'deploy' in data['release'].keys():
        commands.append(data['release']['deploy'])

      subprocess.check_call(['git', 'fetch', '--all', '--tags'], cwd=data['path'])
      subprocess.check_call(['git', 'checkout', 'tags/' + payload['release']['tag_name']], cwd=data['path'])
      subprocess.Popen(' && '.join(commands), cwd=data['path'], executable='/bin/bash', shell=True)

    return