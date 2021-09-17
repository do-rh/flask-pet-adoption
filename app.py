"""Flask app for adopt app."""

from forms import AddPetForm, EditPetForm
from flask import Flask, redirect, render_template, flash

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.get('/')
def show_users():
    """Renders list of pet names and images and whether or not they are available"""
    pets = Pet.query.all()

    return render_template('index.html',
        pets = pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """Pet add form; handles pet adding"""

    form = AddPetForm()

    if form.validate_on_submit():
        #getting form data & adding pet to database
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        available = form.available.data

        new_pet = Pet(
            name=name, 
            species=species, 
            photo_url=photo_url,
            age=age,
            notes=notes,
            available=available
            )
        
        db.session.add(new_pet)
        db.session.commit()

        flash(f"{name} was added!")
        return redirect('/add')
    
    return render_template('pet_add_form.html', form=form) 
    

@app.route("/<int:pet_id>", methods=["GET", "POST"])
def show_and_edit_pet(pet_id):
    """Shows pet detail page and form for editing photo url, notes, and availability"""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj = pet)

    if form.validate_on_submit():
        #getting form data & updating pet db info
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()

        flash(f"{pet.name} was updated!")
        return redirect(f'/{pet_id}')
    
    return render_template('edit_pet.html', 
                            form=form,
                            pet = pet) 
    