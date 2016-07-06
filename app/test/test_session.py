#!/usr/bin/env python
# -*- coding:utf8 -*-

__author__ = 'jesse'

import web
import time

urls = (
    "/.*", "default",
)

app = web.application(urls, locals())


class default:
    def GET(self):
        print web.ctx.session.count, web.ctx.session.info, web.ctx.session.get('test', 'none')
        web.ctx.session.count += 1
        web.ctx.session['info'] = time.strftime('%H:%M:%S')
        web.ctx.session['test'] = 'jesse'
        return "test default"
