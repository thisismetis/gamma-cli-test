[![Build Status](https://travis-ci.com/thisismetis/gamma-cli.svg?token=tJ687Bi2a1fC7eLRuHQg&branch=master)](https://travis-ci.com/thisismetis/gamma-cli)

# gamma-cli
The command line tool for the gamma curriculum

# Installation

This tool is maintained behind a private repo, so it is not hosted on the python package index. You will need to set up [SSH keys with GitHub](https://help.github.com/articles/connecting-to-github-with-ssh/) in order for the following script to work. It will clone this repo to `~/.gamma/gamma-cli` and use an editable install:

```bash
mkdir -p ~/.gamma; git clone git@github.com:thisismetis/gamma-cli.git ~/.gamma/gamma-cli; pip install -e ~/.gamma/gamma-cli
```
