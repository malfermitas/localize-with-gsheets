import httplib2
from googleapiclient import discovery


class Localizer:
    sheet = ''
    api_key = ''
    google_spreadsheet_hash = ''

    def __init__(self, sheet, api_key, google_spreadsheet_hash):
        self.sheet = sheet
        self.api_key = api_key
        self.google_spreadsheet_hash = google_spreadsheet_hash

    def set_sheet(self, sheet):
        self.sheet = sheet

    def save(self, file_path, key_column, value_column, localization_format):
        if file_path is None:
            raise RuntimeError('No file path specified!')
        if localization_format is None:
            raise RuntimeError('Format not specified!')

        discovery_url = ('https://sheets.googleapis.com/$discovery/rest?'
                         'version=v4')

        service = discovery.build(
            'sheets',
            'v4',
            http=httplib2.Http(),
            discoveryServiceUrl=discovery_url,
            developerKey=self.api_key)

        spreadsheet_id = self.google_spreadsheet_hash
        range_name = 'A1:G99'
        sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        sheets_names = []
        for sheet in sheets:
            sheets_names.append(sheet.get("properties", {}).get("title"))
        print(sheets_names)

        if self.sheet not in sheets_names:
            print(f"The sheet name {self.sheet} was not found in the spreadsheet. Aborting.")
            return None

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=f"{self.sheet}!{range_name}").execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            try:
                key_column_index = values[0].index(key_column)
            except ValueError:
                print(f"Key {key_column} was not found in sheet {self.sheet}. Aborting.")
                return None
            try:
                value_column_index = values[0].index(value_column)
            except ValueError:
                print(f"Values column named {value_column} was not found in sheet {self.sheet}. Aborting.")
                return None
            parse(localization_format, values, key_column_index, value_column_index, file_path=file_path)


def parse(format_os, values, key_column_index, value_column_index, file_path=None):
    file = open(file_path, 'w')
    for column_index in range(1, len(values), 1):
        try:
            key = values[column_index][key_column_index]
        except IndexError:
            key = None

        try:
            value = values[column_index][value_column_index]
        except IndexError:
            value = None

        if key is None and value is None:
            file.write("\n")
            continue

        if key.find("//") == 0:
            if format_os == 'iOS':
                file.write(f"{key}\n")
            elif format_os == 'android':
                file.write(f"<!-- {key[2:]} -->\n")
            continue

        if key is None and value is not None or key is not None and value is None or len(key) == 0:
            continue
        else:
            if format_os == 'iOS':
                file.write(f"\"{key}\" = \"{value}\";\n")
            elif format_os == 'android':
                file.write(f"<string name=\"{key}\">{value}</string>\n")
