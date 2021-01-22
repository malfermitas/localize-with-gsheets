from localization import Localizer


def main():
    # Obtain an API key at https://console.developers.google.com/apis/credentials and paste it below
    apiKey = ''
    # Paste a hash of your google spreadsheet you want to get localization from
    spreadsheet_id = ''

    localizer = Localizer(sheet='Mobile', api_key=apiKey, google_spreadsheet_hash=spreadsheet_id)
    localizer.save(file_path="loc.txt", key_column="iOS", value_column="FR", localization_format="iOS")


if __name__ == '__main__':
    main()
