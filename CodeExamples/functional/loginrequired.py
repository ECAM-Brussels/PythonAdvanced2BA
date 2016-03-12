#!/usr/bin/env python3
# loginrequired.py
# author: Sébastien Combéfis
# version: March 12, 2016

from bottle import route, redirect, run

user = None

def login_required(f):
    def wrapper(*args):
        if user == None:
            redirect('/login')
        return f(*args)
    return wrapper

@route('/myaccount')
@login_required
def myaccount():
    return 'OK...'

run(host='localhost', port=8080)