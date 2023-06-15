from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zoo.db'
db = SQLAlchemy(app)


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(50))
    breed = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))

    def __repr__(self):
        return f"Animal(species='{self.species}', breed='{self.breed}', age={self.age}, gender='{self.gender}')"


@app.route('/')
def index():
    animal_counts = Animal.query.with_entities(Animal.species, db.func.count()).group_by(Animal.species).all()
    return render_template('index.html', animal_counts=animal_counts)


@app.route('/animals')
def animals():
    species = request.args.get('species')
    age = request.args.get('age')

    animals = Animal.query
    if species:
        animals = animals.filter_by(species=species)
    if age:
        animals = animals.filter_by(age=age)

    animals = animals.all()
    return render_template('animals.html', animals=animals)


@app.route('/animal/<int:animal_id>', methods=['GET', 'POST', 'DELETE'])
def animal(animal_id):
    animal = Animal.query.get(animal_id)

    if request.method == 'POST':
        animal.species = request.form['species']
        animal.breed = request.form['breed']
        animal.age = request.form['age']
        animal.gender = request.form['gender']
        db.session.commit()
        return redirect(url_for('index'))

    if request.method == 'DELETE':
        db.session.delete(animal)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('animal.html', animal=animal)


@app.route('/about')
def about():
    return render_template('about.html')


with app.app_context():
    db.create_all()