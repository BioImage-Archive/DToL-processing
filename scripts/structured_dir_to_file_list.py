import os
import json
import logging
from pathlib import Path

import click
import parse
import pandas as pd

from biosamples import get_biosample_record


logger = logging.getLogger(__file__)


def attributes_dict_from_biosamples_id(sample_id):

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


def fetch_attributes_if_not_existing(dirpath):

    for fpath in dirpath.glob("*.jpg"):
        basename = os.path.splitext(fpath.name)[0]
        biosamples_id, n = basename.split("_")

        metadata_fname = f"{biosamples_id}.json"
        metadata_fpath = dirpath/metadata_fname

        if not metadata_fpath.exists():
            logger.info(f"Fetching BioSamples metadata for {biosamples_id}")
            attributes = attributes_dict_from_biosamples_id(biosamples_id)
            with open(metadata_fpath, "w") as fh:
                json.dump(attributes, fh, indent=2)


@click.command()
@click.argument('input_dirpath')
def main(input_dirpath):

    logging.basicConfig(level=logging.INFO)

    input_dirpath = Path(input_dirpath)

    fetch_attributes_if_not_existing(input_dirpath)

    all_entries = []
    image_filename_template = "{biosamples_id}_{n}.jpg"
    attributes_filename_template = "{biosamples_id}.json"
    for fpath in input_dirpath.glob("*.jpg"):
        identifier_dict = parse.parse(image_filename_template, fpath.name).named
        attributes_file = attributes_filename_template.format(**identifier_dict)
        with open(input_dirpath/attributes_file) as fh:
            attributes = json.load(fh)
        attributes['Files'] = fpath.name
        all_entries.append(attributes)

    df = pd.DataFrame(all_entries)
    df.set_index(['Files'], inplace=True)
    print(df.to_csv())


if __name__ == "__main__":
    main()