#  Copyright (c) 2015 SONATA-NFV, 5GTANGO, UBIWHERE, QUOBIS SL.
# ALL RIGHTS RESERVED.
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
#
# Neither the name of the SONATA-NFV, 5GTANGO, UBIWHERE, QUOBIS SL.
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has been performed in the framework of the SONATA project,
# funded by the European Commission under Grant number 671517 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.sonata-nfv.eu).
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.5gtango.eu).

from setuptools import setup, find_packages
import os.path as path

cwd = path.dirname(__file__)
with open(path.join(cwd, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

longdesc = """
Component to validate 5GTANGO SDK projects, services, and
functions.
"""

setup(name='tngsdk.validate',
      license='Apache License, Version 2.0',
      version='0.1',
      url='https://github.com/sonata-nfv/tng-sdk-validation',
      author='Ana Pol',
      author_email='ana.pol@quobis.com',
      long_description=longdesc,
      package_dir={'': 'src'},
      packages=find_packages('src'),  # dependency resolution
      namespace_packages=['tngsdk', ],
      package_data={
            'tngsdk': ['validation/eventcfg.yml']
        },
      include_package_data=True,
      install_requires=requirements,
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'tng-sdk-validate=tngsdk.validation:main',
              'tng-validate=tngsdk.validation:main',
              'tng-vld=tngsdk.validation:main'
          ],
      },
      test_suite='tngsdk',
      setup_requires=[],
      tests_require=['pytest'])
