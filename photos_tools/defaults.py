import os

class PhotosToolsDefaults:
    PHOTOS_SECRETS_FILE = "~/secrets/google/client_secrets.json"
    PHOTOS_REFRESH_TOKEN = "~/secrets/google/refresh.json"
    ENABLE_LOGGING = False

    @staticmethod
    def getKwargsOrDefault(argname, **kwargs):
        argname_mapping = {
            "photos_secrets_file": PhotosToolsDefaults.PHOTOS_SECRETS_FILE,
            "photos_refresh_token": PhotosToolsDefaults.PHOTOS_REFRESH_TOKEN,
            "enable_logging": PhotosToolsDefaults.ENABLE_LOGGING,
        }
        return kwargs[argname] if (argname in kwargs and kwargs[argname] is not None) else argname_mapping[argname]
