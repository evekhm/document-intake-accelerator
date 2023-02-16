"""
Copyright 2022 Google LLC

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
import time
from google.cloud import storage
from common.utils.logging_handler import Logger
"""
Config module to setup common environment
"""

import os, json
# API clients
gcs = None


# ========= Overall =============================
PROJECT_ID = os.environ.get("PROJECT_ID", "")
if PROJECT_ID != "":
  os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
assert PROJECT_ID, "Env var PROJECT_ID is not set."


REGION = "us-central1"
PROCESS_TIMEOUT_SECONDS = 600


# Doc approval status, will reflect on the Frontend app.
STATUS_APPROVED = "Approved"
STATUS_REVIEW = "Need Review"
STATUS_REJECTED = "Rejected"
STATUS_PENDING = "Pending"
STATUS_IN_PROGRESS = "Processing"

STATUS_SUCCESS = "Complete"
STATUS_ERROR = "Error"
STATUS_TIMEOUT = "Timeout"

# ========= Document upload ======================
BUCKET_NAME = f"{PROJECT_ID}-document-upload"
TOPIC_ID = "queue-topic"
UPLOAD_API_PATH = "/upload_service/v1"
PROCESS_TASK_API_PATH = f"{UPLOAD_API_PATH}/process_task"
DOCUMENT_STATUS_API_PATH = "/document_status_service/v1"

# ========= Validation ===========================
BUCKET_NAME_VALIDATION = PROJECT_ID
PATH = f"gs://{PROJECT_ID}/Validation/rules.json"
PATH_TEMPLATE = f"gs://{PROJECT_ID}/Validation/templates.json"
BIGQUERY_DB = "validation.validation_table"
VALIDATION_TABLE = f"{PROJECT_ID}.validation.validation_table"

CLASSIFIER = "classifier"
CONFIG_BUCKET = os.environ.get("CONFIG_BUCKET")
CONFIG_FILE_NAME = "config.json"


def load_config(bucketname, filename):
  # Todo add optimization and check for the latest timestamp changed
  # Reload only if file changes detected
  # Currently re-loading each time
  Logger.info(f"load_config with bucket={bucketname}, filename={filename}")
  global gcs
  if not gcs:
    gcs = storage.Client()

  try:
    if bucketname and gcs.get_bucket(bucketname).exists():
      bucket = gcs.get_bucket(bucketname)
      blob = bucket.blob(filename)
      if blob.exists():
        data = json.loads(blob.download_as_text(encoding="utf-8"))
        return data
      else:
        print(f"___________file does not exist {filename} _____")
        print(f"___________gs://{bucketname}/{filename}  _____")
    else:
      print("___________bucket does not exist _____")
  except Exception as e:
    Logger.error(f"Error: while obtaining file from GCS gs://{bucketname}/{filename} {e}")
    return None

  # Fall-back to local file
  Logger.warning(f"Warning: Using local {filename}")
  json_file = open(os.path.join(os.path.dirname(__file__), "config", filename))
  return json.load(json_file)


def get_config(config_name):
  start_time = time.time()
  config = load_config(CONFIG_BUCKET, CONFIG_FILE_NAME)
  assert config, f"Unable to locate '{config_name} or incorrect JSON file'"
  select_config = config.get(config_name)
  Logger.info(f"{config_name}={select_config}")

  process_time = time.time() - start_time
  time_elapsed = round(process_time * 1000)
  Logger.info(f"Retrieving {config_name} took : {str(time_elapsed)} ms")
  return select_config


def get_parser_config():
  return get_config("parser_config")


def get_document_types_config():
  return get_config("document_types_config")


def get_docai_entity_mapping():
  return get_config("docai_entity_mapping")


def get_docai_settings():
  return get_config("settings_config")


# Fall back value (when auto-approval config is not available for the form) - to trigger Need Review State
def get_extraction_confidence_threshold():
  settings = get_docai_settings()
  return float(settings.get("extraction_confidence_threshold", 0.85))


# Fall back value (when auto-approval config is not available for the form) - to trigger Need Review State
def get_extraction_confidence_threshold_per_field():
  settings = get_docai_settings()
  return float(settings.get("field_extraction_confidence_threshold", 0.60))


#Prediction Confidence threshold for the classifier to reject any prediction
#less than the threshold value.
def get_classification_confidence_threshold():
  settings = get_docai_settings()
  return float(settings.get("classification_confidence_threshold", 0.85))


def get_classification_default_label():
  settings = get_docai_settings()
  return float(settings.get("classification_default_label"))


DOCUMENTS_TYPE_CONFIG = get_document_types_config()


APPLICATION_FORM_DISPLAY_NAME = "Application Form"
APPLICATION_FORM = "application_form"
SUPPORTING_DOC = "supporting_documents"
SUPPORTING_DOC_DISPLAY_NAME = "Supporting Documents"
SUPPORTED_DOC_TYPES = {
    APPLICATION_FORM: APPLICATION_FORM_DISPLAY_NAME,
    SUPPORTING_DOC: SUPPORTING_DOC_DISPLAY_NAME
}
# APPLICATION_FORMS = [k for k, v in DOCUMENTS_TYPE_CONFIG.items() if v.get("doc_type") == APPLICATION_FORM]
# Logger.info(f"APPLICATION_FORMS={APPLICATION_FORMS}")
# SUPPORTING_DOCS = [k for k, v in DOCUMENTS_TYPE_CONFIG.items() if v.get("doc_type") == SUPPORTING_DOC]
# Logger.info(f"SUPPORTING_DOCS={SUPPORTING_DOCS}")


def get_document_class_by_label(label_name):
  for k, v in get_document_types_config().items():
    if v.get("classifier_label") == label_name:
      doc_type = v.get("doc_type")
      if not doc_type or doc_type not in SUPPORTED_DOC_TYPES.keys():
        Logger.warning(f"Doc class {k} does not have a valid doc_type (should be in {SUPPORTED_DOC_TYPES.keys()}). Assigning {SUPPORTING_DOC} for now")
        doc_type = SUPPORTING_DOC
      return k, doc_type

  Logger.warning(f"{label_name} is not a valid classifier label listed in {DOCUMENTS_TYPE_CONFIG}.")

  return label_name, SUPPORTING_DOC


# ========= HITL and Frontend UI =======================

# List of database keys and extracted entities that are searchable
DB_KEYS = [
    "active",
    "auto_approval",
    "is_autoapproved",
    "matching_score",
    "case_id",
    "uid",
    "url",
    "context",
    "document_class",
    "document_type",
    "upload_timestamp",
    "extraction_score",
    "is_hitl_classified",
]
ENTITY_KEYS = [
    "name",
    "dob",
    "residential_address",
    "email",
    "phone_no",
]

### Misc

# Used by E2E testing. Leave as blank by default.
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
