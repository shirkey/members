[![Stories in Ready](https://badge.waffle.io/timlinux/user_map.png?label=ready)](https://waffle.io/timlinux/user_map)
[![Build Status](http://jenkins.linfiniti.com/buildStatus/icon?job=UserMap)](http://jenkins.linfiniti.com/job/UserMap/)

User Map
========

A simple flask application for creating user community maps.

By default, this app reads configuration from `users/config.py`.
To override values set in default config, simply copy the contents
of `users/config.py` and save it elsewhere.

    cp users/config.py /path/to/custom/config.py

Then edit the custom config file, setting appropriate values as needed.

To run in debug mode (which will also serve up static content),
use the `-d` flag:

    USERS_CONFIG=/path/to/custom/config.py python runserver.py -d

Each config item is overridable through environment variable.
For instance, if you want to suppress email delivery,
simply set appropriate value:

    USERS_MAIL_SUPPRESS_SEND=True python runserver

To run testcases:

    USERS_CONFIG=/path/to/custom/config.py MAIL_SUPPRESS_SEND=True ./runtests.sh

Collaboration
-------------

1. Fork this repo.
2. Create a topic branch in your forked repo and start hacking.
3. Run `runtests.sh`. Ensure all tests passed.
4. Once it done, submit your pull request (PR) against upstream `develop` branch.
5. Our maintainers will review your PR. If it's good — all tests passed and proposed feature is in our roadmap — your PR will be merged.

Deployment using Docker
-----------------------

If you are using docker, you can create a Docker image for this app easily as
follows:

```
wget -O Dockerfile https://raw.github.com/timlinux/user_map/master/docker/Dockerfile
wget -O sources.list https://raw.github.com/timlinux/user_map/master/docker/sources.list
wget -O post-setup.sh https://raw.github.com/timlinux/user_map/master/docker/post-setup.sh
chmod +x post-setup.sh

docker build -t linfiniti/user_map:base .
docker run -d -p 8099:80 -t linfiniti/user_map:base -n user_map -D
```

If you are on a Hetzner server, consider replacing the second line above with:

```
wget -O sources.list https://raw.github.com/timlinux/user_map/master/docker/hetzner-sources.list
```

Authors
-------

Tim Sutton and Akbar Gumbira
