#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$DIR/../SET"

BIGQUERY_DATASET=validation
BIGQUERY_TABLE=validation_table

DELETE='DELETE FROM `'"${PROJECT_ID}"'`.'"${BIGQUERY_DATASET}."''"${BIGQUERY_TABLE}"' WHERE true; '

do_query()
{
  bq query  --nouse_legacy_sql \
  $DELETE
}

read -p "Are you sure you want to delete all BigQuery entries inside $PROJECT_ID.$BIGQUERY_DATASET.$BIGQUERY_TABLE? Press [y] if yes: " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
  echo "Cleaning Up then..."
  do_query  2>/dev/null
fi


