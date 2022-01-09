from enum import Enum
import awswrangler as wr


class Bucket(Enum):
    CRYPTO_DATAHUB = "crypto-datahub"


def clean_s3_folder(path):
    wr.s3.delete_objects(path)
