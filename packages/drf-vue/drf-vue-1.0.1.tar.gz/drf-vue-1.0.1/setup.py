#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import shutil
import sys
from io import open

from setuptools import find_packages, setup


def read(f):
    return open(f, 'r', encoding='utf-8').read()


version = '1.0.1'

if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('drf-vue.egg-info')
    sys.exit()

setup(
    name='drf-vue',
    version='1.0.1',
    url='https://github.com/blackjackgg/drf-vue',
    license='BSD',
    description=' 自动生成前端vue模板的 drf插件',
    long_description=read('README.MD'),
    long_description_content_type='text/markdown',
    keywords="djangorestframework drf history drf vue generator ",
    author=' blackjack0v0',
    author_email='yihongwy1@163.com',  # SEE NOTE BELOW (*)
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=['jinja2', 'uuid', 'requests'],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ]
)

# (*) Please direct queries to the discussion group, rather than to me directly
#     Doing so helps ensure your question is helpful to other users.
#     Queries directly to my email are likely to receive a canned response.
#
#     Many thanks for your understanding.
