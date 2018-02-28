#  Copyright (c) 2015 SONATA-NFV, 5GTANGO, UBIWHERE, QUOBIS SL.
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
import argparse
import os
import sys

from os.path import expanduser

LOG = logging.getLogger(os.path.basename(__file__))

DEFAULT_WORKSPACE_DIR = os.path.join(expanduser("~"), "tng-workspace")

class CLI(object):

    def __init__(self, args, validator):
        self._args = args
        self._v = validator

    def dispatch(self):
        # Validate package_file
        if self._args.package_file:
            result = self._v.validate_package(self._args.package_file)
            # self._v.print_result(validator, result)

        # Validate project
        elif self._args.project_path:
            result = self._v.validate_project(self._args.project_path)
            # self._v.print_result(validator, result)

        # Validate service
        elif self._args.nsd:
            # Check the existance of dpath and dext at some moment
            pass

        # Validate function
        elif self._args.vnfd:
            pass

def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description="5GTANGO SDK validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Example usage:
        tng-validate --project /home/sonata/projects/project_X
                     --workspace /home/sonata/.son-workspace
        tng-validate --service ./nsd_file.yml --path ./vnfds/ --dext yml
        tng-validate --function ./vnfd_file.yml
        tng-validate --function ./vnfds/ --dext yml
        """)

    exclusive_parser = parser.add_mutually_exclusive_group(
        required=True
    )

    parser.add_argument(
        "-w", "--workspace",
        # help="Specify the directory of the SDK workspace for validating the SDK project.",
        help="Specify the directory of the SDK workspace for validating the "
             "SDK project. If not specified will assume the directory: '{}'"
             .format(DEFAULT_WORKSPACE_DIR),
        dest="workspace_path",
        required=False,
        default=None
    )

    exclusive_parser.add_argument(
        "--project",
        # help="Validate the service of the specified SDK project.",
        help="Validate the service of the specified SDK project. If "
             "not specified will assume the current directory: '{}'\n"
             .format(os.getcwd()),
        dest="project_path",
        required=False,
        default=None
    )
    exclusive_parser.add_argument(
        "--package",
        help="Validate the specified package descriptor.",
        dest="package_file",
        required=False,
        default=None
    )
    exclusive_parser.add_argument(
        "--service",
        help="Validate the specified service descriptor. "
             "The directory of descriptors referenced in the service "
             "descriptor should be specified using the argument '--path'.",
        dest="nsd",
        required=False,
        default=None
    )
    exclusive_parser.add_argument(
        "--function",
        help="Validate the specified function descriptor. If a directory is "
             "specified, it will search for descriptor files with extension "
             "defined in '--dext'",
        dest="vnfd",
        required=False,
        default=None
    )
    parser.add_argument(
        "--dpath",
        help="Specify a directory to search for descriptors. Particularly "
             "useful when using the '--service' argument.",
        required=False,
        default=None
    )
    parser.add_argument(
        "--dext",
        help="Specify the extension of descriptor files. Particularly "
             "useful when using the '--function' argument",
        required=False,
        default=None
    )
    parser.add_argument(
        "--syntax", "-s",
        help="Perform a syntax validation.",
        action="store_true",
        required=False,
        default=False
    )
    parser.add_argument(
        "--integrity", "-i",
        help="Perform an integrity validation.",
        action="store_true",
        required=False,
        default=False
    )
    parser.add_argument(
        "--topology", "-t",
        help="Perform a network topology validation.",
        action="store_true",
        required=False,
        default=False
    )
    parser.add_argument(
        "--debug",
        help="Sets verbosity level to debug",
        dest="verbose",
        action="store_true",
        required=False,
        default=False
    )
    parser.add_argument(
        "--api",
        help="Run packager in service mode with REST API.",
        dest="api",
        action="store_true",
        required=False,
        default=False
    )

    if args is None:
       args = sys.argv[1:]

    args = parser.parse_args(args)
    
    # By default, perform all validations
    if not args.syntax and not args.integrity and not args.topology:
        args.syntax = args.integrity = args.topology = True
    
    return args