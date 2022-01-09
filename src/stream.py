from bsc_scan import BscScanClient
from enum import Enum
import awswrangler as wr
import pandas as pd
from glue import Db, Table, get_s3_path
from dateutil.parser import parse


class Streamtype(Enum):
    TRANSACTION = "transaction"
    TOKEN_TRANSFER = "token_transfer"


def lambda_handler(event, context):
    stream_type = event["stream_type"]
    wallet_address = event["wallet_address"]
    timestamp = int(parse(event["timestamp"]).replace(second=0).timestamp())

    bsc_client = BscScanClient()
    db = Db.CRYPTO.value
    table = Table.RAW_WALLET_TRANSACTION.value
    if stream_type == Streamtype.TRANSACTION.value:

        last_block_downloaded = int(
            wr.athena.read_sql_query(
                f"""SELECT blocknumber FROM {table} ORDER BY blocknumber DESC LIMIT 1""",
                database=db,
            ).loc[0, "blocknumber"]
        )

        current_block = bsc_client.get_current_block(timestamp=timestamp)
        if last_block_downloaded >= current_block:
            raise Exception(
                f"current_block {current_block} can not be smaller or equal to the last downloaded block {last_block_downloaded}"
            )

        df = bsc_client.get_address_transaction_list(
            address=wallet_address,
            from_block=last_block_downloaded,
            to_block=current_block,
        )
        df["datetime"] = pd.to_datetime(df["timeStamp"], unit="s")
        df["date"] = df["datetime"].dt.strftime("%Y-%m-%d")
        wr.s3.to_parquet(
            df=df,
            dataset=True,
            database=db,
            table=table,
            partition_cols=["date"],
            path=get_s3_path(db=db, table=table),
        )
