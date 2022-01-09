from bsc_scan import BscScanClient
import pandas as pd
import awswrangler as wr


def main(cryptopolis_stacking_contract: str):
    client = BscScanClient()
    # last_block = wr.athena.read_sql_query(
    #     "SELECT blockNumber FROM stacking_transaction ORDER BY blockNumber DESC LIMIT 1",
    #     database="cryptopolis",
    # )

    df = client.get_contract_transaction(
        address=cryptopolis_stacking_contract, from_block=0
    )

    df["datetime"] = pd.to_datetime(df["timeStamp"], unit="s")

    wr.s3.to_parquet(
        df=df,
        path="s3://crypto-datahub/cryptopolis/stacking_transaction",
        dataset=True,
        database="cryptopolis",
        table="stacking_transaction",
    )
