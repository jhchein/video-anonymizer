import datetime
import logging
import os
from argparse import ArgumentParser

import ffmpeg
from azure.storage.blob import BlobClient, ContainerClient

logger = logging.getLogger(__name__)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--inputblob", help="URI of the BLOB with SAS token")
    parser.add_argument("--connectionstring", help="Container connection string")
    return parser.parse_args()


def download_blob(blob_uri_with_sas):
    pass


def main(args):
    blob_client = BlobClient.from_blob_url(args.inputblob)
    container_client = ContainerClient.from_connection_string(
        container_name="videoanonymizer", conn_str=args.connectionstring
    )

    # Download the blob to a local file
    with open("input.mp4", "wb") as fh:
        blob_data = blob_client.download_blob()
        blob_data.readinto(fh)

    # GET CREATION DATE FROM FILE
    logger.info("Probing File")
    probe = ffmpeg.probe(filename="input.mp4")
    creation_time = probe["format"]["tags"]["creation_time"]
    creation_datetime = datetime.datetime.strptime(
        creation_time, "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    logger.info(f"Creation time: {creation_datetime}")

    os.makedirs("output", exist_ok=True)
    ffmpeg.input("input.mp4").output("output/out-%04d.jpg").run(quiet=True)

    # Upload the files to the container
    target_folder = os.path.join(
        "output",
        str(creation_datetime.year),
        str(creation_datetime.month),
        str(creation_datetime.day),
        os.path.split(blob_client.blob_name)[-1],
    )
    for file in os.listdir("output"):
        with open(os.path.join("output", file), "rb") as fh:
            container_client.upload_blob(
                name=os.path.join(target_folder, file), data=fh
            )
    logger.info("Upload complete")


if __name__ == "__main__":
    args = parse_args()
    main(args)
