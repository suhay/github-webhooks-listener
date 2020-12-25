# GitHub Webhooks Listener

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

A simple listener that will trigger custom scripts when it receives events from GitHub.

## Usage

```bash
$ git clone git@github.com:suhay/github-webhooks-listener.git
$ cd github-webhooks-listener
$ python setup.py install --user
```

### .env file

```
API_TOKEN=YOUR_GITHUB_SECRET
```

### Repo configuration files

```bash
.
├── README.md
└── sites
    └── my-site.json
```

```json
my-site.json

{
  "path": "/home/code/my-site",
  "release": {
    "build": "yarn && yarn build && tar -xvf {{release.sha}}.tar.gz", # you may use handlebar notation to inject GitHub payload values into your steps
    "deploy": "rsync -av --delete public/ /var/www/html/my-site",
    "cleanup": "rm -rf node_modules/ && rm -rf .cache/ && yarn cache clean"
  }
}
```

### Adding listener to GitHub Webhooks

As of `v0.2.1` - Only the `release` event is supported.

`https://{domain}/webhooks/{repo}`  
or  
`https://yoursite.com/webhooks/my-site`

The `repo` name must match the repository name (minus the user/org name) sent from GitHub and also the respective `.json` file that contains its custom scripts.

### Deploying with Hypercorn

```bash
$ sudo nano /etc/systemd/system/github-webhooks-listener.service
```

```bash
[Unit]
Description=GitHub Webhooks Listener
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=ubuntu
ExecStart=/home/ubuntu/.local/bin/hypercorn /mnt/projects/github-webhooks-listener/src/app --bind 127.0.0.1:5000

[Install]
WantedBy=multi-user.target
```

Within your Apache2 `.conf`

```bash
ProxyPass /webhooks http://localhost:5000/webhooks
ProxyPassReverse /webhooks https://localhost:5000/webhooks
```