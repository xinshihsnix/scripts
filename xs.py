#!/usr/bin/python
# -*- coding: utf8 -*-
"""
IT IS JUST A NOTE BOOK
"""
import sys
import os
import time


argvs = sys.argv

option = argvs[1]

content = argvs[2] if len(argvs) > 2 else ''

note_path = '/home/xinshi/projects/github/scripts/xs.note.log'
reminder_path = '/var/log/xinshi/reminder.log'

def handle_insert():
    cmd = "echo '{0}' >> {1}".format(content, note_path)
    os.system(cmd)

    os.system("echo '{0}' >> {1}".format('-----', note_path))


def handle_select():
    os.system("less {0}".format(note_path))


# def handle_insert_from_clipboard():
def handle_insert_reminder():
    cmd = "echo '{0}' >> {1}".format(content, reminder_path)
    os.system(cmd)

def handle_show_reminder():
    os.system("less {0}".format(reminder_path))

def handle_insert_ling_pwd():
    from Crypto.Cipher import AES
    from settings import AES_PWD, MY_PWD_FILE_PATH
    d = AES.new(AES_PWD)

    c = content + 'fgf'    # 设置分隔符号(fgf)
    x_content = c + (16 - len(c)%16)*'u'    # 被加密字符串要是16的倍数，所以不够的用u填充
    print x_content
    encrypted_content = d.encrypt(x_content)

    f = open(MY_PWD_FILE_PATH, 'a')
    f.write(encrypted_content)
    f.close()

def handle_select_ling_pwd():
    from Crypto.Cipher import AES
    from settings import AES_PWD, MY_PWD_FILE_PATH
    d = AES.new(AES_PWD)

    f = open(MY_PWD_FILE_PATH)
    content = f.read()

    decrypted_content = d.decrypt(content)
    de_list = decrypted_content.split('fgf')
    for x in de_list:
        print x
    f.close()


def handle_help():
    print '--- IT IS JUST A NOTE BOOK! ---'
    for i in options:
        print i.get('option'), ': ', i.get('help_text')

options = [
    {
        'option': 'i',
        'help_text': 'insert',
        'function': handle_insert,
    },
    {
        'option': 's',
        'help_text': 'select',
        'function': handle_select,
    },
    {
        'option': 'rs',
        'help_text': 'reminder select',
        'function': handle_show_reminder,
    },
    {
        'option': 'ri',
        'help_text': 'reminder insert',
        'function': handle_insert_reminder,
    },

    {
        'option': 'li',
        'help_text': 'ling insert pwd',
        'function': handle_insert_ling_pwd,
    },
    {
        'option': 'ls',
        'help_text': 'ling select pwd',
        'function': handle_select_ling_pwd,
    },

    {
        'option': '--help',
        'help_text': 'help',
        'function': handle_help,
    },
]


if __name__ == '__main__':
    for op in options:
        if option == op.get('option'):
            op.get('function')()
