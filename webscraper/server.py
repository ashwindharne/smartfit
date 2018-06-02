from flask import Flask
app = Flask(__name__)

@app.route('/item/<string:id>')
def show_subpath(id):
    # show the subpath after /path/
    return 'id %s' % id