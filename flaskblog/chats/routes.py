from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import current_user,login_required
from flaskblog.models import User, Chat
from flaskblog.chats.forms import ChatForm
from flaskblog.users.utils import save_chat_pic, get_dynamic_chat_db
from sqlalchemy.orm import  sessionmaker


chats = Blueprint('chats', __name__)





@chats.route("/chat_room", methods=['GET', 'POST'])
@login_required
def chat_room():

    if current_user.is_authenticated:
        friends = User.query.filter(User.id != current_user.id).all()
    return render_template('chat.html', title='Chat Room',   friends=friends)



@chats.route("/message/<username>", methods=['GET', 'POST'])
@login_required
def message(username):
    if current_user.is_authenticated:
       #get_dynamic_chat_db(current_user.username,username)
       engine, db_uri = get_dynamic_chat_db(current_user.username, username)
       
    Session = sessionmaker(bind=engine)
    session = Session()
    chats = session.query(Chat).filter(
        ((Chat.sender == current_user.username) & (Chat.receiver == username)) |
        ((Chat.sender == username) & (Chat.receiver == current_user.username))
    ).order_by(Chat.timestamp.asc()).all()
    
    user = User.query.filter_by(username=username).first()
    


    form = ChatForm()
    if form.validate_on_submit():
       
       if form.picture.data:
            picture_file = save_chat_pic(form.picture.data)  # Save the picture
       else:
            picture_file = None  # No picture uploaded


       chat = Chat(
            sender=current_user.username,
            receiver=username,
            message=form.message.data if form.message.data else '',
            image_file=picture_file
        )

       session.add(chat)
       session.commit()
        #flash('Message sent!', 'success')
       return redirect(url_for('chats.message', username=username))
    
    
    return render_template('message.html', title='Message', form=form, chats=chats, friend=user,)