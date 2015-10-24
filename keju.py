# coding: utf8
import os
import commands
import subprocess

hint_format = '------{0}------'


def print_hint(hint, result):
    print hint_format.format(hint)
    print result
    print hint_format.format('end')

# ---------------------------------------------------
wt_path = u'/home/xinshi/projects/wt-html最新版'

css_source_path = '/home/xinshi/projects/wt-html最新版/css/red.css'
css_to_path = '/home/xinshi/projects/KeJu/wechat/static/wechat/css/red.css'

images_source_path = '/home/xinshi/projects/wt-html最新版/images/'
images_to_path = '/home/xinshi/projects/KeJu/wechat/static/wechat/images/'

os.chdir(wt_path)

# ----------------------------------------------------
(status, output) = commands.getstatusoutput('svn up')
print_hint('svn up', output)

cp_css_command = "cp {0} {1}".format(css_source_path, css_to_path)
s = subprocess.Popen(cp_css_command, shell=True, stdout=subprocess.PIPE)
(stdoutdata, stderrdata) =  s.communicate()
print_hint(cp_css_command, stdoutdata)

cp_images_command = 'cp -R {0} {1}'.format(images_source_path, images_to_path)
s = subprocess.Popen(cp_images_command, shell=True, stdout=subprocess.PIPE)
(stdoutdata, stderrdata) =  s.communicate()
print_hint(cp_images_command, stdoutdata)
