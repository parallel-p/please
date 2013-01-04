# -*- coding: utf8 -*-

import sys
from distutils import log as log
from distutils.core import Command
import os


import please
import please.utils
from please.executors.compiler import compile
from please.utils.form_error_output import form_err_string_by_std
from please.utils.exceptions import PleaseException
import please.log

path = os.path.join(os.path.dirname(please.__file__), 'checkers')
for file in os.listdir(path):
    res,fout, err = None, None, None
    if os.path.splitext(file)[1] == '.cpp':
        res, fout, err = compile(os.path.join(path, file))
        if res.verdict != 'OK':
            print(form_err_string_by_std(fout, err))

import distribute_setup
# Ставим дистрибьют правильной версии
# Installation of the up to date distribution
distribute_setup.use_setuptools(version="0.6.19")

from setuptools import setup, find_packages

# Папки, не содержащие код
# Folders without
package_data = {
    'please': ['templates/*.*', 'checkers/*.*'],
    'please.exporter': ['templates/*.*'],
    'please.language': ['mime.types'],
}


entry_points = {
    'console_scripts' : ['please = please.launcher:main']
}

# python-библиотеки, обязательные к установке.
# python-modules obligatory for installation
# Можно указывать версию. Больше информации можно найти здесь:
# You can specify the current version. For more information:
# http://packages.python.org/distribute/setuptools.html#id12
# Если инсталлятор не находит правильной версии библиотеки, то
# нужно прописать в dependency_links либо прямую ссылку на дистрибутив, либо
# ссылку на страницу, где перечислены варианты дистрибутивов этой библиотеки
# со ссылками - он сам повыдёргивает, откуда скачать.
install_requires = [
    'psutil',
    'colorama',
    'HTML.py ==0.04',
]

dependency_links = [
    'http://please.googlecode.com/svn/third_party/HTML.py-0.04-py3.2.egg',
    'http://www.decalage.info/files/',
    'http://pypi.python.org/pypi/colorama',
    'http://please.googlecode.com/svn/third_party/psutil-0.3.0.tar.gz',
    'http://please.googlecode.com/svn/third_party/windows/psutil-0.3.0.win32-py3.2.exe', #psutil for win32
    'http://please.googlecode.com/svn/third_party/windows/HTML.py-0.04-py3.2.egg', #html for win32
    'http://please.googlecode.com/svn/third_party/windows/psutil-0.3.0.win-amd64-py3.2.exe', # psutil for amd64
]

# python-библиотеки, необходимые для разработчика.
# Формат аналогичен предыдущему пункту.
# dependency_links с предыдущим пунктом общие.
develop_requires = [
    #'coverage',
    'mox',
]

extras_require = {
    'develop' : develop_requires
}

try:
    from setup_extensions.develop import develop
except ImportError as e:
    print('Error while importing develop extension: %s' % (str(e)))
setup_params = {
    'name'             : 'Please',
    'version'          : '0.3',
    'description'      : '***',
    'package_dir'      : {'please': 'please'},
    'packages'         : ['please.' + x for x in find_packages('please')] + ['please'],
    'package_data'     : package_data,
    'install_requires' : install_requires,
    'extras_require'   : extras_require,
    'dependency_links' : dependency_links,
    'entry_points'     : entry_points,
    'cmdclass'         : {'develop' : develop},
}

setup(**setup_params)


import platform
system = platform.system()[0]
if (system == 'W'):
    log.info("\nChecking Path variable...")
    from distutils import sysconfig as conf
    path = os.getenv('path').replace('"', '').split(';')
    log.info("Path: %s", os.getenv('path'))
    pp = os.path.join(conf.PREFIX, 'scripts')
    if (not (pp in path or (pp + os.sep) in path)):
        req = 'echo Y | reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH /t REG_SZ /d "%s;%s"' % (os.getenv('path'), pp)
        log.info('calling ' + req)
        os.system(req)
        log.info('Added %s to path', pp)
        log.info('\nTo apply changes, after the installation, please reboot the computer.')


log.info('\nInstallation finished!')
