[![Build Status](https://travis-ci.com/thisismetis/gamma-cli.svg?token=tJ687Bi2a1fC7eLRuHQg&branch=master)](https://travis-ci.com/thisismetis/gamma-cli)

# gamma-cli
The command line tool for the gamma curriculum

# Installation

This tool is maintained behind a private repo which creates some minor annoyances. I'll be smoothing out the install and update process shortly but for now, here's what that looks like (You will need to set up [SSH keys with GitHub](https://help.github.com/articles/connecting-to-github-with-ssh/) in order for the following scripts to work.):

install:
```bash
mkdir -p ~/.gamma; git clone git@github.com:thisismetis/gamma-cli.git ~/.gamma/gamma-cli; pip install -e ~/.gamma/gamma-cli
```

update:
```bash
cd ~/.gamma/gamma-cli; git pull
```
