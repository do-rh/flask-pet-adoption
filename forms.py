"""Forms for adopt app."""
from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, BooleanField, SelectField
from wtforms.fields.core import BooleanField
from wtforms.validators import InputRequired, Optional, URL
from wtforms.widgets.core import Input


class AddPetForm(FlaskForm):
    """Form for adding new pets"""

    name = StringField("Pet Name", 
                        validators=[InputRequired()])
    species = SelectField("Species", 
                        choices=[('cat','Cat'), ('dog','Dog'),('porcupine','Porcupine')], 
                        validate_choice=True)
    photo_url = StringField("Image URL", validators=[URL(require_tld=True),Optional()])

    age = SelectField("Age", 
                        choices=[('baby','Baby'), ('young','Young'),('adult','Adult'), ('senior','Senior')], 
                        validate_choice=True,
                        )
    notes = TextField("Notes")
    available = SelectField("Adoptability", 
                        choices=[('True','Available for Adoption'), ('False','Not Available for Adoption')], 
                        validate_choice=True, coerce=bool)