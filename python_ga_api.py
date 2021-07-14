from apiclient.discovery import build
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'xxxxx.json'

def get_service():
    """
    Build Analytics Reporting API V4 service object.
    """
    credentials = Credentials.from_service_account_file(
        KEY_FILE_LOCATION, scopes=SCOPES
    )
    service = build(serviceName='analyticsreporting', version='v4', credentials=credentials)
    return service
    
def get_report(
    service, view_id, 
    start_date='7daysAgo', end_date='yesterday', 
    metrics=[], dimensions=[]
    ):
    return service.reports().batchGet(
            body={
                'reportRequests': [{
                    'viewId': view_id,
                    'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                    'metrics': [{'expression': m} for m in metrics],
                    'dimensions': [{'name': d} for d in dimensions],
                }]
            }).execute()
  
  
VIEW_ID = 'xxxxxxxx'
metrics = ['ga:sessions']
dimensions = ['ga:source', 'ga:medium']
start_date, end_date = '7daysAgo', 'yesterday'

service = get_service()
response = get_report(
                service, VIEW_ID,
                start_date, end_date,
                metrics, dimensions
                )


def res_to_df(res):
    report = res['reports'][0]
    dimensions = report['columnHeader']['dimensions']
    metrics = [m['name'] for m in report['columnHeader']['metricHeader']['metricHeaderEntries']]
    headers = [*dimensions, *metrics]
    
    data_rows = report['data']['rows']
    data = []
    for row in data_rows:
        data.append([*row['dimensions'], *row['metrics'][0]['values']])
    
    return pd.DataFrame(data=data, columns=headers)
    
df = res_to_df(response)
