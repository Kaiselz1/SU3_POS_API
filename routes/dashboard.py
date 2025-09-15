from app import app, abort

@app.route('/')
def dashboard():
    return 'dashboard'

@app.route('/admin')
def admin():
    abort(403)