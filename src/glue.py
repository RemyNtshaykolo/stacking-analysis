from enum import Enum

from s3 import Bucket


class Db(Enum):
    CRYPTO = "crypto"


class Table(Enum):
    RAW_WALLET_TRANSACTION = "raw_wallet_transaction"


def get_s3_path(db: str, table: str):
    return f"s3://{Bucket.CRYPTO_DATAHUB.value}/{db}/{table}"
