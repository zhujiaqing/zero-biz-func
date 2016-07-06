#!/usr/bin/env python
# -*- coding:utf8 -*-

__author__ = 'jesse'

import web
import time
from test import test_session

web.config.debug = False

urls = (
    "/count", "count",
    "/reset", "reset",
    "/sub", test_session.app
)

app = web.application(urls, locals())

web.config.session_parameters['cookie_name'] = 'jsid'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 100,  # 24 * 60 * 60, # 24 hours   in seconds
web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = True
web.config.session_parameters['secret_key'] = 'fLjUfxqXtfNoIldA0A0J'
web.config.session_parameters['expired_message'] = 'Session expired'

db = web.database(dbn='sqlite', db='/tmp/s-%s.db' % int(time.time()))
db.query('''
 create table sessions (
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data text
);
''')
store = web.session.DBStore(db, 'sessions')

# store = web.session.DiskStore('/tmp/s-%s' % int(time.time()))
session = web.session.Session(app, store, initializer={'count': 100, 'info': 'js'})


def session_hook():
    web.ctx.session = session


app.add_processor(web.loadhook(session_hook))


class count:
    def GET(self):
        session.count += 1
        return str(session.count)


class reset:
    def GET(self):
        session.kill()
        return ""


if __name__ == "__main__":
    app.run()
