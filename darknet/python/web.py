import os
import box
import darknet as dn
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

UPLOAD_FOLDER = os.path.join('python', 'static')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

net,meta = dn.load_app()
netf,metaf = dn.load_app_flower()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/info')
def inFormation():
    return render_template('info.html')

@app.route('/detect')
def detectPage():
    return render_template('detect.html')

@app.route('/detectflower')
def detectFlowerPage():
    return render_template('detectflower.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # f.save(secure_filename(f.filename))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("save image")
            print(app.config['UPLOAD_FOLDER'])
            print(filename)
            output_filename = box.write_detect(net,meta, app.config['UPLOAD_FOLDER'],filename)
            return render_template('detect.html', inputFile=filename, outputFile=output_filename)
        return render_template('detect.html')

@app.route('/uploaderflower', methods = ['GET', 'POST'])
def upload__flower_file():
    if request.method == 'POST':
        file = request.files['file']
        # f.save(secure_filename(f.filename))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("save image")
            print(app.config['UPLOAD_FOLDER'])
            print(filename)
            output_filename = box.write_detect(netf,metaf, app.config['UPLOAD_FOLDER'],filename)
            return render_template('detectflower.html', inputFile=filename, outputFile=output_filename)
        return render_template('detectflower.html')

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == "__main__":
    
    app.run()