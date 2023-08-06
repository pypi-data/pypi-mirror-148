#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import logging
import os
import sys
from time import sleep
import unittest

from kubernetes import client, config
from kubernetes.client import V1PersistentVolume, V1PersistentVolumeClaim

# noinspection PyBroadException
try:
    config.load_kube_config()
except Exception:
    msg = "Kubernetes is not running\n"
    sys.stdout.write(f"INFO: {msg}")

_LOG = logging.getLogger('volume_util')
_LOCAL_VOLUMES = set([])
_kubernetes = client.CoreV1Api()

class TestKubernetesVolume(unittest.TestCase):
    def setUp(self) -> None:
        self.config = {
            'volumes': [
                {
                    'volume': 'gettingstartedvol',
                    'claim_name': 'gettingstartedvol-pvc'
                }
            ]
        }
        # configs = ConfigUtil(path).safe_load(is_render_variables=True,
        #                                                 soft_merge=True)
        # for config in configs:
        #     if config.get('volumes'):
        #         logging.info(f'local volume is being created')
        #         volume_util.create_local_volumes(config, os.path.dirname(
        #             files_util.resolve_pipeline_source_file(config['name'])))

        # cls.config = base.get_e2e_configuration()

    def test_create_volume(self):
        create_volume = volume_util.create_local_volumes(self.config, os.path.dirname(
            files_util.resolve_pipeline_source_file(self.config['name'])))
        self.assertTrue('RUN pip install -r requirements.txt' in build_out,
                        'Incorrect pip command')
        # expected = {
        #     "env": "env1",
        #     "env4": "env4",
        #     "env_dict": {
        #         "env2": "env2",
        #         "env3": "env3"
        #     }
        # }
        # self.assertEqual(expected, dict_util.merge_dicts(self.dict1, self.dict2, True))


    def setUp(self) -> None:
        self.dict1 = {
            "env": "env1",
            "env_dict":
                {
                    "env3": "env3"
                },
            "env4": "env4"
        }

        self.dict2 = {
            "env": "env1",
            "env_dict":
                {
                    "env2": "env2"
                }
        }