from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client.service_account import ServiceAccountCredentials
#test
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
KEY_FILE_LOCATION = 'smiling-timing-218217-1ad86f993db2.json'

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1cgW_CJnLNdBlfp-eC6a_Y66sBftyvdjM1tglX7h3yE8'
SAMPLE_RANGE_NAME = 'Sheet1!A5:D'

#SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
#SAMPLE_RANGE_NAME = 'Class Data!A2:E'

def initialize_sheets():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  sheets = build('sheets', 'v4', credentials=credentials)

  return sheets

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    #creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    #if os.path.exists('token.pickle'):
    #    with open('token.pickle', 'rb') as token:
    #        creds = pickle.load(token)
    ## If there are no (valid) credentials available, let the user log in.
    #if not creds or not creds.valid:
    #    if creds and creds.expired and creds.refresh_token:
    #        creds.refresh(Request())
    #    else:
    #        flow = InstalledAppFlow.from_client_secrets_file(
    #            'smiling-timing-218217-1ad86f993db2.json', SCOPES)
    #        creds = flow.run_local_server(port=0)
    #    # Save the credentials for the next run
    #    with open('token.pickle', 'wb') as token:
    #        pickle.dump(creds, token)

    #service = build('sheets', 'v4', credentials=creds)
    sheets = initialize_sheets()

    # Call the Sheets API
    sheet = sheets.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))

if __name__ == '__main__':
    main()