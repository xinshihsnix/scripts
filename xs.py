#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
from db_service import xsite_dbs

# print sys.argv

argvs = [a.lower() for a in sys.argv]   # 忽略大小写

option = argvs[1]

title = argvs[2] if len(argvs) > 2 else ''

content = argvs[3] if len(argvs) > 3 else ''


def handle_add():
    pass


def handle_s():
    pass


def handle_sa():
    _sql = 'select * from reminder_reminder'
    xsite_dbs.cursor.execute(_sql)
    rows = xsite_dbs.cursor.fetchall()

    for r in rows:
        print r[2], ' ------ ',r[3]

    xsite_dbs.close()

options = [
    {
        'option': 'add',
        'help_text': '',
        'function': handle_add,
    },
    {
        'option': 's',
        'help_text': 'select',
        'function': handle_s,
    },
    {
        'option': 'sa',
        'help_text': 'select all',
        'function': handle_sa,
    }
]


if __name__ == '__main__':
    for op in options:
        if option == op.get('option'):
            op.get('function')()
