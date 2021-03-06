from google_images_download import google_images_download

from multiprocessing import Process

common_arguments = {
    "limit": 500,
    "print_urls": True,
    "chromedriver":'/usr/local/bin/chromedriver',
    "color": "blue"
}

response = google_images_download.googleimagesdownload()  # class initialization


def download_images(cloud_type):
    common_arguments["keywords"] = "{}".format(cloud_type)
    response.download(common_arguments)


random = ["books",
               "random things",
               "seats",
               "buildings",
               "cars",
               "faces",
               "jumper",
               "glass",
               "dog",
               "cat",
               "food",
               "gordon ramsey",
               "belts",
               "dark room",
               "black room",
               "lights",
               "stealing",
               "walls",
               "germany",
               "czech republic",
               "prague",
               "shows",
               "shoes",
               "mirror",
               "glasses",
               "wardrobe",
               "doing nothing",
               "catching fire",
               "friends",
               "world war",
               "bed",
               "trousers",
               "climbing",
               "squash play"]

cloud_types = ["clear sky blue"]

for cloud_type in cloud_types:
    p = Process(target=download_images, args=(cloud_type, ))
    p.start()

