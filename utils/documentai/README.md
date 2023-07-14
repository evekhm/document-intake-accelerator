# Table of contents

- [Document AI Utilities](#document-ai-utilities)
  - [Prerequisites](#prerequisites)
    - [Install required libraries](#install-required-libraries)
    - [Set env variables](#set-env-variables)
    - [Create Service Account Key](#create-service-account-key)
    - [Verify assigned roles/permissions](#verify-assigned-rolespermissions)
    - [Setup application default authentication](#setup-application-default-authentication)
  - [Utilities and tools for CDA](#utilities-and-tools-for-cda)
    - [Batch load into DocAI WareHouse](#batch-load-into-docai-warehouse)
    - [Classifier/Splitter Test](#classifiersplitter-test)
    - [Extraction Test](#extraction-test)
    - [Sort and Copy PDF files](#sort-and-copy-pdf-files)
    - [Get raw JSON output](#get-raw-json-output)
    - [Delete specific Firestore documents](#delete-specific-firestore-documents)

# Document AI Utilities

Below utility scripts help you debug DocumentAI for CDA Engine.

## Prerequisites

 ### Install required libraries 
```shell
    cd utils/documentai
    pip install -r requirements.txt
```

### Set env variables
Project you will be running experiments in:
```shell
  export PROJECT_ID=
  gcloud config set project $PROJECT_ID    
 ```

For each utility you might need an additional environment variables, they will be listed then.

### Create Service Account Key
You will need service account and service account key to execute utility scripts (via `GOOGLE_APPLICATION_CREDENTIALS` environment variable pointing to the service account key).

* Make sure to disable Organization Policy  preventing Service Account Key Creation
```shell
gcloud services enable orgpolicy.googleapis.com
gcloud org-policies reset constraints/iam.disableServiceAccountKeyCreation --project=$PROJECT_ID
```

* Create Service Account 

```shell
  export SA_NAME=docai-utility-sa
  export SA_EMAIL=${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
  gcloud iam service-accounts create $SA_NAME \
          --description="Service Account for calling DocAI API and Document Warehouse API" \
          --display-name="docai-utility-sa"  

```

* Generate and Download Service Account key
```shell
  export KEY=${PROJECT_ID}_${SA_NAME}.json                     
  gcloud iam service-accounts keys create ${KEY}  --iam-account=${SA_EMAIL}
  export GOOGLE_APPLICATION_CREDENTIALS=${KEY}
```

* Assign required roles
** Following roles are required for all utilityies. 
* 

For each utility additional dedicated roles will be listed when required. 

Following Roles need to be granted:
* For The DOCAI_PROJECT_ID:
  * `roles/documentai.apiUser`
  * `roles/documentai.editor`
  * `roles/logging.viewer`
* For the PROJECT_ID Project:
  * `roles/storage.objectViewer`

### Verify assigned roles/permissions

* Verify assigned roles/permissions (you will need to have `getIamPolicy` role for both projects to see a list of assigned permissions):
```shell
gcloud projects get-iam-policy $PROJECT_ID --flatten="bindings[].members" --format='table(bindings.role)' --filter="bindings.members:${SA_EMAIL}"
gcloud projects get-iam-policy $DOCAI_PROJECT_ID --flatten="bindings[].members" --format='table(bindings.role)' --filter="bindings.members:${SA_EMAIL}"
```

As an alternative, following commands below will create Service Account with required permissions (though account executing commands must have permissions to create the role bindings, which might not always be a case):
```shell
# DOCAI Access
gcloud projects add-iam-policy-binding $DOCAI_PROJECT_ID \
        --member="serviceAccount:${SA_EMAIL}" \
        --role="roles/documentai.apiUser"
gcloud projects add-iam-policy-binding $DOCAI_PROJECT_ID \
        --member="serviceAccount:${SA_EMAIL}" \
        --role="roles/documentai.editor"

gcloud projects add-iam-policy-binding $DOCAI_PROJECT_ID \
        --member="serviceAccount:${SA_EMAIL}" \
        --role="roles/logging.viewer"
        
gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:${SA_EMAIL}" \
        --role="roles/storage.objectViewer"
        
     
export KEY=${PROJECT_ID}_${SA_NAME}.json                     
gcloud iam service-accounts keys create ${KEY} \
        --iam-account=${SA_EMAIL}
                
export GOOGLE_APPLICATION_CREDENTIALS=${KEY}
```


### Setup application default authentication
```shell
gcloud auth application-default login
```

## Utilities and tools for CDA

### Batch load into DocAI WareHouse

#### Prerequisites 
1. Make sure to follow ALL steps as described in the [prerequisites](#prerequisites) and export all variables as listed in there.
  - `GOOGLE_APPLICATION_CREDENTIALS`
  - `SA_NAME`
  - `SA_EMAIL`
  - `PROJECT_ID`
2. For this exercise you will need to have [Document Ai Warehouse provisioned](https://cloud.google.com/document-warehouse/docs/quickstart) in your GCP environment prior to any further steps,

3. Create DocAI processor (for example OCR processor) inside DocAI WH project: 
```shell
export PROCESSOR_ID=
```
4. Create GCS Bucket inside Docai WH project for storing output of the DocAI batch processing jobs:

```shell
export DOCAI_OUTPUT_BUCKET="$PROJECT_ID-docai-output"
gsutil mb gs://$DOCAI_OUTPUT_BUCKET
```
5. Set additional env variables:
```shell
  export DOCAI_WH_PROJECT_ID=$PROJECT_ID
  export CALLER_USER=${SA_EMAIL}
```
4. Add required roles/permissions for the service account created in [prerequisites](#prerequisites) steps:
```shell
  cd utils/documentai

  export DOCAI_WH_PROJECT_NUMBER=$(gcloud projects describe  "${DOCAI_WH_PROJECT_ID}" --format='get(projectNumber)')

  gcloud projects add-iam-policy-binding $DOCAI_WH_PROJECT_ID --member="serviceAccount:${SA_EMAIL}"  --role="roles/documentai.apiUser"
  gcloud projects add-iam-policy-binding $DOCAI_WH_PROJECT_ID --member="serviceAccount:${SA_EMAIL}"  --role="roles/contentwarehouse.documentAdmin"  
 ```

5. If Cloud Storage is in a different Project, make sure to add Cross-Project Access for the Docai WH service account and service account used to execute the script:
```shell
gcloud storage buckets add-iam-policy-binding  gs://<PATH-TO-YOUR-BUCKET> --member="serviceAccount:service-${DOCAI_WH_PROJECT_NUMBER}@gcp-sa-cloud-cw.iam.gserviceaccount.com" --role="roles/storage.objectViewer"
gcloud storage buckets add-iam-policy-binding  gs://<PATH-TO-YOUR-BUCKET> --member="serviceAccount:${SA_EMAIL}" --role="roles/storage.objectViewer"
```



**Description**:
Will use PDF form on the GCS bucket as an input and provide classification/splitter output using `classifier` processor from the CDA config file.

Make sure to do pre-requisite steps and set variables:
```shell
cd utils/documentai
export PROJECT_ID=
export API_DOMAIN=
export GOOGLE_APPLICATION_CREDENTIALS=
source ../../SET
```

### Classifier/Splitter Test

**Description**: 
Will use PDF form on he GCS bucket as an input and provide classification/splitter output using `classifier` processor from the CDA config file.

```shell
EXTERNAL=True;BASE_URL=https:/; python classify.py -f gs://<path_to_form>.pdf 
```

**Sample output:**

```shell
--(output omitted)--
Classification output (sub-documents split per pages):
gs://docs_for_testing/Package-combined.pdf
  {'predicted_class': 'fax_cover_page', 'predicted_score': 0.91, 'pages': (0, 0)}
  {'predicted_class': 'health_intake_form', 'predicted_score': 0.96, 'pages': (1, 1)}
  {'predicted_class': 'pa_form_texas', 'predicted_score': 0.92, 'pages': (2, 2)}
  {'predicted_class': 'pa_form_cda', 'predicted_score': 0.99, 'pages': (3, 3)}

```

### Extraction Test
Make sure to do pre-requisite steps and set variables:
```shell
EXTERNAL=True;BASE_URL=https:/; python extract.py  -f gs://<path_to_form>.pdf -c form_class_name
```

**Sample output:**


### Sort and Copy PDF files
TODO

### Get raw JSON output
```shell
  export PROCESSOR_ID=
  export PROJECT_ID=<DOCAI_PROJECT_ID>
  python get_docai_json_response.py -f /local/path/to/file.pdf
```


### Delete specific Firestore documents
utils/database_cleanup_case_id_prefix.py - to delete specific records from the database using case_id prefix 


Setup cross Project access if you have not done so:
```shell
./setup/setup_docai_access.sh
```

When using Cloud Storage to send documents for DocAI, make sure, `DocumentAI Core Service Agent` service account has access to the cloud storage bucket.

Easiest, is to assign Cloud Storage Viewer rights to the whole project:

```shell
PROJECT_DOCAI_NUMBER=$(gcloud projects describe "$DOCAI_PROJECT_ID" --format='get(projectNumber)')
SA_DOCAI="service-${PROJECT_DOCAI_NUMBER}@gcp-sa-prod-dai-core.iam.gserviceaccount.com"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA_DOCAI"  --role="roles/storage.objectViewer"  2>&1
gcloud projects get-iam-policy $PROJECT_ID --flatten="bindings[].members" --format='table(bindings.role)' --filter="bindings.members:${SA_DOCAI}"
```

Otherwise, assign Viewer Access per dedicated Bucket (replace `<YOUR_BUCKET_HERE>` accordingly):
```shell
  gcloud storage buckets add-iam-policy-binding  gs://<YOUR_BUCKET_HERE> --member="serviceAccount:$SA_DOCAI" --role="roles/storage.objectViewer"  2>&1

```
