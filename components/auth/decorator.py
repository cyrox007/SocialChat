import functools
from flask import redirect, url_for, session
from database import Database

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if session.get('login') is None:
            return redirect(url_for('login'))
        
        return view(*args, **kwargs)

    return wrapped_view


""" def connection_db(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if session.get('login') is None:
            return redirect(url_for('login'))

        return view(*args, **kwargs)

    return wrapped_view """