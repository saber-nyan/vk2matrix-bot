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
    dependency_links=[
        "https://github.com/MaT1g3R/matrix-python-sdk/archive/52207cdc25d797295dbf795db41e9eb189bc2d82.zip"
        "#egg=matrix_client-0.0.6.git+52207cd",
    ],
    install_requires=[
        'vk_api',
        'requests',
        'aiohttp',
        'matrix_client==0.0.6.git+52207cd',
    ],
    packages=find_packages(),
    include_package_data=True
)
