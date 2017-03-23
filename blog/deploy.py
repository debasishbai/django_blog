import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

CLOUD_NAME = os.environ.get("CLOUD_NAME")
CLOUD_API_KEY = os.environ.get("CLOUD_API_KEY")
CLOUD_API_SECRET = os.environ.get("CLOUD_API_SECRET")
ENV_ROLE = os.environ.get("ENV_ROLE")


def upload_images(location):
    cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=CLOUD_API_KEY,
        api_secret=CLOUD_API_SECRET
        )
    pics = os.listdir(path)
    for pic in pics:
        cloudinary.uploader.upload(location + pic, public_id=pic)


if ENV_ROLE == "development":
    path = "/home/debasish/heroku_apps/debasishbai/blog/static/images/full/"
    upload_images(path)


if ENV_ROLE == "production":
    path = "/app/blog/static/images/full/"
    upload_images(path)
