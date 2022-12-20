import sys
from datetime import datetime
from typing import List, Dict, Optional

import requests
from pydantic import BaseModel


class Relationship(BaseModel):
    source: str
    type: str
    target: str
        

class Characteristic(BaseModel):
    text: str
    tag: Optional[str]
    unit: Optional[str]
    

class BioSample(BaseModel):
    name: str
    accession: str
    taxId: int
    submitted: datetime
    
    characteristics: Dict[str, List[Characteristic]]
    relationships: List[Relationship] = []
        
def get_biosample_record(sample_id):
    request_uri = f"http://www.ebi.ac.uk/biosamples/samples/{sample_id}"
    
    r = requests.get(request_uri)
    
    if not r.ok:
        r.raise_for_staus()
        sys.exit()
    
    return BioSample.parse_raw(r.content)