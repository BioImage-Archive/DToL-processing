import os
import logging

import click
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
        biosamples_data = sample.characteristics.get(characteristic, None)
        if biosamples_data:
            attributes_dict[characteristic] = sample.characteristics[characteristic][0].text
        else:
            attributes_dict[characteristic] = None

    return attributes_dict


@click.command()
@click.argument('old_filelist')
@click.argument('new_filelist')
def main(old_filelist, new_filelist):

    logging.basicConfig(level=logging.INFO)
    new_entries = []
    old_entries = []
    if old_filelist:
        old_entries = pd.read_csv(old_filelist, sep="\t") 

    with open(new_filelist) as f:
        for fpath in f:
            if 'Files' in fpath:
                continue
            ba = os.path.basename(fpath)
            basename = os.path.splitext(ba)[0]
            biosamples_id, n = basename.split("_")
            if ba not in old_entries['Files'].values:
                 attributes = attributes_dict_from_biosamples_id(biosamples_id)
                 attributes['Files'] = fpath.split('\n')[0]
                 new_entries.append(attributes)
                

    df = pd.DataFrame(new_entries)
    df.set_index(['Files'], inplace=True)
    old_entries.set_index(['Files'], inplace=True)
    #df2 = pd.concat([old_entries,df])
    df2 = old_entries.combine_first(df)
    print(df2.to_csv(sep="\t"), end="")


if __name__ == "__main__":
    main()