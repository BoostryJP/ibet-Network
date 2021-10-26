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
import json
import os
import sys

import solcx

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

from tests.config import (
    SOLC_VERSION_PRAGMA,
    CONTRACT_PATH,
    CONTRACT_NAME
)

# Install Solc
solcx.install_solc_pragma(SOLC_VERSION_PRAGMA)
version = solcx.get_installed_solc_versions()[0]

# Compile Test Contract
spec = {
    "language": "Solidity",
    "sources": {
        f"{CONTRACT_NAME}.sol": {
            "urls": [f"{CONTRACT_PATH}/{CONTRACT_NAME}.sol"]
        }
    },
    "settings": {
        "evmVersion": "byzantium",
        "optimizer": {
            "enabled": True,
            "runs": 200
        },
        "outputSelection": {
            "*": {
                "*": [
                    "abi", "evm.bytecode.object", "evm.deployedBytecode.object",
                ]
            }
        }
    }
}
contract_json = solcx.compile_standard(
    spec,
    allow_paths=[os.path.dirname(os.path.abspath(__file__))],
    solc_version=version)

# Output File
contract_json = contract_json["contracts"][f"{CONTRACT_NAME}.sol"][CONTRACT_NAME]
contract_json["bytecode"] = contract_json["evm"]["bytecode"]["object"]
contract_json["deployedBytecode"] = contract_json["evm"]["deployedBytecode"]["object"]
contract_json.pop("evm")
with open(f"{CONTRACT_PATH}/{CONTRACT_NAME}.json", "w") as f:
    f.write(json.dumps(contract_json))
