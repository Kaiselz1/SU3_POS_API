import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from PIL import Image, ImageDraw, ImageFont
from models.user import db, User

user_bp = Blueprint("user_bp", __name__)

# --- Image Configuration ---
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

# --- Image functions ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file):
    if not file:
        return "No image uploaded"
    if not allowed_file(file.filename):
        return "Invalid file type (allowed: png, jpg, jpeg)"
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > MAX_FILE_SIZE:
        return "Image must be smaller than 2MB"
    return None

def add_watermark(image_path):
    img = Image.open(image_path).convert("RGBA")
    watermark_text = "@VIRAKYOTH@"
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(img)

    # --- Calculate text size (works for new Pillow versions) ---
    try:
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        # fallback for older Pillow
        text_width, text_height = font.getsize(watermark_text)

    # Bottom-right corner
    position = (img.width - text_width - 10, img.height - text_height - 10)
    draw.text(position, watermark_text, fill=(0, 0, 0, 128), font=font)

    # --- Fix for JPEG ---
    ext = os.path.splitext(image_path)[1].lower()
    if ext in ['.jpg', '.jpeg']:
        img = img.convert("RGB")  # JPEG cannot handle alpha

    img.save(image_path)
    img.close()

# --- CRUD ---
@user_bp.route('/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_crud():
    # --- Create ---
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        file = request.files.get('profile')

        # --- Validation ---
        if not user_name or not password:
            return jsonify({"message": "user_name and password are required"}), 400
        if User.query.filter_by(user_name=user_name).first():
            return jsonify({"message": "Username already exists"}), 409
        
        error = validate_image(file)
        if error:
            return jsonify({"message": error}), 400

        # --- Save image ---
        filename = secure_filename(file.filename)
        save_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        file.save(save_path)
        add_watermark(save_path)

        # --- Save user ---
        hashed_pw = generate_password_hash(password)
        new_user = User(user_name=user_name, password=hashed_pw, profile=f"uploads/{filename}")
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User created", 
            "id": new_user.id
        }), 201
    
    # --- Read ---
    elif request.method == 'GET':
        user_id = request.args.get('id')  # get id from query string

        if user_id:  # if id is provided, return single user
            user = User.query.get(user_id)
            if not user:
                return jsonify({"message": "User not found"}), 404
            return jsonify({
                "id": user.id,
                "user_name": user.user_name,
                "profile": user.profile
            })

        # if no id, return all users
        users = User.query.all()
        return jsonify([
            {"id": u.id, "user_name": u.user_name, "profile": u.profile}
            for u in users
        ])

    # --- Update ---
    elif request.method == 'PUT':
        data = request.form
        user_id = data.get('id')
        if not user_id:
            return jsonify({"message": "id is required"}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        if 'user_name' in data:
            user.user_name = data['user_name']
        if 'password' in data:
            user.password = generate_password_hash(data['password'])
        if 'profile' in request.files:
            file = request.files['profile']
            error = validate_image(file)
            if error:
                return jsonify({"message": error}), 400
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
            file.save(save_path)
            add_watermark(save_path)
            user.profile = f"uploads/{filename}"

        db.session.commit()
        return jsonify({"message": "User updated"}), 200

    # --- Delete ---
    elif request.method == 'DELETE':
        user_id = request.form.get('id')
        if not user_id:
            return jsonify({"message": "id is required"}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        file_path = os.path.join(current_app.root_path, 'static', user.profile)
        if os.path.exists(file_path):
            os.remove(file_path)

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200

