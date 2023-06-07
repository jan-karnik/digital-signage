import sys
import os
import shutil
from flask import Flask, render_template, jsonify, redirect
from apscheduler.schedulers.background import BackgroundScheduler
import logging

app = Flask(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

nas_source_folder = sys.argv[1]

# Index of the next image to show
next_image_index = 0

# Index of the next video to show
next_video_index = 0


def can_navigate_to_videos():
    try:
        video_files = []

        files_in_video_folder = os.listdir("static/videos")

        for file in files_in_video_folder:
            if file.startswith("."):
                continue
            else:
                video_files.append(file)

        video_files_length = len(video_files)

        return video_files_length > 0

    except:
        # Failed to list static/videos folder --> that means we have no videos
        return False


def download_nas_files():
    global next_image_index
    next_image_index = 0

    path_to_images_on_nas = nas_source_folder + "/images"
    path_to_videos_on_nas = nas_source_folder + "/videos"
    path_to_images_local = "static/images"
    path_to_videos_local = "static/videos"

    images_on_nas = os.listdir(path_to_images_on_nas)
    videos_on_nas = os.listdir(path_to_videos_on_nas)

    app_images = os.listdir(path_to_images_local)

    app_videos = []

    try:
        app_videos = os.listdir(path_to_videos_local)
    except:
        print("No videos local yet")

    for current_image in app_images:
        os.remove(path_to_images_local + "/" + current_image)

    for current_video in app_videos:
        os.remove(path_to_videos_local + "/" + current_video)

    for image_file in images_on_nas:
        if image_file.startswith("."):
            continue

        source = path_to_images_on_nas + "/" + image_file
        destination = path_to_images_local + "/" + image_file
        if os.path.isfile(source):
            shutil.copy(source, destination)

    os.makedirs(os.path.dirname(path_to_videos_local + "/"), exist_ok=True)
    for video_file in videos_on_nas:
        if video_file.startswith("."):
            continue

        source = path_to_videos_on_nas + "/" + video_file
        destination = path_to_videos_local + "/" + video_file
        if os.path.isfile(source):
            shutil.copy(source, destination)


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(download_nas_files, "interval", minutes=1)
scheduler.start()


@app.route("/")
def home():
    global next_image_index
    template = "image.html"

    image_files = os.listdir("static/images")

    image_to_show = image_files[next_image_index]
    last_image_index = len(image_files) - 1

    if next_image_index == last_image_index:
        can_go_to_videos = can_navigate_to_videos()

        template_to_render = render_template(
            template,
            image=image_to_show,
            can_go_to_videos=can_go_to_videos,
            is_last_image=True,
        )

        next_image_index = 0

        return template_to_render

    template_to_render = render_template(
        template,
        image=image_to_show,
    )

    next_image_index = next_image_index + 1

    return template_to_render


@app.route("/video")
def video():
    global next_video_index
    template = "video.html"

    try:
        video_files = os.listdir("static/videos")

        last_video_index = len(video_files) - 1
        video_to_show = video_files[next_video_index]

        if next_video_index == last_video_index:
            next_video_index = 0

            template_to_render = render_template(
                template, video=video_to_show, go_to_images=True
            )

            return template_to_render
        else:
            next_video_index = next_video_index + 1

            template_to_render = render_template(
                template,
                video=video_to_show,
                go_to_images=False,
            )

            return template_to_render

    except Exception as e:
        print(e)
        return redirect("/", code=302)


@app.route("/api/image")
def get_image():
    global next_image_index

    image_files = os.listdir("static/images")

    image_to_show = image_files[next_image_index]
    index_of_last_image = len(image_files) - 1

    if next_image_index == index_of_last_image:
        next_image_index = 0

        can_go_to_videos = can_navigate_to_videos()

        return jsonify(
            {
                "image": image_to_show,
                "can_go_to_videos": can_go_to_videos,
                "is_last_image": True,
            }
        )

    next_image_index = next_image_index + 1

    return jsonify({"image": image_to_show, "can_go_to_videos": False})


@app.route("/api/video")
def get_video():
    global next_video_index

    video_files = []

    try:
        video_files = os.listdir("static/videos")

        video_to_show = video_files[next_video_index]
        index_of_last_video = len(video_files) - 1

        if next_video_index == index_of_last_video:
            next_video_index = 0

            return jsonify({"video": video_to_show, "go_to_images": True})
        else:
            next_video_index = next_video_index + 1

            return jsonify({"video": video_to_show, "go_to_images": False})

    except:
        next_video_index = 0
        print("No video files")

        return jsonify({"video": None, "go_to_images": True})


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
    try:
        app.run(debug=True, host="0.0.0.0", port=8081)
    except Exception as e:
        print("error with running")
        print(e)
