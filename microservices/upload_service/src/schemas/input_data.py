"""
Copyright 2024 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""
Schema for  Model for Upload  JSON API's
"""
from typing import Optional
from pydantic import BaseModel


class InputData(BaseModel):
  """json input  Pydantic Model"""
  case_id: Optional[str]
  name: str
  document_class: str
  context: str
  dob: str
  employer_name: Optional[str]
  employer_phone_no: Optional[str]
  ssn: Optional[str]
  phone_no: Optional[str]
  application_apply_date: Optional[str]
  mailing_address: Optional[str]
  mailing_city: Optional[str]
  mailing_zip: Optional[str]
  residential_address: Optional[str]
  work_end_date: Optional[str]
  sex: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "case_id": "123A",
            "name": "Jon",
            "employer_name": "Quantiphi",
            "employer_phone_no": "9282112222",
            "context": "Callifornia",
            "dob": "7 Feb 1997",
            "document_class": "unemployment",
            "ssn": "1234567",
            "phone_no": "9730388333",
            "application_apply_date": "2022/03/16",
            "mailing_address": "Arizona USA",
            "mailing_city": "Phoniex",
            "mailing_zip": "123-33-22",
            "residential_address": "Phoniex , USA",
            "work_end_date": "2022/03",
            "sex": "Female"
        }
    }
