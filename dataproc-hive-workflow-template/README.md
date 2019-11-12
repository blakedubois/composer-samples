## Overview
    Airflow DAG that triggeres Dataproc Workflow template. 
    Particular workflow template creates Hive table, load data from GS bucket, apply simple aggregation on it and
    save results into external table on GS. In another words emulates some simple ETL pipeline.

## Requirements:
- Python 3.6
- Dependencies in requirements.txt

## Prepare
- Copy dataset to GS bucket `gsutil cp records.tsv gs://<BUCKET>/dataset/`
- Load sql `gsutil cp -r sql/* gs://<BUCKET>/sql/`
- Load Workflow template `gcloud dataproc workflow-templates import wlt-demo-wf --source workflow.yml --region <REGION>`
