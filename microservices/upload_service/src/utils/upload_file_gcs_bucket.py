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

""" Upload file to gcs bucket function """

from common.config import BUCKET_NAME
from google.cloud.storage import Blob
from google.cloud import storage
from common.config import STATUS_IN_PROGRESS, STATUS_SUCCESS, STATUS_ERROR


def upload_file(case_id, uid, file):
  client = storage.Client()
  bucket = client.get_bucket(BUCKET_NAME)
  blob_name = f"{case_id}/{uid}/{file.filename}"
  blob = Blob(blob_name, bucket)
  blob.upload_from_file(file.file)
  return STATUS_SUCCESS


def upload_json_file(case_id, uid, input_data, content_type='application/pdf'):
  destination_blob_name = f"{case_id}/{uid}/input_data_{case_id}_{uid}.json"
  storage_client = storage.Client()
  bucket = storage_client.bucket(BUCKET_NAME)
  blob = bucket.blob(destination_blob_name)
  blob.upload_from_string(input_data, content_type)
  print(case_id + uid + input_data)
  return STATUS_SUCCESS
