
import os
import secrets
from PIL import Image
from flask import current_app
from flask_mail import Message
from flaskblog import mail
from flaskblog.models import Chat
from sqlalchemy import create_engine 
import os
from flask import url_for

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture.stream)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_chat_pic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/chat_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



def send_reset_email(user):
    token = user.get_reset_token()
    print(token,"................")  # For debugging purposes to check the token
    
    # Create the reset password URL
    reset_url = url_for('users.reset_token', token=token, _external=True)
    
    # Create the message object
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    
    # The body of the email includes the reset link
    msg.body = msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email, and no changes will be made.
'''

    
    # Send the email
    mail.send(msg)



def get_dynamic_chat_db(user1, user2):
    # Ensure 'chat_databases' directory exists
    if not os.path.exists('chat_databases'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Determine database name dynamically
    db_name = f"{min(user1, user2)}_{max(user1, user2)}.db"
    db_path = os.path.abspath(os.path.join('chat_databases', db_name))
    db_uri = f"sqlite:///{db_path}"

    # Manually create and bind the engine
    engine = create_engine(db_uri)


        # Ensure the chat table is created in the dynamic database
    Chat.__table__.create(bind=engine, checkfirst=True)

    return engine, db_uri
