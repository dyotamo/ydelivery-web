import glob

import cloudinary
import cloudinary.uploader

cloudinary.config(cloud_name='dzpauyp0q',
                  api_key='372117561346182',
                  api_secret='wtwVIAhR4nOniZuVXVfAaONI-3o')

with open('upload_photos.txt', 'w') as f:
    for filename in glob.glob('photos/*'):
        uploaded_file = cloudinary.uploader.upload(filename)
        print(uploaded_file, file=f)
        print(uploaded_file)
