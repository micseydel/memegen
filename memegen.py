from flask import Flask, request, g, redirect, url_for, render_template

import memegenerator
import dao

DATABASE = 'memegen.db'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    return redirect(url_for("get_images"))


@app.route('/image', methods=['GET'])
def get_images():
    db_images = dao.get_images(get_db())
    images = []
    for image_id, filename in db_images:
        id_url = url_for('get_image', image_id=image_id)
        img_url = url_for('static', filename='images/%s' % filename)
        images.append({'id_url': id_url, 'img_url': img_url})

    form_data = {'images': images, 'to_upload': True}
    return render_template('grid.html', form_data=form_data)


@app.route('/image/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = {'id': image_id, 'name': dao.get_image_path(get_db(), image_id)}
    from pprint import pprint; pprint(image)
    return render_template('make_meme.html', image=image)


@app.route('/image', methods=['POST'])
def post_images():
    img = request.files['image']
    img.save('static/images/%s' % img.filename)
    img_id = dao.create_image(get_db(), img.filename)
    return redirect(url_for("get_image", image_id=img_id))


@app.route('/meme/<int:meme_id>', methods=['GET'])
def get_meme(meme_id):
    return redirect(url_for('static', filename='memes/%d.png' % meme_id))


@app.route('/meme', methods=['GET'])
def get_memes():
    db_images = dao.get_memes(get_db())
    images = []
    for img_id, _, _, _ in db_images:
        img_url = id_url = url_for('static', filename='memes/%d.png' % img_id)
        images.append({'img_url': img_url, 'id_url': id_url})

    form_data = {'images': images, 'to_upload': False}
    return render_template('grid.html', form_data=form_data)


@app.route('/meme', methods=['POST'])
def post_meme():
    image_id = int(request.form['image'])
    top = request.form['top']
    bottom = request.form['bottom']

    meme_id = dao.create_meme(get_db(), image_id, top, bottom)
    image_name = dao.get_image_path(get_db(), image_id)
    memegenerator.gen_meme(image_name, top, bottom, meme_id)

    return redirect(url_for('static', filename='memes/%d.png' % meme_id))


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = dao.connect_db(app)
    return db


def main():
    import sys
    if '-d' in sys.argv or '--debug' in sys.argv:
        print 'Running in debug mode'
        app.debug = True
    print 'Server is available externally'
    app.run("0.0.0.0")


# if __name__ == '__main__':
main()
