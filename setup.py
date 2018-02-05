# -*- coding: utf-8 -*-
"""
Наш кривой скрипт установки.
"""
from distutils.core import setup

from setuptools import find_packages

with open('README.md', mode='r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='vk2matrix-bot',
    version='0.0.0.1',
    description='Converts VKontakte links to text in the Matrix room.',
    long_description=readme,
    author='saber-nyan',
    author_email='saber-nyan@ya.ru',
    url='https://github.com/saber-nyan/vk2matrix-bot',
    license='WTFPL',
    install_requires=[
        'vk_api',
        'matrix_bot_api',
        'requests',
    ],
    packages=find_packages(),
    include_package_data=True
)
