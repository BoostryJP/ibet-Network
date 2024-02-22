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

import logging
import os
import sys
import time
from logging.config import dictConfig

from requests.exceptions import ConnectionError
from web3 import Web3

BLOCK_SYNC_MONITORING_INTERVAL = os.environ.get("BLOCK_SYNC_MONITORING_INTERVAL") or 30
MINIMUM_INCREMENTAL_NUMBER = (
    os.environ.get("BLOCK_SYNC_MONITORING_MINIMUM_INCREMENTAL_NUMBER") or 1
)

web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

LOG_CONFIG = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        }
    },
    "loggers": {
        "monitor": {
            "handlers": [
                "console",
            ],
            "propagate": False,
        }
    },
    "root": {
        "level": "INFO",
    },
}
dictConfig(LOG_CONFIG)
log_fmt = "%(levelname)s [%(asctime)s|MONITOR-BLOCK-SYNC] %(message)s"
logging.basicConfig(format=log_fmt)


def monitor_block_sync(start_block_number):
    """Monitor block synchronization

    :param start_block_number: Monitoring start block number
    :return: Next monitoring start block number
    """
    try:
        latest_block_number = web3.eth.blockNumber
        if (
            latest_block_number - start_block_number > MINIMUM_INCREMENTAL_NUMBER
        ):  # Normal
            logging.info(
                f"Blocks are successfully synchronized: "
                f"start={start_block_number}, "
                f"latest={latest_block_number}"
            )
            start_block_number = latest_block_number
        else:  # Fatal Error
            logging.error(
                f"FATAL: Block number has not been increased: "
                f"start={start_block_number}, "
                f"latest={latest_block_number}"
            )
    except ConnectionError:
        logging.warning("Unable to connect to node")
    except Exception as err:
        logging.exception(
            "An exception occurred while monitoring block synchronization: ", err
        )
    finally:
        return start_block_number


if __name__ == "__main__":
    block_number = 0
    while True:
        start_time = time.time()

        block_number = monitor_block_sync(start_block_number=block_number)

        elapsed_time = time.time() - start_time
        time.sleep(max(BLOCK_SYNC_MONITORING_INTERVAL - elapsed_time, 0))
