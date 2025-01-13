from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional
from flask_login import current_user
from flaskblog.models import User



class ChatForm(FlaskForm):
    message = TextAreaField('Message',validators=[Optional()])
    
                          
    picture = FileField('Upload Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField('Send')


    # Custom validator to ensure at least one field is filled
    def validate(self, *args, **kwargs):
        if not FlaskForm.validate(self):  # Call base validation
            return False
        if not self.message.data and not self.picture.data:
            self.message.errors.append("Please provide either a message or a picture.")
            return False
        return True
