import json
import pathlib
from collections import defaultdict
from typing import Optional, List

import click
from pydantic import BaseModel, parse_file_as


class AttributeDetail(BaseModel):
    name: str
    value: str


class Attribute(BaseModel):
    name: str
    value: Optional[str]
    reference: bool = False
    nmqual: List[AttributeDetail] = []
    valqual: List[AttributeDetail] = []

    def as_tsv(self):
        if self.reference:
            tsv_rep = f"<{self.name}>\t{self.value}\n"
        else:
            tsv_rep = f"{self.name}\t{self.value}\n"

        return tsv_rep


class File(BaseModel):
    path: pathlib.Path
    size: int
    attributes: List[Attribute] = []


def attributes_to_dict(attributes: List[Attribute]) -> dict:

    return {attr.name: attr.value for attr in attributes}


@click.command()
@click.argument("nhm_study_pagetab_json_fpath")
@click.argument("copo_output_json_fpath")
def main(nhm_study_pagetab_json_fpath, copo_output_json_fpath):

    file_list = parse_file_as(List[File], nhm_study_pagetab_json_fpath)

    with open(copo_output_json_fpath) as fh:
        raw_copo = json.load(fh)

    nhm_ids_in_copo = set(raw_copo["specimen_id"].values())

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


    by_nhm_id = defaultdict(list)
    for file in file_list:
        attr_dict = attributes_to_dict(file.attributes)
        nhm_barcode = attr_dict["NHMUK barcode"]
        nhm_id = f"NHMUK{nhm_barcode}"
        if nhm_id in nhm_ids_in_copo:
            by_nhm_id[nhm_id].append(file.path)
    


    for nhm_id, paths in by_nhm_id.items():
        for n, path in enumerate(sorted(paths), start=1):
            biosample_id = nhm_to_biosample_id[nhm_id]
            print(f"cp {path} {biosample_id}_{n}.jpg")
    

if __name__ == "__main__":
    main()