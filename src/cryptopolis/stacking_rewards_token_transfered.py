from bsc_scan import BscScanClient


def main(contract_address: str):
    """Retrieve all the token transfered from the stacking reward contract to the stacking contract"""
    stacking_reward_address = "0x60e75cb4f51bfac38c845d8c240d6a6b03dac2a5"
    client = BscScanClient()
    df = client.get_address_token_transfered(address=stacking_reward_address)
    print(df)
