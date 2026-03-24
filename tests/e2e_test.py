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

import pytest
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from eth_utils import keccak, to_checksum_address
from web3 import Web3
from web3.datastructures import AttributeDict
from web3.exceptions import ContractLogicError, TimeExhausted, Web3RPCError
from web3.middleware import ExtraDataToPOAMiddleware

from tests.config import (
    CHAIN_ID,
    DEPLOYED_CONTRACT_ADDRESS,
    TX_GAS_LIMIT,
    WEB3_HTTP_PROVIDER,
    ZERO_ADDRESS,
)
from tests.util import ContractUtils, TestAccount

web3 = Web3(Web3.HTTPProvider(WEB3_HTTP_PROVIDER))
web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)


def _hex_to_bytes(value: str) -> bytes:
    return bytes.fromhex("".join(value.split()))


def _precompile_address(value: int) -> str:
    return Web3.to_checksum_address(f"0x{value:040x}")


def _to_bytes32(value: int) -> bytes:
    return value.to_bytes(32, byteorder="big")


def _get_p256_vector() -> tuple[bytes, bytes, bytes, bytes, bytes]:
    # Deterministic test vector to keep E2E reproducible.
    private_key = int(
        "1f1e1d1c1b1a191817161514131211101f1e1d1c1b1a19181716151413121110", 16
    )
    key = ECC.construct(curve="P-256", d=private_key)
    message = b"ibet-network-p256-e2e"
    hash_bytes = SHA256.new(message).digest()
    signature = DSS.new(key, "deterministic-rfc6979", encoding="binary").sign(
        SHA256.new(message)
    )

    r_bytes = signature[:32]
    s_bytes = signature[32:64]
    qx_bytes = _to_bytes32(int(key.pointQ.x))
    qy_bytes = _to_bytes32(int(key.pointQ.y))
    return hash_bytes, r_bytes, s_bytes, qx_bytes, qy_bytes


_BLS_G1_ADD_INPUT = _hex_to_bytes("""
    0000000000000000000000000000000017f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb0000000000000000000000000000000008b3f481e3aaa0f1a09e30ed741d8ae4fcf5e095d5d00af600db18cb2c04b3edd03cc744a2888ae40caa232946c5e7e10000000000000000000000000000000017f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb0000000000000000000000000000000008b3f481e3aaa0f1a09e30ed741d8ae4fcf5e095d5d00af600db18cb2c04b3edd03cc744a2888ae40caa232946c5e7e1
    """)
_BLS_G1_ADD_EXPECTED = _hex_to_bytes("""
    000000000000000000000000000000000572cbea904d67468808c8eb50a9450c9721db309128012543902d0ac358a62ae28f75bb8f1c7c42c39a8c5529bf0f4e00000000000000000000000000000000166a9d8cabc673a322fda673779d8e3822ba3ecb8670e461f73bb9021d5fd76a4c56d9d4cd16bd1bba86881979749d28
    """)
_BLS_G2_ADD_INPUT = _hex_to_bytes("""
    00000000000000000000000000000000024aa2b2f08f0a91260805272dc51051c6e47ad4fa403b02b4510b647ae3d1770bac0326a805bbefd48056c8c121bdb80000000000000000000000000000000013e02b6052719f607dacd3a088274f65596bd0d09920b61ab5da61bbdc7f5049334cf11213945d57e5ac7d055d042b7e000000000000000000000000000000000ce5d527727d6e118cc9cdc6da2e351aadfd9baa8cbdd3a76d429a695160d12c923ac9cc3baca289e193548608b82801000000000000000000000000000000000606c4a02ea734cc32acd2b02bc28b99cb3e287e85a763af267492ab572e99ab3f370d275cec1da1aaa9075ff05f79be00000000000000000000000000000000024aa2b2f08f0a91260805272dc51051c6e47ad4fa403b02b4510b647ae3d1770bac0326a805bbefd48056c8c121bdb80000000000000000000000000000000013e02b6052719f607dacd3a088274f65596bd0d09920b61ab5da61bbdc7f5049334cf11213945d57e5ac7d055d042b7e000000000000000000000000000000000ce5d527727d6e118cc9cdc6da2e351aadfd9baa8cbdd3a76d429a695160d12c923ac9cc3baca289e193548608b82801000000000000000000000000000000000606c4a02ea734cc32acd2b02bc28b99cb3e287e85a763af267492ab572e99ab3f370d275cec1da1aaa9075ff05f79be
    """)
_BLS_G2_ADD_EXPECTED = _hex_to_bytes("""
    000000000000000000000000000000001638533957d540a9d2370f17cc7ed5863bc0b995b8825e0ee1ea1e1e4d00dbae81f14b0bf3611b78c952aacab827a053000000000000000000000000000000000a4edef9c1ed7f729f520e47730a124fd70662a904ba1074728114d1031e1572c6c886f6b57ec72a6178288c47c33577000000000000000000000000000000000468fb440d82b0630aeb8dca2b5256789a66da69bf91009cbfe6bd221e47aa8ae88dece9764bf3bd999d95d71e4c9899000000000000000000000000000000000f6d4552fa65dd2638b361543f887136a43253d9c66c411697003f7a13c308f5422e1aa0a59c8967acdefd8b6e36ccf3
    """)
_BLS_PAIRING_FALSE_INPUT = _hex_to_bytes("""
    0000000000000000000000000000000017f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb0000000000000000000000000000000008b3f481e3aaa0f1a09e30ed741d8ae4fcf5e095d5d00af600db18cb2c04b3edd03cc744a2888ae40caa232946c5e7e100000000000000000000000000000000024aa2b2f08f0a91260805272dc51051c6e47ad4fa403b02b4510b647ae3d1770bac0326a805bbefd48056c8c121bdb80000000000000000000000000000000013e02b6052719f607dacd3a088274f65596bd0d09920b61ab5da61bbdc7f5049334cf11213945d57e5ac7d055d042b7e000000000000000000000000000000000ce5d527727d6e118cc9cdc6da2e351aadfd9baa8cbdd3a76d429a695160d12c923ac9cc3baca289e193548608b82801000000000000000000000000000000000606c4a02ea734cc32acd2b02bc28b99cb3e287e85a763af267492ab572e99ab3f370d275cec1da1aaa9075ff05f79be
    """)
_BLS_PAIRING_TRUE_INPUT = _BLS_PAIRING_FALSE_INPUT[:128] + (b"\x00" * 256)
_BLS_PAIRING_RESULT_TRUE = (b"\x00" * 31) + b"\x01"
_BLS_PAIRING_RESULT_FALSE = b"\x00" * 32


# NOTE:
# Called JSON-RPC list.
# - eth_call
# - eth_blockNumber
# - eth_getBlockByNumber
# - eth_getLogs
# - eth_getTransactionCount
# - eth_getTransactionReceipt
# - eth_sendRawTransaction
# - eth_syncing
# - txpool_inspect(Geth API)
# - personal_listAccounts(Geth API)
# - personal_unlockAccounts(Geth API)
# - eth_sendTransaction
# - eth_getCode
class TestE2E:
    ###########################################################################
    # Normal Case
    ###########################################################################

    # <Normal_1_1>
    # deploy setting
    # - eth_getTransactionCount
    # - eth_sendRawTransaction
    # - eth_getTransactionReceipt
    # - eth_call
    def test_normal_1_1(self):
        args = [
            True,
            "0x0123456789abcDEF0123456789abCDef01234567",
            "test text",
            1,
            2,
            b"0123456789abcdefghijklmnopqrstuv",
        ]
        contract_address, _, _ = ContractUtils.deploy_contract(args)
        contract = ContractUtils.get_contract(contract_address)

        # Assertion
        assert contract.functions.item1_bool().call() is True
        assert (
            contract.functions.item1_address().call()
            == "0x0123456789abcDEF0123456789abCDef01234567"
        )
        assert contract.functions.item1_string().call() == "test text"
        assert contract.functions.item1_uint().call() == 1
        assert contract.functions.item1_int().call() == 2
        assert (
            contract.functions.item1_bytes().call()
            == b"0123456789abcdefghijklmnopqrstuv"
        )

    # <Normal_1_2>
    # deploy setting(deployed contract)
    # - eth_call
    def test_normal_1_2(self):
        if DEPLOYED_CONTRACT_ADDRESS == ZERO_ADDRESS:
            return

        # Assertion
        contract = ContractUtils.get_contract(DEPLOYED_CONTRACT_ADDRESS)
        assert contract.functions.item3_bool().call() is False
        assert (
            contract.functions.item3_address().call()
            == "0x0123456789ABCDeF0123456789aBcdEF01234568"
        )
        assert contract.functions.item3_string().call() == "test text2"
        assert contract.functions.item3_uint().call() == 4
        assert contract.functions.item3_int().call() == 8
        assert (
            contract.functions.item3_bytes().call()
            == b"456789abcdefghijklmnopqrstuvwxyz"
        )

    # <Normal_2_1>
    # call setter/getter function
    # - eth_getTransactionCount
    # - eth_sendRawTransaction
    # - eth_getTransactionReceipt
    # - eth_call
    def test_normal_2_1(self, contract):
        args = [
            False,
            "0x0123456789ABCDeF0123456789aBcdEF01234568",
            "test text2",
            4,
            8,
            b"456789abcdefghijklmnopqrstuvwxyz",
        ]
        tx = contract.functions.setItem2(*args, 0).build_transaction(
            transaction={
                "chainId": CHAIN_ID,
                "from": TestAccount.address,
                "gas": TX_GAS_LIMIT,
                "gasPrice": 0,
            }
        )
        ContractUtils.send_transaction(tx, TestAccount.private_key)

        # Assertion
        assert contract.functions.item2_bool().call() is False
        assert (
            contract.functions.item2_address().call()
            == "0x0123456789ABCDeF0123456789aBcdEF01234568"
        )
        assert contract.functions.item2_string().call() == "test text2"
        assert contract.functions.item2_uint().call() == 4
        assert contract.functions.item2_int().call() == 8
        assert (
            contract.functions.item2_bytes().call()
            == b"456789abcdefghijklmnopqrstuvwxyz"
        )
        assert contract.functions.getItemsValueSame().call() == 5

    # <Normal_2_2>
    # call setter/getter function(deployed contract)
    # - eth_getTransactionCount
    # - eth_sendRawTransaction
    # - eth_getTransactionReceipt
    # - eth_call
    def test_normal_2_2(self):
        if DEPLOYED_CONTRACT_ADDRESS == ZERO_ADDRESS:
            return

        # Pre-assertion
        contract = ContractUtils.get_contract(DEPLOYED_CONTRACT_ADDRESS)
        assert contract.functions.getItemsValueOther().call() == 5

        args = [
            False,
            "0x0123456789ABCDeF0123456789aBcdEF01234568",
            "test text2",
            16,
            8,
            b"456789abcdefghijklmnopqrstuvwxyz",
        ]
        tx = contract.functions.setItem2(*args, 0).build_transaction(
            transaction={
                "chainId": CHAIN_ID,
                "from": TestAccount.address,
                "gas": TX_GAS_LIMIT,
                "gasPrice": 0,
            }
        )
        ContractUtils.send_transaction(tx, TestAccount.private_key)

        # Assertion
        assert contract.functions.item2_bool().call() is False
        assert (
            contract.functions.item2_address().call()
            == "0x0123456789ABCDeF0123456789aBcdEF01234568"
        )
        assert contract.functions.item2_string().call() == "test text2"
        assert contract.functions.item2_uint().call() == 16
        assert contract.functions.item2_int().call() == 8
        assert (
            contract.functions.item2_bytes().call()
            == b"456789abcdefghijklmnopqrstuvwxyz"
        )
        assert contract.functions.getItemsValueSame().call() == 17

    # <Normal_3_1>
    # Get events
    # - eth_blockNumber
    # - eth_getTransactionCount
    # - eth_sendRawTransaction
    # - eth_getTransactionReceipt
    # - eth_getLogs
    def test_normal_3_1(self, contract):
        block_from = web3.eth.block_number
        args = [
            False,
            "0x0123456789ABCDeF0123456789aBcdEF01234568",
            "test text2",
            4,
            8,
            b"456789abcdefghijklmnopqrstuvwxyz",
        ]
        tx = contract.functions.setItem2(*args, 0).build_transaction(
            transaction={
                "chainId": CHAIN_ID,
                "from": TestAccount.address,
                "gas": TX_GAS_LIMIT,
                "gasPrice": 0,
            }
        )
        ContractUtils.send_transaction(tx, TestAccount.private_key)
        block_to = web3.eth.block_number
        events = contract.events.SetItem.get_logs(
            from_block=block_from, to_block=block_to
        )

        # Assertion
        assert len(events) == 1
        event = events[0]
        args = event["args"]
        assert args["item_bool"] is False
        assert args["item_address"] == "0x0123456789ABCDeF0123456789aBcdEF01234568"
        assert args["item_string"] == "test text2"
        assert args["item_uint"] == 4
        assert args["item_int"] == 8
        assert args["item_bytes"] == b"456789abcdefghijklmnopqrstuvwxyz"

    # <Normal_3_2>
    # Get events(deployed contract)
    # - eth_call
    # - eth_getLogs
    def test_normal_3_2(self):
        if DEPLOYED_CONTRACT_ADDRESS == ZERO_ADDRESS:
            return

        contract = ContractUtils.get_contract(DEPLOYED_CONTRACT_ADDRESS)
        block_number = contract.functions.optional_item().call()
        events = contract.events.SetItem.get_logs(
            from_block=block_number, to_block=block_number
        )

        # Assertion
        assert len(events) == 1
        event = events[0]
        args = event["args"]
        assert args["item_bool"] is False
        assert args["item_address"] == "0x0123456789ABCDeF0123456789aBcdEF01234568"
        assert args["item_string"] == "test text2"
        assert args["item_uint"] == 4
        assert args["item_int"] == 8
        assert args["item_bytes"] == b"456789abcdefghijklmnopqrstuvwxyz"

    # <Normal_4>
    # Get block by number
    # - eth_blockNumber
    # - eth_getBlockByNumber
    def test_normal_4(self):
        block_number = web3.eth.block_number
        block = web3.eth.get_block(block_number)

        # Assertion
        assert block["number"] == block_number

    # <Normal_5>
    # Get sync information
    # - eth_syncing
    def test_normal_5(self, contract):
        sync = web3.eth.syncing

        # Assertion
        if (
            not isinstance(sync, bool)
            and not isinstance(sync, dict)
            and not isinstance(sync, AttributeDict)
        ):
            assert False

    # <Normal_6>
    # Get inspected transaction pool
    # - txpool_inspect(Geth API)
    def test_normal_6(self, contract):
        txpool = web3.geth.txpool.inspect()

        # Assertion
        if not isinstance(txpool, dict) and not isinstance(txpool, AttributeDict):
            assert False

    # <Normal_7_1>
    # Get bytecode(contract address)
    # - eth_getCode
    def test_normal_7_1(self, contract):
        # Get bytecode
        bytecode = web3.eth.get_code(contract.address)

        # Assertion
        contract_json = ContractUtils.get_contract_json()
        assert bytecode.to_0x_hex() == f'0x{contract_json["deployedBytecode"]}'

    # <Normal_7_2>
    # Get bytecode(EOA address)
    # - eth_getCode
    def test_normal_7_2(self, contract):
        # Get bytecode
        bytecode = web3.eth.get_code(TestAccount.address)

        # Assertion
        assert bytecode.to_0x_hex() == "0x"

    # <Normal_8>
    # Verify secp256r1 signature by precompile (0x0100)
    # - eth_call
    def test_normal_8(self, contract):
        hash_bytes, r_bytes, s_bytes, qx_bytes, qy_bytes = _get_p256_vector()
        call_success, verified, raw_result = contract.functions.verifyP256Result(
            hash_bytes, r_bytes, s_bytes, qx_bytes, qy_bytes
        ).call()

        # Assertion
        assert call_success is True
        assert verified is True
        assert raw_result == (b"\x00" * 31) + b"\x01"

    # <Normal_9_1>
    # BLS12-381 G1Add precompile (0x0b)
    # - eth_call
    def test_normal_9_1(self, contract):
        call_success, raw_result = contract.functions.callPrecompile(
            _precompile_address(0x0B), _BLS_G1_ADD_INPUT
        ).call()

        # Assertion
        assert call_success is True
        assert raw_result == _BLS_G1_ADD_EXPECTED

    # <Normal_9_2>
    # BLS12-381 G2Add precompile (0x0d)
    # - eth_call
    def test_normal_9_2(self, contract):
        call_success, raw_result = contract.functions.callPrecompile(
            _precompile_address(0x0D), _BLS_G2_ADD_INPUT
        ).call()

        # Assertion
        assert call_success is True
        assert raw_result == _BLS_G2_ADD_EXPECTED

    # <Normal_9_3>
    # BLS12-381 Pairing precompile true case (0x0f)
    # - eth_call
    def test_normal_9_3(self, contract):
        call_success, raw_result = contract.functions.callPrecompile(
            _precompile_address(0x0F), _BLS_PAIRING_TRUE_INPUT
        ).call()

        # Assertion
        assert call_success is True
        assert raw_result == _BLS_PAIRING_RESULT_TRUE

    # <Normal_9_4>
    # BLS12-381 Pairing precompile false case (0x0f)
    # - eth_call
    def test_normal_9_4(self, contract):
        call_success, raw_result = contract.functions.callPrecompile(
            _precompile_address(0x0F), _BLS_PAIRING_FALSE_INPUT
        ).call()

        # Assertion
        assert call_success is True
        assert raw_result == _BLS_PAIRING_RESULT_FALSE

    ###########################################################################
    # Error Case
    ###########################################################################

    # <Error_1>
    # Occur REVERT
    # assert error
    def test_error_1(self, contract):
        err_flg = 1
        args = [
            False,
            "0x0123456789ABCDeF0123456789aBcdEF01234568",
            "test text2",
            4,
            8,
            b"456789abcdefghijklmnopqrstuvwxyz",
        ]
        tx = contract.functions.setItem2(*args, err_flg).build_transaction(
            transaction={
                "chainId": CHAIN_ID,
                "from": TestAccount.address,
                "gas": TX_GAS_LIMIT,
                "gasPrice": 0,
            }
        )
        nonce = web3.eth.get_transaction_count(TestAccount.address)
        tx["nonce"] = nonce
        signed_tx = web3.eth.account.sign_transaction(
            transaction_dict=tx, private_key=TestAccount.private_key
        )
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction.to_0x_hex())
        txn_receipt = web3.eth.wait_for_transaction_receipt(
            transaction_hash=tx_hash, timeout=10
        )

        # Assertion
        assert txn_receipt["status"] == 0

    # <Error_2>
    # Occur REVERT
    # require error
    def test_error_2(self, contract):
        err_flg = 2
        args = [
            False,
            "0x0123456789ABCDeF0123456789aBcdEF01234568",
            "test text2",
            4,
            8,
            b"456789abcdefghijklmnopqrstuvwxyz",
        ]
        tx = contract.functions.setItem2(*args, err_flg).build_transaction(
            transaction={
                "chainId": CHAIN_ID,
                "from": TestAccount.address,
                "gas": TX_GAS_LIMIT,
                "gasPrice": 0,
            }
        )
        nonce = web3.eth.get_transaction_count(TestAccount.address)
        tx["nonce"] = nonce
        signed_tx = web3.eth.account.sign_transaction(
            transaction_dict=tx, private_key=TestAccount.private_key
        )
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction.to_0x_hex())
        txn_receipt = web3.eth.wait_for_transaction_receipt(
            transaction_hash=tx_hash, timeout=10
        )

        # Assertion
        assert txn_receipt["status"] == 0

    # <Error_3>
    # Occur REVERT
    # reverted
    def test_error_3(self, contract):
        err_flg = 3
        args = [
            False,
            "0x0123456789ABCDeF0123456789aBcdEF01234568",
            "test text2",
            4,
            8,
            b"456789abcdefghijklmnopqrstuvwxyz",
        ]
        tx = contract.functions.setItem2(*args, err_flg).build_transaction(
            transaction={
                "chainId": CHAIN_ID,
                "from": TestAccount.address,
                "gas": TX_GAS_LIMIT,
                "gasPrice": 0,
            }
        )
        nonce = web3.eth.get_transaction_count(TestAccount.address)
        tx["nonce"] = nonce
        signed_tx = web3.eth.account.sign_transaction(
            transaction_dict=tx, private_key=TestAccount.private_key
        )
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction.to_0x_hex())
        txn_receipt = web3.eth.wait_for_transaction_receipt(
            transaction_hash=tx_hash, timeout=10
        )

        # Assertion
        assert txn_receipt["status"] == 0

    # <Error_4>
    # Occur REVERT
    # Calls to non-existent attribute cause revert.
    def test_error_4(self, contract):
        contract_json = ContractUtils.get_contract_json()

        not_deployed_func = {
            "inputs": [],
            "name": "notExistAttribute",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        }
        # Inject invalid contract function to ABI
        contract_json["abi"].append(not_deployed_func)

        # Create contract object with invalid ABI
        contract_with_invalid_abi = web3.eth.contract(
            address=to_checksum_address(contract.address),
            abi=contract_json["abi"],
        )
        _function = getattr(contract_with_invalid_abi.functions, "notExistAttribute")
        args = []
        with pytest.raises(ContractLogicError):
            _ = _function(*args).call()

    # <Error_5>
    # Occur ERROR
    # Nonce too low
    def test_error_5(self, contract):
        args = [
            False,
            "0x0123456789ABCDeF0123456789aBcdEF01234568",
            "test text2",
            4,
            8,
            b"456789abcdefghijklmnopqrstuvwxyz",
        ]
        tx = contract.functions.setItem2(*args, 0).build_transaction(
            transaction={
                "chainId": CHAIN_ID,
                "from": TestAccount.address,
                "gas": TX_GAS_LIMIT,
                "gasPrice": 0,
            }
        )

        # Get nonce
        nonce = web3.eth.get_transaction_count(TestAccount.address)
        tx["nonce"] = nonce
        signed_tx = web3.eth.account.sign_transaction(
            transaction_dict=tx, private_key=TestAccount.private_key
        )

        # Send Transaction (1): success
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction.to_0x_hex())
        txn_receipt = web3.eth.wait_for_transaction_receipt(
            transaction_hash=tx_hash, timeout=10
        )
        calculated_tx_hash = keccak(hexstr=signed_tx.raw_transaction.to_0x_hex())
        assert tx_hash == calculated_tx_hash
        assert tx_hash == txn_receipt["transactionHash"]

        # Send Transaction (2): nonce too low
        with pytest.raises(
            Web3RPCError, match="{'code': -32000, 'message': 'nonce too low'}"
        ):
            _ = web3.eth.send_raw_transaction(signed_tx.raw_transaction.to_0x_hex())

    # <Error_6>
    # Occur ERROR
    # Already known
    def test_error_6(self, contract):
        args = [
            False,
            "0x0123456789ABCDeF0123456789aBcdEF01234568",
            "test text2",
            4,
            8,
            b"456789abcdefghijklmnopqrstuvwxyz",
        ]
        tx = contract.functions.setItem2(*args, 0).build_transaction(
            transaction={
                "chainId": CHAIN_ID,
                "from": TestAccount.address,
                "gas": TX_GAS_LIMIT,
                "gasPrice": 0,
            }
        )

        # Get nonce
        nonce = web3.eth.get_transaction_count(TestAccount.address)
        tx["nonce"] = nonce + 1
        signed_tx = web3.eth.account.sign_transaction(
            transaction_dict=tx, private_key=TestAccount.private_key
        )

        # Send Transaction (1): sent but not executed
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction.to_0x_hex())
        with pytest.raises(TimeExhausted):
            _ = web3.eth.wait_for_transaction_receipt(
                transaction_hash=tx_hash, timeout=10
            )

        # Send Transaction (2): already known
        with pytest.raises(
            Web3RPCError, match="{'code': -32000, 'message': 'already known'}"
        ):
            _ = web3.eth.send_raw_transaction(signed_tx.raw_transaction.to_0x_hex())

    # <Error_7_1>
    # Invalid signature for secp256r1 precompile
    # - eth_call
    def test_error_7_1(self, contract):
        hash_bytes, r_bytes, s_bytes, qx_bytes, qy_bytes = _get_p256_vector()
        invalid_s = bytes([s_bytes[0] ^ 0x01]) + s_bytes[1:]
        call_success, verified, raw_result = contract.functions.verifyP256Result(
            hash_bytes, r_bytes, invalid_s, qx_bytes, qy_bytes
        ).call()

        # Assertion
        assert call_success is True
        assert verified is False
        assert raw_result == b""

    # <Error_7_2>
    # Invalid input length for secp256r1 precompile
    # - eth_call
    def test_error_7_2(self, contract):
        hash_bytes, r_bytes, s_bytes, qx_bytes, qy_bytes = _get_p256_vector()
        valid_input = hash_bytes + r_bytes + s_bytes + qx_bytes + qy_bytes
        invalid_length_input = valid_input[:-1]
        call_success, raw_result = contract.functions.callPrecompile(
            _precompile_address(0x0100), invalid_length_input
        ).call()

        # Assertion
        assert len(invalid_length_input) == 159
        assert call_success is True
        assert raw_result == b""

    # <Error_8>
    # Invalid input length for BLS12-381 Pairing precompile
    # - eth_call
    def test_error_8(self, contract):
        invalid_length_input = _BLS_PAIRING_TRUE_INPUT + b"\x00"
        call_success, raw_result = contract.functions.callPrecompile(
            _precompile_address(0x0F), invalid_length_input
        ).call()

        # Assertion
        assert len(invalid_length_input) == len(_BLS_PAIRING_TRUE_INPUT) + 1
        assert call_success is False
        assert raw_result == b""
