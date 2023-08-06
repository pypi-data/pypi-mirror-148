    #!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='lhy-utils',
    version='0.1.14',
    author='lhy',
    url='https://github.com/lhy2749/lhy-utils',
    author_email='379970083@qq.com',
    description=u'工具箱',
    packages=['lhy_utils'],
    install_requires=[
        'DaPy==1.16.1',
        'pynvml==11.4.1',
        'numpy==1.18.5',
        'xlsxwriter==3.0.3'
    ]
)