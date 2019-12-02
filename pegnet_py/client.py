import random
import string
from factom_keys.fct import FactoidAddress
from typing import List, Union
from urllib.parse import urljoin

from .errors import handle_error_response
from .session import APISession


class BaseAPI(object):
    def __init__(self, ec_address=None, fct_address=None, host=None, username=None, password=None, certfile=None):
        """
        Instantiate a new API client.

        Args:
            ec_address (str): A default entry credit address to use for
                transactions. Credits will be spent from this address.
            fct_address (str): A default factoid address to use for
                transactions.
            host (str): Hostname, including http(s)://, of the node
            username (str): RPC username for protected APIs.
            password (str): RPC password for protected APIs.
            certfile (str): Path to certificate file to verify for TLS
                connections (mostly untested).
        """
        self.ec_address = ec_address
        self.fct_address = fct_address
        self.version = "v1"

        if host:
            self.host = host

        self.session = APISession()

        if username and password:
            self.session.init_basic_auth(username, password)

        if certfile:
            self.session.init_tls(certfile)

    @property
    def url(self):
        return urljoin(self.host, self.version)

    @staticmethod
    def _xact_name():
        return "TX_{}".format("".join(random.choices(string.ascii_uppercase + string.digits, k=6)))

    def _request(self, method, params=None, request_id: int = 0):
        data = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params:
            data["params"] = params

        resp = self.session.request("POST", self.url, json=data)

        resp_json = resp.json()
        if resp.status_code >= 400 or len(resp_json.get("error", {}).keys()) != 0:
            handle_error_response(resp)

        return resp_json.get("result")


class PegNetd(BaseAPI):
    def __init__(self, ec_address=None, fct_address=None, host=None, username=None, password=None, certfile=None):
        tmp_host = host if host is not None else "http://localhost:8070"
        super().__init__(ec_address, fct_address, tmp_host, username, password, certfile)

    def get_sync_status(self):
        """Retrieve the current sync status of the node."""
        return self._request("get-sync-status")

    def get_balances(self, address: FactoidAddress):
        """Retrieve all current pegnet balances for the given address"""
        return self._request("get-pegnet-balances", {"address": address.to_string()})

    def get_issuance(self):
        """Retrieve the token issuance for all pegnet assets"""
        return self._request("get-pegnet-issuance")

    def get_rates(self, height: int):
        """Retrieve the PegNet conversion rates for a given height"""
        return self._request("get-pegnet-rates", {"height": height})

    def get_tx_status(self, entry_hash: Union[bytes, str]):
        """Retrieve the status for a PegNet transaction"""
        return self._request(
            "get-transaction-status", {"entryhash": entry_hash.hex() if type(entry_hash) is bytes else entry_hash}
        )

    def get_txs(
        self,
        entry_hash: Union[bytes, str] = None,
        address: str = None,
        height: int = None,
        offset: int = 0,
        desc: bool = False,
        transfer: bool = True,
        conversion: bool = True,
        coinbase: bool = True,
        burn: bool = True,
    ):
        """Retrieve the transactions associated with the provided entry_hash or address or height"""
        request_params = {}

        if entry_hash:
            request_params["entryhash"] = entry_hash.hex() if type(entry_hash) is bytes else entry_hash
        elif address:
            request_params["address"] = address
        elif height:
            request_params["height"] = height
        else:
            raise ValueError("One of entry_hash, address or height must be specified")

        request_params.update(
            {
                "offset": offset,
                "desc": desc,
                "transfer": transfer,
                "conversion": conversion,
                "coinbase": coinbase,
                "burn": burn,
            }
        )

        return self._request("get-transactions", request_params)

    def send_transaction(self, chain_id: bytes, ext_ids: List[bytes], content: bytes):
        """Send a transaction with the specified external ids and content"""
        return self._request(
            "send-transaction",
            {"chainid": chain_id.hex(), "extids": [x.hex() for x in ext_ids], "content": content.hex()},
        )
