# Gitmouth - SSH-to-Git Server for Openruko

## Introduction

`gitmouth` is a small SSH server written in Python using the [Twisted
engine](http://twistedmatrix.com/trac/) framework to handle git push and pull
commands users make to manage their remote git repositories. It authenticates
the user by matching their public key fingerprint against the API server
database, then asks the API server to provision a dyno (a virtualization
container) with the respective git repository mounted, finally it connects to
this dyno over an SSH-like protocol and runs the git-receive-pack or git-
upload-pack command, which in turn will execute the buildpack via git hooks.

For those not familiar with Heroku infrastructure, as buildpacks can contain
potentially dangerous code the git command has to run inside an isolated dyno
too, hence gitmouth is simply a bridge from the ssh transport to where the git
commands run inside a dyno, authenticating and authorizing the request in the
pipeline.


## Requirements

Tested on Linux 3.2 using Python 2.7.3.

On a fresh Ubuntu 12.04 LTS instance:

    $ apt-get install python python-dev
    $ apt-get install python-virtualenv

Please share experiences with CentOS, Fedora, OS X, FreeBSD etc... I am fairly
confident it will not work on Windows based machines however.


## Installation

Ensure [virtualenv](http://www.virtualenv.org/en/latest/#installation) is
installed then:

    # Getting the code
    $ git clone https://github.com/openruko/gitmouth.git gitmouth
    $ cd gitmouth
    # Isolating and installing dependencies
    $ make init
    # Setting up temporary openssl certs
    $ make certs


## Environment Variables

`gitmouth` will check for the presence of several environment variables, these
must be configured as part of the process start - e.g. configured in
supervisord or as part of boot script see `./gitmouth/bin/gitmouth`

* APISERVER_KEY - special key to authenticate with API server. Example:
  `APISERVER_KEY=abcdef-342131-123123123-asdasd`


## Launch

    $ cat > .env << EOF
    PYTHONUNBUFFERED=true
    APISERVER_KEY=$WHAT_WAS_WRITTEN_AT_THE_END_OF_APISERVER_SETUP
    EOF
    $ make run


## Help and Todo

My Python is a little rusty especially in the areas of pythonic practices,
feel free to contribute improvements and share thoughts.

* Pass SIGTERM, SIGKILL through to dyno

* Flow control using SIGCONT/SIGSTOP

* Max timeout
  Kill the event chain after X minutes

* Brute force attacks - Limit connections by user/IP

* Locking - only one concurrent commit per repository


## License

`gitmouth` and other `openruko` components are licensed under MIT.
[http://opensource.org/licenses/mit-license.php](http://opensource.org/licenses/mit-license.php)


## Authors and Credits

Matt Freeman
[email me - im looking for some remote work](mailto:matt@nonuby.com)
[follow me on twitter](http://www.twitter.com/nonuby )
