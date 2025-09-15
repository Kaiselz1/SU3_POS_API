from app import app, abort

@app.route('/')
def dashboard():
    return '<h1>dashboard</h1>'

@app.route('/admin')
def admin():
    abort(403)

@app.route('/list')
def list():
    arr = [1,2]
    arr[3] = 5  # This will raise an IndexError
    return '<h1>list</h1>'