"""
DAG describing Hive pipeline
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.dataproc_operator import DataprocWorkflowTemplateInstantiateInlineOperator

PROJECT_ID = 'wmt-data-search'
TEMPLATE_ID = 'wlt-demo-wf'
REGION_ID = 'us-central1'

BUCKET_ID = 'wlt-demo-wf'

start_date = datetime(2019, 1, 1)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': start_date,
    'email': ['airflow-monitoring@somedomain.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(dag_id='simple_dataproc_workflow_inline',
         default_args=default_args,
         start_date=start_date,
         schedule_interval=None) as dag:

    run_hive = DataprocWorkflowTemplateInstantiateInlineOperator(
        task_id='RunHiveWorkflow',
        project_id=PROJECT_ID,
        region=REGION_ID,
        template={
            "jobs": [
                {
                    "hiveJob": {
                        "queryFileUri": f"gs://{BUCKET_ID}/sql/1_load-data-job.sql",
                        "scriptVariables": {
                            "INPUT_PATH": f"gs://{BUCKET_ID}/dataset/records.tsv"
                        }
                    },
                    "stepId": "1_load-data-job"
                },
                {
                    "hiveJob": {
                        "queryFileUri": f"gs://{BUCKET_ID}/sql/2_read-data-job.sql",
                        "scriptVariables": {
                            "OUTPUT_PATH": f"gs://{BUCKET_ID}"
                        }
                    },
                    "prerequisiteStepIds": [
                        "1_load-data-job"
                    ],
                    "stepId": "2_read-data-job"
                }
            ],
            "placement": {
                "managedCluster": {
                    "clusterName": "two-node-cluster",
                    "config": {
                        "gceClusterConfig": {
                            "zoneUri": "us-central1-f"
                        },
                        "masterConfig": {
                            "diskConfig": {
                                "bootDiskSizeGb": 250
                            },
                            "machineTypeUri": "n1-standard-2"
                        },
                        "softwareConfig": {
                            "imageVersion": "1.3-deb9"
                        },
                        "workerConfig": {
                            "diskConfig": {
                                "bootDiskSizeGb": 250
                            },
                            "machineTypeUri": "n1-standard-2",
                            "numInstances": 2
                        }
                    }
                }
            }
        }
    )

    load_data = DummyOperator(
        task_id='DummyTask'
    )

    load_data >> run_hive




with DAG(dag_id='simple_dataproc_workflow_inline_autoscale',
         default_args=default_args,
         start_date=start_date,
         schedule_interval=None) as dag:

    run_hive = DataprocWorkflowTemplateInstantiateInlineOperator(
        task_id='RunHiveWorkflow',
        project_id=PROJECT_ID,
        region=REGION_ID,
        template={
            "jobs": [
                {
                    "hiveJob": {
                        "queryFileUri": f"gs://{BUCKET_ID}/sql/1_load-data-job.sql",
                        "scriptVariables": {
                            "INPUT_PATH": f"gs://{BUCKET_ID}/dataset/records.tsv"
                        }
                    },
                    "stepId": "1_load-data-job"
                },
                {
                    "hiveJob": {
                        "queryFileUri": f"gs://{BUCKET_ID}/sql/2_read-data-job.sql",
                        "scriptVariables": {
                            "OUTPUT_PATH": f"gs://{BUCKET_ID}"
                        }
                    },
                    "prerequisiteStepIds": [
                        "1_load-data-job"
                    ],
                    "stepId": "2_read-data-job"
                }
            ],
            "placement": {
                "managedCluster": {
                    "clusterName": "two-node-cluster",
                    "config": {
                        "gceClusterConfig": {
                            "zoneUri": "us-central1-f"
                        },
                        "masterConfig": {
                            "diskConfig": {
                                "bootDiskSizeGb": 250
                            },
                            "machineTypeUri": "n1-standard-2"
                        },
                        "softwareConfig": {
                            "imageVersion": "1.3-deb9"
                        },
                        "workerConfig": {
                            "diskConfig": {
                                "bootDiskSizeGb": 250
                            },
                            "machineTypeUri": "n1-standard-2",
                            "numInstances": 2,

                            #
                            # Autoscale reference
                            #
                            "autoscalingConfig": {
                                "policyUri": "projects/wmt-data-search/locations/us-central1/autoscalingPolicies/wmt-scale-policy_01"
                            }
                        }
                    }
                }
            }
        }
    )

    load_data = DummyOperator(
        task_id='DummyTask'
    )

    load_data >> run_hive
