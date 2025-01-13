__author__ = 'Slim Dady'

import os
import secrets
from PIL import Image
from flask import  current_app




def save_picture(form_picture, folder='post_pics'):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    folder_path = os.path.join(current_app.root_path, 'static', folder)
    
    # Ensure the directory exists
    os.makedirs(folder_path, exist_ok=True)
    
    picture_path = os.path.join(folder_path, picture_fn)

    # Resize and save the image
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


'''

def count_likes(post_id):
    return Like.query.filter_by(post_id=post_id).count()

def count_comments(post_id):
    return Comment.query.filter_by(post_id=post_id).count()
'''