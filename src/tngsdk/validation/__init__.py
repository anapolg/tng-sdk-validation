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

import logging
import coloredlogs
import os

from tngsdk.validation.cli import parse_args, CLI
from tngsdk.validation.validator import Validator

LOG = logging.getLogger(os.path.basename(__file__))


def logging_setup():
    os.environ["COLOREDLOGS_LOG_FORMAT"] \
        = "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"

def validateFile(args): 
    if not os.path.isfile(args.package_file):
        LOG.error("Provided package is not a valid file")
        exit(1)
    return

def setValidationType(v, args):
    if args.integrity:
        v._topology = False
          
    elif args.syntax:
        v._integrity = False
        v._topology = False
    return v

def main():
    logging_setup()
    args = parse_args()

    # TODO better log configuration (e.g. file-based logging)
    if args.verbose:
        coloredlogs.install(level="DEBUG")
    else:
        coloredlogs.install(level="INFO")

    # TODO validate if args combination makes any sense

    # TODO validate params introduced

    # Validate params for package_file validation
    if args.package_file:
        validateFile(args)
        
    # Validate params for project validation
    elif args.project_path:
        pass

    # Validate params for service validation
    elif args.nsd:
        # Check the existance of dpath and dext at some moment
        pass

    # Validate params for function validation
    elif args.vnfd:
        pass

    else:
        LOG.error("Invalid arguments.")
        exit(1)

    v = Validator()

    v = setValidationType(v, args)
               
    if args.api:
        # TODO start package in service mode
        LOG.warning("Running rest api")
        pass
    else:
        # Run package in CLI mode
        c = CLI(args, v)
        c.dispatch()
