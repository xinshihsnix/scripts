#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
import os
import commands
import subprocess
import re
import pexpect

from settings import GIT_USERNAME, GIT_PASSWORD

# -------------------------
wt_path = u'/home/xinshi/projects/wt-html最新版'

css_source_path = '/home/xinshi/projects/wt-html最新版/css/red.css'
css_to_path = '/home/xinshi/projects/KeJu/wechat/static/wechat/css/red.css'

images_source_path = '/home/xinshi/projects/wt-html最新版/images/*'
images_to_path = '/home/xinshi/projects/KeJu/wechat/static/wechat/images/'

git_keju_path = '/home/xinshi/projects/KeJu'

git_commit_exclude_files = ['KeJu/settings.py', 'common/decorator/auth.py']
# -------------------------

argvs = [a.lower() for a in sys.argv]   # 忽略大小写

option = argvs[1]

hint_format = '++++++++++++ {0} +++++++++++'


def print_hint(hint, result):
    print hint_format.format(hint)
    print result
    print hint_format.format('---- end ----')


def run_command_and_show_result(cmd):
    s = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    (stdoutdata, stderrdata) =  s.communicate()
    print_hint(cmd, stdoutdata)


def handle_hq():
    os.chdir(wt_path)

    svn_cmd = 'svn up'
    run_command_and_show_result(svn_cmd)

    cp_css_command = "cp {0} {1}".format(css_source_path, css_to_path)
    run_command_and_show_result(cp_css_command)

    cp_images_command = 'cp -R {0} {1}'.format(images_source_path, images_to_path)
    run_command_and_show_result(cp_images_command)


def handle_git_pull():
    print_hint('git pull start')
    os.chdir(git_keju_path)

    pull_cmd = 'git pull'
    child = pexpect.spawn(pull_cmd)

    index = child.expect(["(?i)Username for"])   # 期望具有提示输入用户名的字符出现
    if index == 0:
        child.sendline(GIT_USERNAME)    # 发送登录用户名 + 换行符给子程序.
        index = child.expect(["(?i)Password for", "(?i)Authentication failed"])
        if index == 0:
            child.sendline(GIT_PASSWORD)   # 匹配到了密码提示符，发送密码 + 换行符给子程序.
        elif index == 1:
            print 'Authentication failed'
    else:
        print 'not Username'

    print_hint(pull_cmd + ' result', child.read())      # 打印执行结果
    child.close(force=True)

    print_hint(' end ')


def handle_git_push():
    print_hint('git push start')
    os.chdir(git_keju_path)

    push_cmd = 'git push'
    child = pexpect.spawn(push_cmd)

    index = child.expect(["(?i)Username for"])   # 期望具有提示输入用户名的字符出现
    if index == 0:
        child.sendline(GIT_USERNAME)    # 发送登录用户名 + 换行符给子程序.
        index = child.expect(["(?i)Password for", "(?i)Authentication failed"])
        if index == 0:
            child.sendline(GIT_PASSWORD)   # 匹配到了密码提示符，发送密码 + 换行符给子程序.
        elif index == 1:
            print 'Authentication failed'
    else:
        print 'not Username'

    print_hint(push_cmd + ' result', child.read())      # 打印执行结果
    child.close(force=True)

    print_hint(' end ')


def handle_git_commit():
    os.chdir(git_keju_path)

    git_add_A = 'git add *.css *.png *.jpg'
    run_command_and_show_result(git_add_A)

    git_status = 'git status'
    s = subprocess.Popen(git_status, shell=True, stdout=subprocess.PIPE)
    (stdoutdata, stderrdata) =  s.communicate()
    print_hint(git_status, stdoutdata)

    out_s_list = re.split('\s+', stdoutdata)
    commit_path_list = []

    for o in out_s_list:
        if os.path.exists(o):
            commit_path_list.append(o)

    for e in git_commit_exclude_files:      # pop settings & auth debug
        if e in commit_path_list:
            commit_path_list.remove(e)

    commit_cmd = 'git commit'
    for p in commit_path_list:
        commit_cmd += '  %s'%p

    commit_notes = argvs[2]
    commit_cmd += "  -m'%s' "%commit_notes
    print '!!!!!!!!!! you will execute this command! !!!!!!!!!!!'
    print commit_cmd
    print '?????????? y/yes? ??????????'

    i = raw_input()
    if i.lower() == 'y':
        run_command_and_show_result(commit_cmd)

    run_command_and_show_result(git_status)


def handle_git_yitiaolong():
    print 'git pull??'
    i = raw_input()
    if i.lower() == 'y':
        handle_git_pull()

    print 'git commit??'
    i = raw_input()
    if i.lower() == 'y':
        handle_git_commit()

    print 'git push??'
    i = raw_input()
    if i.lower() == 'y':
        handle_git_push()


def handle_help():
    for o in options:
        print o.get('option'), ':', o.get('help_text')

options = [
    {
        'option': 'hq',
        'help_text': 'hong qin',
        'function': handle_hq,
    },
    {
        'option': 'gc',
        'help_text': 'git status&commit',
        'function': handle_git_commit,
    },
    {
        'option': 'gpl',
        'help_text': 'git pull',
        'function': handle_git_pull,
    },
    {
        'option': 'gph',
        'help_text': 'git push',
        'function': handle_git_push,
    },
    {
        'option': 'gytl',
        'help_text': 'git yitiaolong',
        'function': handle_git_yitiaolong,
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



