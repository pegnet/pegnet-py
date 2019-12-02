import dataclasses
import datetime
import hashlib
import json
from dataclasses import dataclass
from factom_keys.fct import FactoidAddress, FactoidPrivateKey
from typing import Any, Dict, List, Set, Tuple

from .consts import ALL_ASSETS, TRANSACTIONS_CHAIN_ID


@dataclass
class Transaction:
    input: Dict[str, Any] = dataclasses.field(default_factory=dict)
    transfers: List[Dict[str, Any]] = dataclasses.field(default_factory=list)
    conversion: str = None
    metadata: str = None

    def set_input(self, address: FactoidAddress, asset_type: str, amount: int):
        """
        :param address: The public Factoid address spending the assets being transacted
        :param asset_type: The pegged asset token ticker to transact
        :param amount: The amount of `asset_type` tokens being transacted
        :return:
        """
        self.input = {"address": address.to_string(), "type": asset_type, "amount": amount}

    def add_transfer(self, address: FactoidAddress, amount: int):
        """
        :param address: The public Factoid address receiving the assets being transacted
        :param amount: The amount of `asset_type` tokens being asked for
        :return:
        """
        transfer = {"address": address.to_string(), "amount": amount}
        self.transfers.append(transfer)

    def to_dict(self):
        tx = {"input": self.input}
        if 0 < len(self.transfers):
            tx["transfers"] = self.transfers
        if self.conversion is not None:
            tx["conversion"] = self.conversion
        if self.metadata is not None:
            tx["metadata"] = self.metadata
        return tx

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return Transaction(
            input=d.get("input"),
            transfers=d.get("transfers"),
            conversion=d.get("conversion"),
            metadata=d.get("metadata"),
        )

    def is_valid(self) -> bool:
        """
        Returns True if the structure of the transaction is sane and able to be executed.
        Does not take balances or conversion rates into account
        """
        if type(self.input) != dict:
            return False

        input_address = self.input.get("address")
        if not FactoidAddress.is_valid(input_address):
            return False  # Address must be a valid Factoid address string

        input_type = self.input.get("type")
        if input_type not in ALL_ASSETS:
            return False  # Input type must be a valid pegged asset

        input_amount = self.input.get("amount")
        if type(input_amount) != int or input_amount < 0:
            return False  # Input amount must  a positive integer

        if self.transfers is not None and self.conversion is not None:
            return False

        if self.transfers is not None:
            if type(self.transfers) != list:
                return False
            for transfer in self.transfers:
                if type(transfer) != dict:
                    return False

                output_address = transfer.get("address")
                if not FactoidAddress.is_valid(output_address):
                    return False

                output_amount = transfer.get("amount")
                if type(output_amount) != int or output_amount < 0:
                    return False  # Output amount must be None or a positive integer
        elif self.conversion not in ALL_ASSETS:
            return False

        return True


@dataclass
class TransactionBatch:
    timestamp: str = str(int(datetime.datetime.utcnow().timestamp()))

    _txs: List[Transaction] = dataclasses.field(init=False, default_factory=list)
    _signer_keys: List[FactoidPrivateKey] = dataclasses.field(init=False, default_factory=list)

    def add_transaction(self, tx: Transaction) -> None:
        self._txs.append(tx)

    def add_signer(self, key: FactoidPrivateKey) -> None:
        self._signer_keys.append(key)

    def sign(self) -> Tuple[List[bytes], bytes]:
        """
        Sign the object using all private keys added to this object. Signature scheme is detailed here:
        https://github.com/Factom-Asset-Tokens/FAT/blob/master/fatips/103.md#salting-hashing-and-signing

        :return: A tuple containing the list of external ids, then the content (all as bytes)
        """
        tx_payload = {"version": 1, "transactions": [tx.to_dict() for tx in self._txs]}
        content = json.dumps(tx_payload, separators=(",", ":")).encode()

        chain_id = TRANSACTIONS_CHAIN_ID
        external_ids = [self.timestamp.encode()]
        for i, key in enumerate(self._signer_keys):
            rcd = b"\x01" + key.get_factoid_address().key_bytes
            external_ids.append(rcd)

            message = bytearray()
            message.extend(str(i).encode())
            message.extend(self.timestamp.encode())
            message.extend(chain_id)
            message.extend(content)
            message_hash = hashlib.sha512(message).digest()
            signature = key.sign(message_hash)
            external_ids.append(signature)

        return external_ids, content

    @classmethod
    def from_entry(cls, external_ids: List[bytes], content: bytes):
        """
        Parses an entry (the external_ids and content) and tries to construct a TransactionEntry.
        If it does not have the proper structure or all required signatures to cover inputs, None will be returned.
        """
        if len(external_ids) < 3 or len(external_ids) % 2 != 1:
            return None  # Number of external ids = 1 + 2 * N, where N is number of signatures >= 1

        timestamp = external_ids[0]

        # Gather all (public key, signature) pairs from the external ids
        full_signatures = external_ids[1:]
        observed_signatures: List[Tuple[FactoidAddress, bytes]] = []
        observed_signers: Set[str] = set()
        for i, rcd in enumerate(full_signatures[::2]):
            signature = full_signatures[2 * i + 1]
            if len(rcd) != 33 or len(signature) != 64:
                return None
            address_bytes = rcd[1:]
            address = FactoidAddress(key_bytes=address_bytes)
            observed_signatures.append((address, signature))
            observed_signers.add(address.to_string())

        # Check that the content field has a valid json with a "transactions" list
        try:
            tx_payload = json.loads(content.decode())
        except ValueError:
            return None
        if "transactions" not in tx_payload:
            return None
        tx_list = tx_payload["transactions"]
        if type(tx_list) != list:
            return None

        # Check that all included inputs are valid and collect the keys we need to have signatures for
        e = TransactionBatch(timestamp=timestamp.decode())
        for tx_dict in tx_list:
            if type(tx_dict) != dict:
                return None
            tx = Transaction(
                input=tx_dict.get("input"),
                transfers=tx_dict.get("transfers"),
                conversion=tx_dict.get("conversion"),
                metadata=tx_dict.get("metadata"),
            )
            if not tx.is_valid():
                return None
            e.add_transaction(tx)
            if tx.input["address"] not in observed_signers:
                return None  # Missing this input signer, not a valid entry

        # Finally check all the signatures
        chain_id = TRANSACTIONS_CHAIN_ID
        for i, full_signature in enumerate(observed_signatures):
            key, signature = full_signature

            message = bytearray()
            message.extend(str(i).encode())
            message.extend(timestamp)
            message.extend(chain_id)
            message.extend(content)
            message_hash = hashlib.sha512(message).digest()
            if not key.verify(signature, message_hash):
                return None

        return e
