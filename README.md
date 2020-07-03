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
    "build": "yarn && yarn build",
    "deploy": "rsync -av --delete public/ /var/www/html/my-site"
  }
}
```

### Adding listener to GitHub Webhooks

As of `v0.1.0` - Only the `release` event is supported.

`https://{domain}/webhooks/{repo}`  
or  
`https://yoursite.com/webhooks/my-site`

The `repo` name must match the repository name (minus the user/org name) sent from GitHub and also the respective `.json` file that contains its custom scripts.