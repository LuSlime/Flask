from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[])
    picture = FileField('Add Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Post')

    def validate_form(self):
        if not FlaskForm.validate(self):  # Base validation
            return False
        if not self.title.data and not self.picture.data:  # Check if both are empty
            self.title.errors.append("Please provide a title or upload a picture.")
            return False
        return True
