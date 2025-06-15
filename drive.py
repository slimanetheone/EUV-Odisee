from google.oauth2 import service_account
from googleapiclient.discovery import build

# Vervang dit door jouw JSON key bestand
SERVICE_ACCOUNT_FILE = 'credentialsgdrive.json'

# Folder ID die je wilt uitlezen
FOLDER_ID = '1tPFuRJ5qFkVg05MNXlLe3zBUpNvgOA6U'

# Scopes voor lezen Drive metadata
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    # Credentials laden
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Drive API client aanmaken
    service = build('drive', 'v3', credentials=creds)

    # Query om alle niet-verwijderde bestanden in folder op te halen
    query = f"'{FOLDER_ID}' in parents and trashed = false"

    # API call om bestanden op te halen
    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType)"
    ).execute()

    items = results.get('files', [])

    if not items:
        print('Geen bestanden gevonden in folder.')
    else:
        print(f'Bestanden in folder {FOLDER_ID}:')
        for item in items:
            print(f"{item['name']} (ID: {item['id']}) [{item['mimeType']}]")

if __name__ == '__main__':
    main()
