#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
import os
import commands
import subprocess
import re
import pexpect
import pxssh
import time

from settings import *

argvs = sys.argv

option = argvs[1]

hint_format = u'++++++++++++ {0} +++++++++++'


def print_hint(hint, result):
    print hint_format.format(hint)
    print result
    print hint_format.format('---- end ----')


def run_command_and_show_result(cmd):
    s = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    (stdoutdata, stderrdata) =  s.communicate()
    print_hint(cmd, stdoutdata)


def handle_hq():
    os.chdir(WT_PATH)

    svn_cmd = 'svn up'
    run_command_and_show_result(svn_cmd)

    cp_css_command = u"cp {0} {1}".format(CSS_SOURCE_PATH, CSS_TO_PATH)
    run_command_and_show_result(cp_css_command)

    cp_images_command = u'cp -R {0} {1}'.format(IMAGES_SOURCE_PATH, IMAGES_TO_PATH)
    run_command_and_show_result(cp_images_command)


def handle_git_pull():
    os.chdir(GIT_KEJU_PATH)

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


def handle_git_push():
    os.chdir(GIT_KEJU_PATH)

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


def handle_git_commit(commit_notes):
    os.chdir(GIT_KEJU_PATH)

    git_add_A = 'git add *.css *.png *.jpg *.html *.py'
    run_command_and_show_result(git_add_A)

    git_status = 'git status'
    s = subprocess.Popen(git_status, shell=True, stdout=subprocess.PIPE)
    (stdoutdata, stderrdata) = s.communicate()
    print_hint(git_status, stdoutdata)

    out_s_list = re.split('\s+', stdoutdata)
    commit_path_list = []

    for o in out_s_list:
        if os.path.exists(o):
            commit_path_list.append(o)

    for e in GIT_COMMIT_EXCLUDE_FILES:      # pop settings & auth debug
        if e in commit_path_list:
            commit_path_list.remove(e)

    commit_cmd = 'git commit'
    for p in commit_path_list:
        commit_cmd += '  %s'%p

    if not commit_notes:
        commit_notes = argvs[2]
    commit_cmd += "  -m'%s' "%commit_notes
    print '!!!!!!!!!! you will execute this command! !!!!!!!!!!!'
    print commit_cmd
    print '?????????? y/yes? ??????????'

    i = raw_input()
    if i.lower() == 'y':
        run_command_and_show_result(commit_cmd)

    run_command_and_show_result(git_status)


# def handle_test_git_pull():
#     cd_keju = 'cd /var/www/KeJu'
#
#     try:
#         # 调用构造函数，创建一个 pxssh 类的对象.
#         s = pxssh.pxssh()
#         s.login (TEST_SERVER_IP, TEST_SERVER_USERNAME, TEST_SERVER_PASSWORD, login_timeout=200)
#
#         s.sendline(cd_keju)
#         s.prompt()
#
#         s.sendline('git pull')
#         s.prompt()       # match the prompt
#         print s.before      # print everything before the propt.
#         s.logout()
#     except pxssh.ExceptionPxssh, e:
#         print "pxssh failed on login."
#         print str(e)


def handle_git_yitiaolong():
    print 'git pull??'
    print 'press enter to continue'
    i = raw_input()
    if not i:
        handle_git_pull()

    commit_notes = argvs[2]
    handle_git_commit(commit_notes)

    print 'git push??'
    print 'press enter to continue'
    i = raw_input()
    if not i:
        handle_git_push()


def handle_test_connect():
    os.chdir('/usr/src/my-script/shell_script')
    connect_cmd = './keju_new_test_server_terminal.sh'

    os.system(connect_cmd)


def handle_product_connect():
    os.chdir('/usr/src/my-script/shell_script')
    connect_cmd = './keju_new_product_server_terminal.sh'

    os.system(connect_cmd)


def handle_note():
    os.system("less {0}".format(KEJU_NOTE_PATH))


def handle_breakfast():
    os.system('gnome-terminal --title="test server" --command="ke tc" --geometry=120x30+150+200')
    os.system('gnome-terminal --title="product server" --command="ke pc" --geometry=120x20+0+0')

    os.system('charm & >> /dev/null')
    for t in TAB_SITES:
        os.system("firefox --new-tab {0} & >> /dev/null".format(t))
        time.sleep(6)
    os.system("python /home/xinshi/projects/KeJu/manage.py runserver 0.0.0.0:7777")


def handle_note_insert():
    content = argvs[2]
    cmd = "echo '{0}' >> {1}".format(content, KEJU_NOTE_PATH)
    os.system(cmd)

    cmd = "echo '{0}' >> {1}".format('', KEJU_NOTE_PATH)
    os.system(cmd)

def handle_product_mysql():
    cmd = "mysql -h {0} -u {1} -p{2}".format(MYSQL_PRODUCT_IP, MYSQL_PRODUCT_USERNAME, MYSQL_PRODUCT_PASSWORD)
    os.system(cmd)


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
        'help_text': 'git status&commit [param 1: 备注]',
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
        'help_text': 'git yitiaolong [param 1: 备注]',
        'function': handle_git_yitiaolong,
    },
    {
        'option': 'note',
        'help_text': 'less note',
        'function': handle_note,
    },
    {
        'option': 'tc',
        'help_text': 'test server connect',
        'function': handle_test_connect,
    },
    {
        'option': 'pc',
        'help_text': 'product server connect',
        'function': handle_product_connect,
    },
    {
        'option': 'bf',
        'help_text': 'breakfast',
        'function': handle_breakfast,
    },
    {
        'option': 'ni',
        'help_text': 'note insert',
        'function': handle_note_insert,
    },
    {
        'option': 'pm',
        'help_text': 'product mysql connect',
        'function': handle_product_mysql,
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



