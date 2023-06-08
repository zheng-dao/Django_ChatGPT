"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

#TO ENABLE THE API AND THE ACCOUNT FOR FIN VISIT THIS URL:
#https://console.developers.google.com/apis/api/analyticsreporting.googleapis.com/overview?project=791530239747

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'smiling-timing-218217-1ad86f993db2.json'
VIEWS = {
    'rs':'70529525',
    'sat':'57006968',
    #'ext':'89418156',
    #'calcoast':'220059864',
    }

def get_view_id(code):
    return VIEWS[code]

def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


d = {
        'reportRequests': [
        {
          'viewId': '',
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:sessions'}],
          'dimensions': [{'name': 'ga:country'}]
        }]
      }

def get_report(analytics, body=d, code=None):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  body['reportRequests'][0]['viewId'] = get_view_id(code)
  return analytics.reports().batchGet(
      body=body).execute()


def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response.

  Args:
    response: An Analytics Reporting API V4 response.
  """
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print(header + ': ', dimension)

      for i, values in enumerate(dateRangeValues):
        print('Date range:', str(i))
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print(metricHeader.get('name') + ':', value)


def main():
  code = 'rs'
  analytics = initialize_analyticsreporting()
  response = get_report(analytics, d, code=code)
  print_response(response)

if __name__ == '__main__':
  main()

