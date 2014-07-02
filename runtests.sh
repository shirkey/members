#!/usr/bin/env bash
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
fi

nosetests -v --with-id  users

if [ ! -z $(command -v deactivate) ]; then
    deactivate
fi
