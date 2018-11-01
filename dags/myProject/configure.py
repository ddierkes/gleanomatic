from datetime import datetime, timedelta

startTime = datetime.combine(datetime.today() - timedelta(1), datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': startTime,
    'email': ['dhenry@mohistory.org'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=10),
}

sources = {
        "nih": {
            "name":"National Institutes of Health",
            "sets": {
                "profiles": {
                     "OAISource":"https://profiles.nlm.nih.gov/oai",
                     "OAIMetaDataPrefix":"oai_dc"
                }
            }
        },
        "cern": {
            "name": "CERN",
            "sets": {
                "docs": {
                     "OAISource":"https://cds.cern.ch/oai2d",
                     "OAIMetaDataPrefix":"oai_dc"
                }
            }
        }
}
