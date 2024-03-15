"""
Copyright BOOSTRY Co., Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.

SPDX-License-Identifier: Apache-2.0
"""

import os
import sys

path = os.path.join(os.path.dirname(__file__), "../")
sys.path.append(path)

from tests.util import ContractUtils

# Deploy
args = []
contract_address, _, _ = ContractUtils.deploy_contract(args)

print(f"DEPLOYED_CONTRACT_ADDRESS={contract_address}")
