import sys
import os
import shutil
from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

nas_source_folder = sys.argv[1]

index = 0


def download_nas_files():
    global index
    index = 0

    path_to_images_on_nas = nas_source_folder + "/images"
    path_to_videos_on_nas = nas_source_folder + "/videos"
    path_to_images_local = "static/images"
    path_to_videos_local = "static/videos"

    images_on_nas = os.listdir(path_to_images_on_nas)
    videos_on_nas = os.listdir(path_to_videos_on_nas)

    app_images = os.listdir(path_to_images_local)
    try:
        app_videos = os.listdir(path_to_videos_local)
    except:
        print("No videos local yet")

    for current_image in app_images:
        os.remove(path_to_images_local + "/" + current_image)

    for current_video in app_videos:
        os.remove(path_to_videos_local + "/" + current_video)

    print("Deleting server images & videos")

    for image_file in images_on_nas:
        if image_file.startswith("."):
            continue

        source = path_to_images_on_nas + "/" + image_file
        destination = path_to_images_local + "/" + image_file
        if os.path.isfile(source):
            shutil.copy(source, destination)
            print("Copied " + image_file)

    for video_file in videos_on_nas:
        if video_file.startswith("."):
            continue

        source = path_to_videos_on_nas + "/" + video_file
        destination = path_to_videos_local + "/" + video_file
        if os.path.isfile(source):
            shutil.copy(source, destination)
            print("Copied " + video_file)


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(download_nas_files, "interval", seconds=30)
scheduler.start()


@app.route("/")
def home():
    global index
    template = "image.html"
    image_files = os.listdir("static/images")
    image_to_show = image_files[index]
    last_image_index = len(image_files) - 1

    next_image = (image_files[index + 1 if index != last_image_index else 0],)

    if index == last_image_index:
        template_to_render = render_template(
            template, image=image_to_show, next_image=next_image
        )

        index = 0

        return template_to_render

    template_to_render = render_template(
        template,
        image=image_to_show,
        next_image=next_image,
    )

    index = index + 1

    return template_to_render


@app.route("/api/image")
def get_image():
    global index

    image_files = os.listdir("static/images")

    image_to_show = image_files[index]
    index_of_last_image = len(image_files) - 1

    if index == index_of_last_image:
        index = 0

        return jsonify({"image": image_to_show})

    index = index + 1

    return jsonify({"image": image_to_show})


@app.route("/api/images")
def image_list():
    image_files = os.listdir("static/images")

    return jsonify(image_files)


@app.route("/api/videos")
def video_list():
    try:
        video_files = os.listdir("static/videos")

        return jsonify(video_files)
    except:
        print("No local static videos yet")

        return jsonify([])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081)
