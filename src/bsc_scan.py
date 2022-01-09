import os
import requests
import pandas as pd
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class BscScanClient:
    def __init__(self):
        self.secret = os.environ["bsc_scan_api_key"]

    def get_current_block(self, timestamp):
        url = (
            "https://api.bscscan.com/api"
            "?module=block"
            "&action=getblocknobytime"
            f"&timestamp={timestamp}"
            "&closest=before"
            f"&apikey={self.secret}"
        )
        return int(self.request_proxy(url))

    def get_address_transaction_list(
        self, address: str, from_block=0, to_block=99999999
    ):
        logger.info(f"Retrieve data from block:{from_block} to block :{to_block}")
        url = (
            "https://api.bscscan.com/api?module=account"
            "&action=txlist"
            f"&address={address}"
            f"&startblock={from_block}"
            f"&endblock={to_block}"
            "&sort=asc"
            f"&apikey={self.secret}"
        )
        return pd.DataFrame(self.request_proxy(url))

    def get_address_token_transfered(self, address: str):
        url = (
            "https://api.bscscan.com/api?module=account"
            "&action=tokentx"
            f"&address={address}"
            "&startblock=0"
            "&endblock=999999999"
            "&sort=asc"
            f"&apikey={self.secret}"
        )
        pass

    @staticmethod
    def request_proxy(url):
        resp = requests.get(url)
        data = json.loads(resp.content)
        if data["message"] == "NOTOK":
            raise Exception(
                f"An error occured during {resp.url} with message: \n Error message:  {data['result']}"
            )

        return json.loads(requests.get(url).content)["result"]
