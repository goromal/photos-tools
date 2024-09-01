import logging
import os
import requests

from easy_google_auth.auth import getGoogleService
from photos_tools.defaults import PhotosToolsDefaults as PTD

class Photo(object):
    def __init__(self, data):
        self.id = data["id"]
        self.filename = data["filename"]
        self.url = data["baseUrl"]
        if "video" in data["mediaMetadata"]:
            self.is_video = True
            self.download_url = self.url + "=dv"
        else:
            self.is_video = False
            self.download_url = self.url + "=d"

    def toString(self):
        start_link = f"\033]8;;{self.url}\033\\"
        start_dlink = f"\033]8;;{self.download_url}\033\\"
        end_link = "\033]8;;\033\\"
        return f"{start_link}{self.filename}{end_link}{' (VIDEO)' if self.is_video else ''} - {start_dlink}DOWNLOAD{end_link}"

    def __repr__(self):
        return self.toString()

class PhotosService(object):
    def _check_valid_interface(func):
        def wrapper(self, *args, **kwargs):
            if self.service is None:
                raise Exception("Photos interface not initialized properly; check your secrets")
            return func(self, *args, **kwargs)
        return wrapper
    
    def __init__(self, **kwargs):
        self.enable_logging = PTD.getKwargsOrDefault("enable_logging", **kwargs)
        if self.enable_logging:
            logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
        self.service = None
        try:
            self.service = getGoogleService(
                "photoslibrary",
                "v1",
                PTD.getKwargsOrDefault("photos_secrets_file", **kwargs),
                PTD.getKwargsOrDefault("photos_refresh_token", **kwargs),
                headless=True
            )
        except:
            pass
    
    @_check_valid_interface
    def getFavoritedPhotos(self):
        favorited_photos = []
        next_page_token = None

        while True:
            response = self.service.mediaItems().search(body={
                'filters': {
                    'featureFilter': {
                        'includedFeatures': ['FAVORITES']
                    }
                },
                'pageSize': 100,
                'pageToken': next_page_token
            }).execute()

            if 'mediaItems' in response:
                favorited_photos.extend(response['mediaItems'])
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        return [Photo(p) for p in favorited_photos]

    def downloadPhoto(self, photo, dl_path):
        if not os.path.exists(dl_path):
            logging.info(f"Creating downloads path {dl_path}")
            os.makedirs(dl_path)
        
        logging.info(f"Requesting {photo.download_url}...")
        response = requests.get(photo.download_url)

        if response.status_code == 200:
            file_path = os.path.join(dl_path, photo.filename)
            logging.info(f"Downloading to {file_path}...")
            with open(file_path, "wb") as file:
                file.write(response.content)
            return True
        else:
            logging.error(f"Request failed for {photo.id}")
            return False
