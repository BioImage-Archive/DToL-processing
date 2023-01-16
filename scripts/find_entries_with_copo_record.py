import json
import shutil
import logging
from pathlib import Path
from collections import defaultdict

import click
import requests
from pydantic import BaseModel, parse_file_as

from biostudies import load_submission, find_files_in_submission, file_uri, attributes_to_dict


logger = logging.getLogger(__file__)


def get_nhm_id_to_biosample_id_mapping(copo_output_json_fpath):
    """Load the dump from COPO and use to generate a mapping from NHM
    identifiers to BioSamples IDs"""

    with open(copo_output_json_fpath) as fh:
        raw_copo = json.load(fh)

    indexes = list(raw_copo.values())[0].keys()
    copo_attrs = raw_copo.keys()
    sample_dicts = {
        index: { attr: raw_copo[attr][index] for attr in copo_attrs }
        for index in indexes
    }

    nhm_to_biosample_id = {
        sample_dict['specimen_id'] : sample_dict['biosampleAccession']
        for sample_dict in sample_dicts.values()
    }

    return nhm_to_biosample_id


def copy_uri_to_local(src_uri: str, dst_fpath: Path):
    """Copy the object at the given source URI to the local path specified by dst_fpath."""

    logger.info(f"Fetching {src_uri} to {dst_fpath}")

    with requests.get(src_uri, stream=True) as r:
        with open(dst_fpath, "wb") as fh:
            shutil.copyfileobj(r.raw, fh)


@click.command()
@click.argument("copo_output_json_fpath")
def main(copo_output_json_fpath):

    logging.basicConfig(level=logging.INFO)

    submission = load_submission("S-BIAD588")
    file_list = find_files_in_submission(submission)
    nhm_to_biosample_id = get_nhm_id_to_biosample_id_mapping(copo_output_json_fpath)

    nhm_ids_in_copo = set(nhm_to_biosample_id.keys())
    print(nhm_ids_in_copo)

    # by_nhm_id = defaultdict(list)
    # for file in file_list:
    #     attr_dict = attributes_to_dict(file.attributes)
    #     nhm_barcode = attr_dict["NHMUK barcode"]
    #     nhm_id = f"NHMUK{nhm_barcode}"
    #     if nhm_id in nhm_ids_in_copo:
    #         uri = file_uri("S-BIAD588", file)
    #         by_nhm_id[nhm_id].append(uri)

    # print(by_nhm_id)

    by_biosamples_id = defaultdict(list)
    for file in file_list:
        attr_dict = attributes_to_dict(file.attributes)
        nhm_barcode = attr_dict["NHMUK barcode"]
        nhm_id = f"NHMUK{nhm_barcode}"
        if nhm_id in nhm_ids_in_copo:
            biosamples_id = nhm_to_biosample_id[nhm_id]
            uri = file_uri("S-BIAD588", file)
            by_biosamples_id[biosamples_id].append(uri)

    test = list(by_biosamples_id.items())[1]

    output_dirpath = Path("structured_data")
    output_dirpath.mkdir(exist_ok=True)

    fname = f"{test[0]}.jpg"
    uri = test[1][0]

    output_fpath = output_dirpath/fname

    copy_uri_to_local(uri, output_fpath)

    # print(by_nhm_id)    


    # for nhm_id, paths in by_nhm_id.items():
    #     for n, path in enumerate(sorted(paths), start=1):
    #         biosample_id = nhm_to_biosample_id[nhm_id]
    #         print(f"cp {path} {biosample_id}_{n}.jpg")
    

if __name__ == "__main__":
    main()