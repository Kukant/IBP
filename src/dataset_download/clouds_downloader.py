from google_images_download import google_images_download
from src.cloud_types_map import cloud_types

from multiprocessing import Process

common_arguments = {
    "limit": 500,
    "print_urls": True,
    "chromedriver":'/usr/lib/chromium-browser/chromedriver'
}

response = google_images_download.googleimagesdownload()  # class initialization


def download_images(cloud_type):
    common_arguments["keywords"] = "{} cloud".format(cloud_type)
    response.download(common_arguments)


for cloud_type in cloud_types:
    p = Process(target=download_images, args=(cloud_type, ))
    p.start()

