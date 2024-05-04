# backend/server.py
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

# Configure MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:aryan8484@localhost:3306/dogs_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

# Dog model
class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=True)

# Create tables within the application context
with app.app_context():
    db.create_all()

# Image upload configuration
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/dogs', methods=['GET', 'POST'])
def dogs():
    if request.method == 'GET':
        dogs = Dog.query.all()
        result = [{'id': dog.id, 'name': dog.name, 'breed': dog.breed, 'age': dog.age, 'image': dog.image} for dog in dogs]
        return jsonify(result)
    elif request.method == 'POST':
        name = request.form.get('name')
        breed = request.form.get('breed')
        age = request.form.get('age')

        if 'image' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['image']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_dog = Dog(name=name, breed=breed, age=age, image=filename)
            db.session.add(new_dog)
            db.session.commit()
            return jsonify({'id': new_dog.id, 'name': new_dog.name, 'breed': new_dog.breed, 'age': new_dog.age, 'image': new_dog.image})

        return jsonify({'error': 'File type not allowed'})

@app.route('/api/dogs/<int:id>', methods=['DELETE'])
def delete_dog(id):
    dog = Dog.query.get(id)
    if not dog:
        return jsonify({'error': 'Dog not found'}), 404

    db.session.delete(dog)
    db.session.commit()
    return jsonify({'message': 'Dog adopted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
