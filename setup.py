#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements
from glob import glob

REQUIREMENTS = [str(ir.req) for ir in parse_requirements(
    'requirements.txt',  session=False)]
#REQUIREMENTS_TEST = [str(ir.req) for ir in parse_requirements('requirements-test.txt',  session=False)]

setup(
    name='datasploit',
    version='0.1.0',
    description='OSINT Framework for helping the investigation',

    author='Shubham Mittal, Sudhanshu Chauhan, Kunal Aggarwal, Javier Gutiérrez',
    author_email='nexus.megavexus@gmail.com',

    url='https://github.com/megavexus/datasploit',

    install_requires=REQUIREMENTS,

    packages=find_packages(where='src'),
    include_package_data=True,
    package_dir={'': 'src'},
    zip_safe=False,
    #data_files=[('requs', glob('*.txt'), glob('*.html'))],

    # CLI
    entry_points= {
        'console_scripts':[
            'datasploit=datasploit.datasploit:main'
        ]
    }
    
    # Testing
    #setup_requires=["pytest-runner"],
    #tests_require=REQUIREMENTS_TEST,
)
