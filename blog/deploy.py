import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
import database_config


CLOUD_NAME = os.environ.get("CLOUD_NAME")
CLOUD_API_KEY = os.environ.get("CLOUD_API_KEY")
CLOUD_API_SECRET = os.environ.get("CLOUD_API_SECRET")
ENV_ROLE = os.environ.get("ENV_ROLE")


def config():
    cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=CLOUD_API_KEY,
        api_secret=CLOUD_API_SECRET
    )


def upload_images(location):
    config()
    pics = os.listdir(location)
    count = 0
    for pic in pics:
        cloudinary.uploader.upload(location + pic, public_id=pic)
        count += 1
        print "Uploading . . . ", pic
    print "Images Uploaded: ", count


def destroy(role):
    config()
    if role == "development":
        cur = database_config.local_db()
    elif role == "production":
        cur = database_config.server_db()
    cur.execute("select image_name from blog_post where published_date is not null")
    get_image_names = cur.fetchall()
    if get_image_names[0][0] is None:
        print "No unused images on DB"
        return
    db_image_names = [names[0] for names in get_image_names]
    image_details = cloudinary.api.resources(max_results=100)
    cdn_image_names = [i["public_id"] for i in image_details["resources"]]
    print "No.of Images on CDN:", len(cdn_image_names)
    count = 0
    for image in cdn_image_names:
        if image not in db_image_names:
            cloudinary.uploader.destroy(image)
            count += 1
            print "Deleting . . . ", image
    print "Images Deleted: ", count


def choice(path, role):
    print """
        1. Upload Images
        2. Delete Images
        """
    choose = raw_input("Enter: ")
    if choose == "1":
        upload_images(path)
    elif choose == "2":
        destroy(role)


def environment():
    if ENV_ROLE == "development":
        path = "/path/"
        choice(path, ENV_ROLE)

    if ENV_ROLE == "production":
        path = "/path/"
        choice(path, ENV_ROLE)


if __name__ == "__main__":
    environment()
