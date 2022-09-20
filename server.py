from flask import Flask, request, abort, send_file, jsonify
from werkzeug.utils import secure_filename
from flask.helpers import make_response, send_from_directory
from flask_cors import CORS, cross_origin
import os

import artifical_intellegence
import database
from photoitem import PhotoItem

load_images_dir = "downloads"
os.system('rm -rf ' + load_images_dir)
os.system('mkdir ' + load_images_dir)

db = database.Database()

ai = artifical_intellegence.AI(
                            database_path="dataset", 
                            batch_size=128, 
                            epochs=20, 
                            initLoad=False, 
                            weights_filename="dogandcats.hdf5")

app = Flask(__name__, static_folder="my-app/build", static_url_path="")

cors = CORS(app)


@app.route('/api', methods=['POST'])
@cross_origin()
def upload():
    f = request.files['file']
    filename = secure_filename(f.filename)
    f.save(load_images_dir + "/" + filename)
    photo_item = PhotoItem(load_images_dir + "/" + filename)
    ai.recognize_image(photo_item)
    outMap = photo_item.toMap()
    outMap.update({"isDog": int(photo_item.dogs_percent > photo_item.cats_percent)})
    return jsonify(outMap)


@app.route('/', methods=['GET'])
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == '__main__':
    app.run(threaded=True)

