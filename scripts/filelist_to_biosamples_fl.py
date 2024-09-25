import os
import json
import logging

import click
import parse
import pandas as pd

from pathlib import Path

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
        biosamples_data = sample.characteristics.get(characteristic, None)
        if biosamples_data:
            attributes_dict[characteristic] = sample.characteristics[characteristic][0].text
        else:
            attributes_dict[characteristic] = None

    return attributes_dict


def fetch_attributes_if_not_existing(filelist):
    dirpath = os.path.dirname(filelist)
    with open(filelist) as f:
        for fpath in f:
            ba = os.path.basename(fpath)
            basename = os.path.splitext(ba)[0]
            biosamples_id, n = basename.split("_")

            metadata_fname = f"{biosamples_id}.json"
            metadata_fpath = dirpath + '/' + metadata_fname

            if not Path(metadata_fpath).exists():
                logger.info(f"Fetching BioSamples metadata for {biosamples_id}")
                attributes = attributes_dict_from_biosamples_id(biosamples_id)
                with open(metadata_fpath, "w") as fh:
                    json.dump(attributes, fh, indent=2)


@click.command()
@click.argument('input_filelist')
def main(input_filelist):

    logging.basicConfig(level=logging.INFO)

    fetch_attributes_if_not_existing(input_filelist)
    input_dirpath = os.path.dirname(input_filelist)
    all_entries = []
    image_filename_template = "{biosamples_id}_{n}"
    attributes_filename_template = "{biosamples_id}.json"
    with open(input_filelist) as f:
        files = f.readlines()
        for fpath in files:
            fname = os.path.basename(fpath)
            identifier_dict = parse.parse(image_filename_template, fname).named
            attributes_file = attributes_filename_template.format(**identifier_dict)
            attf = input_dirpath +'/' +attributes_file
            with open(attf) as fh:
                attributes = json.load(fh)
            attributes['Files'] = fpath.split('\n')[0]
            all_entries.append(attributes)

    df = pd.DataFrame(all_entries)
    df.set_index(['Files'], inplace=True)
    print(df.to_csv(sep="\t"), end="")


if __name__ == "__main__":
    main()