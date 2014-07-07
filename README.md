User Map
========

A simple application for creating user community maps powered by Flask.

Hacking
-------

By default, this app reads configuration from `users/default_config.py`.
To override values set in default config, simply copy the contents
of `users/default_config.py` and save it elsewhere.

    cp users/default_config.py /path/to/custom/config.py

Then edit the custom config file, setting appropriate values as needed.

Things you might need to override:

* `SQLALCHEMY_DATABASE_URI` — refer to http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html for details

To install dependencies:

    pip install -r requirements.txt

Before running the server/testcase, ensure database is up-to-date:

    USERS_CONFIG=/path/to/custom/config.py python manage.py db upgrade

To run the development server:

    USERS_CONFIG=/path/to/custom/config.py python manage.py runserver

Each config item is overridable through environment variable.
For instance, if you want to suppress email delivery, simply set appropriate value:

    USERS_CONFIG=/path/to/custom/config.py USERS_MAIL_SUPPRESS_SEND=True python manage.py runserver

To run testcases:

    USERS_CONFIG=/path/to/custom/config.py USERS_MAIL_SUPPRESS_SEND=True ./runtests.sh

Collaboration
-------------

1. Fork this repo.
2. Create a topic branch in your forked repo and start hacking.
3. Run `runtests.sh`. Ensure all tests passed.
4. Once it done, submit your pull request (PR) against upstream `develop` branch.
5. Our maintainers will review your PR. If it's good — all tests passed and proposed feature is in our roadmap — your PR will be merged.

Authors
-------

Tim Sutton and Akbar Gumbira
