
#   Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
from setuptools import setup, find_packages

__version__ = '0.1.dev1'

with io.open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='epann',
    version=__version__,
    author='World_Editors',
    author_email='',
    description=('EPANN: Evolving Plastic Artificial Networks for General Intelligence'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/WorldEditors/EvolvingPRNN',
    license="GPLv3",
    packages=[package for package in find_packages()
              if package.startswith('epann')],
    package_data={'epann': []
    },
    tests_require=['pytest', 'mock'],
    include_package_data=True,
    install_requires=[
        'gym>=0.18.0',
        'numpy>=1.16.4',
        'Pillow>=6.2.2',
        'six>=1.12.0',
        'metagym>0.1.0',
        'parl>=1.4.1'
    ],
    extras_require={},
    zip_safe=False,
)

