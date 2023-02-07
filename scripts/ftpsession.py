# coding: utf-8
import logging
from pathlib import Path
import ftplib

import click


logger = logging.getLogger(__file__)


def ftp_sync(remote_dirname, fpaths_to_sync):
    host = "ftp-private.ebi.ac.uk"
    username = "bsftp"
    password = "bsftp1"
    secret_dir = "/.beta/32/3ff81d-4b65-40a3-b141-1d950cb3db57-a31879"
    ftp = ftplib.FTP(host)
    ftp.login(username, password)

    submission_dirname = remote_dirname
    ftp.cwd(secret_dir)
    try:
        ftp.mkd(submission_dirname)
    except ftplib.error_perm:
        pass

    ftp.cwd(submission_dirname)
    remote_files = set(ftp.nlst())

    for fpath in fpaths_to_sync:
        if fpath.name not in remote_files:
            with open(fpath, "rb") as fh:
                logger.info(f"Storing {fpath}")
                ftp.storbinary("STOR " + fpath.name, fh)


@click.command()
@click.argument("local_dirname")
def main(local_dirname):
    logging.basicConfig(level=logging.INFO)

    local_dirpath = Path(local_dirname)
    
    fpaths_to_sync = local_dirpath.glob("*.jpg")

    ftp_sync(remote_dirname=local_dirname, fpaths_to_sync=fpaths_to_sync)


if __name__ == "__main__":
    main()