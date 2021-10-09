import os
import sys
from urllib.parse import urlparse, unquote
import requests
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pySmartDL import SmartDL
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import shutil
from fake_useragent import UserAgent


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
    ):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session



def get_fileName(url):
    res = requests.get(url,stream=True, allow_redirects=True, headers = {"User-Agent":UserAgent().random})

    try:
        if 'filename' in res.headers.get('Content-Disposition'):
            fileName = res.headers.get(
                'Content-Disposition').split('filename=')[1].split(';')[0].replace('"', '')
        else:
            raise Exception
    except:
        fileName = os.path.basename(urlparse(unquote(res.url)).path)

    return fileName


def gdrive(url):
    if 'usp=drive_open' in url or 'view' in url:
        id = urlparse(url).path.replace('/file/d/', '').replace('/view', '')
        url = 'https://drive.google.com/uc?id={}&export=download'.format(id)
    else:
        id = urlparse(url).query.replace(
            'id=', '').replace('&export=download', '')
        url = 'https://drive.google.com/uc?id={}&export=download'.format(id)

    return url


def download(url):
    if not os.path.isdir('data'):
        os.mkdir('data')

    if 'drive.google.com' in url:
        url = gdrive(url)

    print("[*] Downloading : The file is being Downloaded.")
    try:
        if 'seedr.cc' in url:
            raise Exception

        obj = SmartDL(urls=url,dest='data/',progress_bar=True)
        obj.start()
        fileName=obj.get_dest()
        newfileName = get_fileName(url)
        os.rename(fileName,"data/"+newfileName)
        print("[*] Successful : File has been Download Successfully to "+fileName)
        return newfileName
        
    except Exception:
        print("[*] Downloading : The file is being Downloaded.")
        res = requests_retry_session().get(url=url, allow_redirects=True, headers = {"User-Agent":UserAgent().ff})
        fileName = get_fileName(url)

        totalFileSize = int(res.headers.get('content-length'))
        chunk_size = 1024
        num_bars = int(totalFileSize/chunk_size)
        with open('data/'+fileName, 'wb') as out_file:
            for data in tqdm(res.iter_content(chunk_size=chunk_size),total=num_bars, unit='KB', desc=fileName, leave=True, file=sys.stdout):                
                out_file.write(data)

        print("[*] Successful : File has been Download Successfully to "+fileName)
        return fileName

def authenticate():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth
    return GoogleDrive(gauth)


def uploader(srcFile, teamDriveId="0ABhY56uyjkd5Uk9PVA", parentDirId="1j2hZP0wW4b8ktMfA7vH-vjywN60xUF3F"):
    drive = authenticate()
    title = os.path.basename(srcFile)

    print("\n[*] Uploading : {} is being uploaded. Wait patiently.".format(title))
    file = drive.CreateFile({
        "title": title,
        "parents": [{
            "kind": "drive#fileLink",
            "teamDriveId": teamDriveId,
            "id": parentDirId,
        }]
    })

    file.SetContentFile(srcFile)
    file.Upload({"supportsAllDrives": True})
    file.InsertPermission({
        "type": "anyone",
        "value": "anyone",
        "role": "reader",
        "supportsAllDrives": True
    })
    print("[*] Successful : {} has been uploaded.".format(title))
    # print("[*] Download link : {}".format(file["alternateLink"]))

    return str(file["alternateLink"])

def url_shorten(url):
    url = "http://ouo.io/api/riEs7aPT?s={}".format(url)
    with requests.get(url) as response:
        return response.text

def upDown(url):
    try:
        fileName ='data/' + download(url)
        gdrive_link = uploader(fileName)
        shutil.rmtree(fileName)
        return url_shorten(gdrive_link)
    except:
        return 'Check the Url or Try after sometimes'