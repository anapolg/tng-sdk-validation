#  Copyright (c) 2018 SONATA-NFV, 5GTANGO, UBIWHERE, QUOBIS SL.
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
import os

import time
import zipfile
import shutil
import atexit

from tngsdk.validation.tools import event
from tngsdk.validation.tools.storage import DescriptorStorage
from tngsdk.validation.tools.project import Project

from contextlib import closing
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

LOG = logging.getLogger(os.path.basename(__file__))
evtlog = event.get_logger('validator.events')

class Validator(object):
    def __init__(self):
        self.source_id = None
        self._syntax = True
        self._integrity = True
        self._topology = True

        # For package signature validation
        self._pkg_signature = None
        self._pkg_pubkey = None

        # Descriptors storage
        self._storage = DescriptorStorage()


    @staticmethod
    def validate_package_signature(package, signature, pubkey):
        """
        Verifies with the public key from whom the package file came that is
        indeed signed by their private key
        :param package: path to package file
        :param signature: String signature to be verified
        :param pubkey: String public key
        :return: Boolean. True if valid signature, False otherwise.
        """
        LOG.info("Validating signature of package '{0}'".format(package))
        try:
            with open(package, 'rb') as _file:
                file_data = _file.read()
            pkg_hash = SHA256.new(file_data).digest()
            rsa_key = RSA.importKey(pubkey)
            signature = (eval(signature), )
            result = rsa_key.verify(pkg_hash, signature)
        except IOError as err:
            LOG.error("I/O error: {0}".format(err))
            return False
        except ValueError:
            LOG.error("Invalid key format")
            return False
        except Exception as err:  # override, so validator doesn't crash
            LOG.error("Exception error: {0}".format(err))
            return False

        return result

    # TODO finish validating package. Problem creating package with storage.py
    def validate_package(self, package):
        """
        Validate a 5GTANGO package.
        By default, it performs the following validations: syntax, integrity
        and network topology.
        :param package: 5GTANGO package filename
        :return: True if all validations were successful, False otherwise
        """
        
        self.source_id = package
        LOG.info("Validating package '{0}'".format(os.path.abspath(package)))

        # Check if package is packed in the correct format
        if not zipfile.is_zipfile(package):
            evtlog.log("Invalid package format",
                       "Invalid 5GTANGO package '{}'".format(package),
                       self.source_id,
                       'evt_package_format_invalid')
            return

        package_dir = '.' + str(time.time())
        with closing(zipfile.ZipFile(package, 'r')) as pkg:
            # Extract package contents
            pkg.extractall(package_dir)

            # Set folder for deletion when program exits
            atexit.register(shutil.rmtree, package_dir)

        # Validate package signature (optional)
        if (self._pkg_signature and self._pkg_pubkey) and (
                not self.validate_package_signature(package,
                                                    self._pkg_signature,
                                                    self._pkg_pubkey)):
            evtlog.log("Invalid package signature",
                       "Invalid signature of package '{}'".format(package),
                       self.source_id,
                       'evt_package_signature_invalid')
            return

        pd_filename = os.path.join(package_dir, 'mynsd.mf')
        package = self._storage.create_package(pd_filename)
        # if not package.id:
        #     return

        # if self._syntax and not self._validate_package_syntax(package):
        #     return

        # if self._integrity and not self._validate_package_integrity(package, package_dir):
        #     LOG.warning("Syntax and topology not implemented yet")
        #     return

        return True

    def validate_project(self, prj_root):
        """
        Validate a 5GTANGO project.
        By default, it performs the following validations: syntax, integrity
        and network topology.
        :param project: 5GTANGO project
        :return: True if all validations were successful, False otherwise
        """
        
        project = Project.__create_from_descriptor__(workspace, prj_root)
        if not project:
            LOG.error("Invalid project path: '%s'\n  " % prj_root)
            exit(1)

        # Consider cases when project is a path
        # if type(project) is not Project and os.path.isdir(project):
        #     if not self._workspace:
        #         LOG.error("Workspace not defined. Unable to validate project")
        #         return

        #     project = Project.__create_from_descriptor__(self._workspace,
        #                                                  project)

        # if type(project) is not Project:
        #     return

        # log.info("Validating project '{0}'".format(project.project_root))
        # log.info("... syntax: {0}, integrity: {1}, topology: {2}"
        #          .format(self._syntax, self._integrity, self._topology))

        # # retrieve project configuration
        # self._dpath = project.vnfd_root
        # self._dext = project.descriptor_extension

        # # load all project descriptors present at source directory
        # log.debug("Loading project service")
        # nsd_file = Validator._load_project_service_file(project)
        # if not nsd_file:
        #     return

        # return self.validate_service(nsd_file)






    # def validate_service(self, nsd_file):
    #     """
    #     Validate a SONATA service.
    #     By default, it performs the following validations: syntax, integrity
    #     and network topology.
    #     :param nsd_file: service descriptor filename
    #     :return: True if all validations were successful, False otherwise
    #     """
    #     if not self._assert_configuration():
    #         return

    #     log.info("Validating service '{0}'".format(nsd_file))
    #     log.info("... syntax: {0}, integrity: {1}, topology: {2}"
    #              .format(self._syntax, self._integrity, self._topology))

    #     service = self._storage.create_service(nsd_file)
    #     if not service:
    #         evtlog.log("Invalid service descriptor",
    #                    "Failed to read the service descriptor of file '{}'"
    #                    .format(nsd_file),
    #                    nsd_file,
    #                    'evt_service_invalid_descriptor')
    #         return

    #     # validate service syntax
    #     if self._syntax and not self._validate_service_syntax(service):
    #         return

    #     if self._integrity and not self._validate_service_integrity(service):
    #         return

    #     if self._topology and not self._validate_service_topology(service):
    #         return

    #     return True

    # def validate_function(self, vnfd_path):
    #     """
    #     Validate one or multiple SONATA functions (VNFs).
    #     By default, it performs the following validations: syntax, integrity
    #     and network topology.
    #     :param vnfd_path: function descriptor (VNFD) filename or
    #                       a directory to search for VNFDs
    #     :return: True if all validations were successful, False otherwise
    #     """
    #     if not self._assert_configuration():
    #         return

    #     # validate multiple VNFs
    #     if os.path.isdir(vnfd_path):
    #         log.info("Validating functions in path '{0}'".format(vnfd_path))

    #         vnfd_files = list_files(vnfd_path, self._dext)
    #         for vnfd_file in vnfd_files:
    #             if not self.validate_function(vnfd_file):
    #                 return
    #         return True

    #     log.info("Validating function '{0}'".format(vnfd_path))
    #     log.info("... syntax: {0}, integrity: {1}, topology: {2}"
    #              .format(self._syntax, self._integrity, self._topology))

    #     func = self._storage.create_function(vnfd_path)
    #     if not func:
    #         evtlog.log("Invalid function descriptor",
    #                    "Couldn't store VNF of file '{0}'".format(vnfd_path),
    #                    vnfd_path,
    #                    'evt_function_invalid_descriptor')
    #         return

    #     if self._syntax and not self._validate_function_syntax(func):
    #         return

    #     if self._integrity and not self._validate_function_integrity(func):
    #         return

    #     if self._topology and not self._validate_function_topology(func):
    #         return

    #     return True
