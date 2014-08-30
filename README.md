[![Travis build status](https://travis-ci.org/shirkey/members.png?branch=develop)](https://travis-ci.org/shirkey/members)
User Map
========

A simple application for creating user community maps powered by Flask.

Installation
------------

Prerequisites:

* Python 2.7.x
* PostgreSQL or MySQL database
* pip and (optional) virtualenv

Once you have all prerequisites, the following steps will bootstrap the project:

1.  Grab the source code.

        git clone git://github.com/id-python/members.git
        cd members

2.  Activate your virtual environment (or you can skip this step if you're not using `virtualenv`).

3.  Install all dependencies using `pip`:

        pip install -r requirements.txt

Note: the installation process may take awhile.

Development
-----------

By default, this app reads configuration from `users/default_config.py`.
To override values set in default config, simply copy the contents
of `users/default_config.py` and save it elsewhere.

    cp users/default_config.py /path/to/custom/config.py

Then edit the custom config file, setting appropriate values as needed.

Things you might need to override:

*   `SQLALCHEMY_DATABASE_URI`

    Since this project tested using PostgreSQL and __likely__ will running on MySQL as well,
    there's extra package you need to install to before running the app.

    * `pip install psycopg2` for PostgreSQL
    * `pip install mysql-python` for MySQL

    Just pick one and please refer to http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html for details.

Ensure your database schema is up-to-date by invoking this command:

    USERS_CONFIG=/path/to/custom/config.py python manage.py db upgrade

Running the app will be as simple as:

    USERS_CONFIG=/path/to/custom/config.py python manage.py runserver

Each config item is overridable through environment variable.
For instance, if you want to suppress email delivery, simply set appropriate value:

    USERS_CONFIG=/path/to/custom/config.py USERS_MAIL_SUPPRESS_SEND=1 python manage.py runserver

Testing
-------

NOTE: It is highly-recommended that you're creating a separate database and config file for testing.

To run testcases:

    USERS_CONFIG=/path/to/custom/testing_config.py ./runtests.sh

Each config item is overridable through environment variable.
For instance, if you want to suppress email delivery, simply set appropriate value:

    USERS_CONFIG=/path/to/custom/testing_config.py USERS_MAIL_SUPPRESS_SEND=1 ./runtests.sh

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
