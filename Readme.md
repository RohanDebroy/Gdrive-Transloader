## GDrive Transloader

A small attempt at creating a transloader (an service that can upload file from one server to another).

It uses redis(I just started learning) to queue the tasks.

## How to authenticate

1. Go to [APIs Console](https://console.developers.google.com/iam-admin/projects) and make your own project.
2. Search for ‘Google Drive API’, select the entry, and click ‘Enable’.
3. Select ‘Credentials’ from the left menu, click ‘Create Credentials’, select ‘OAuth client ID’.
4. Now, the product name and consent screen need to be set -> click ‘Configure consent screen’ and follow the instructions. Once finished:

   - Select ‘Application type’ to be Web application.
   - Enter an appropriate name.
   - Input http://localhost:8080 for ‘Authorized JavaScript origins’.
   - Input http://localhost:8080/ for ‘Authorized redirect URIs’.
   - Click ‘Save’.

5. Click ‘Download JSON’ on the right side of Client ID to download client*secret*<really long ID>.json.
   The downloaded file has all authentication information of your application. Rename the file to “client_secrets.json” and place it in your working project directory.
