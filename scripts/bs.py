import os
from pathlib import Path

import click

from biosamples import get_biosample_record


def sto(sample_id):

    sample = get_biosample_record(sample_id)

    attributes_dict = {
        "BioSamples accession ID": sample.accession,
        "NCBI taxonomy ID": sample.taxId
    }

    characteristics = [
        "organism",
        "geographic location (latitude)",
        "geographic location (longitude)",
        "geographic location (region and locality)",
        "habitat",
        "sample collection device or method",
    ]

    for characteristic in characteristics:
        attributes_dict[characteristic] = sample.characteristics[characteristic][0].text

    return attributes_dict


@click.command()
@click.argument('input_dirpath')
def main(input_dirpath):
    for fpath in Path(input_dirpath).iterdir():
        basename = os.path.splitext(fpath.name)[0]
        attributes = sto(basename)
        print(attributes)


if __name__ == "__main__":
    main()