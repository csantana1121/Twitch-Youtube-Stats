from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, Searchuser
from flask_sqlalchemy import SQLAlchemy
# from audio import printWAV # Audio not used yet
import time, random, threading
from turbo_flask import Turbo
from flask_bcrypt import Bcrypt
# from flask_behind_proxy import FlaskBehindProxy # Codio solution don't want to use yet
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from youtube import *
from twitchapi import *
import json


app = Flask(__name__)
# proxied = FlaskBehindProxy(app) # Codio solution not yet

app.config['SECRET_KEY'] = 'efefdc92b673d6000695ae349d5b853e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
# turbo = Turbo(app) #might cause problems

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')" 

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/about")
def about():
    return render_template('about.html', subtitle='About', text='This is an about page')

@app.route("/youtube", methods=['GET', 'POST'])
def youtube():
    form = Searchuser()
    if form.validate_on_submit():
        api_key = "AIzaSyCdon2Ht4qsO50eVJpu9nJO5iJx7TSIOhM"
        api_key2 = "AIzaSyAG-YgDxNNokUoSl8R3wPrakujPLXOE2fw"
        channel_id = get_channel_id(api_key2, form.username.data)
        json = get_stats(channel_id, api_key)
        values = extract_info_json(json)
        playlist_id = get_playlists_id(channel_id, api_key2)
        video_id = get_playlists_items(playlist_id, api_key2)
        video = video_url(video_id)
        print(video)
#         dtfr_without_vals = construct_dtfr()
#         dtfr_with_vals = insert_values_dtfr(dtfr_without_vals, values)
#         result = dtfr_with_vals.to_html()
#         text_file = open("templates/youtubedata.html", "w")
#         text_file.write(result)
#         text_file.close()
        
        return render_template('youtube.html', title='Twitch', form=form, image=values[-1], channel_name=values[0],text = values[1], date =values[6],country=values[2],views=values[3],subs=values[4],numvids=values[5],vidurl=video)
    return render_template('youtube.html', title='Twitch', form=form, image='', channel_name='', text ='', date='', country='', views= '', subs='',numvids='',vidurl='')

@app.route("/youtube_output")
def youtube_output():
    return render_template('youtubedata.html', title='Youtube Results')


@app.route("/twitch", methods=['GET', 'POST'])
def twitch():
    form = Searchuser()
    if form.validate_on_submit():
        user_query = get_user_query(form.username.data)
        user_info = get_response(user_query)

        
        user_id = user_info.json()['data'][0]['id']
        img_url = user_info.json()['data'][0]['profile_image_url']
        #print(user_id)
        #print(img_url)
        user_videos_query = get_user_videos_query(user_id)
        videos_info = get_response(user_videos_query)
            
        videos_info_json = videos_info.json()
        # print(videos_info_json)
        videos_info_json_data = videos_info_json['data']
        videos_info_json_data_reversed = videos_info_json_data[::-1]
        # print(videos_info_json_data_reversed)
            
        line_labels = []
        line_values = []
        title = form.username.data +'\'s Video Stats' 
        # print(title)
        for item in videos_info_json_data_reversed:
            if(len(item['title']) == 0):   
                line_labels.append('No Name')
            elif (len(item['title']) > 20):
                line_labels.append(item['title'][:20] + '...')
            else:
                line_labels.append(item['title'])
            line_values.append(item['view_count'])
#         print('success')
#         print(title)
#         print(line_labels)
#         print(line_values)
#         print(img_url)
#         print(max(line_values) + 10)
        return render_template('line_chart.html', title=title, max= max(line_values) + 10, labels=line_labels,values=line_values,img_url=img_url)
        # return redirect(url_for('twitch'))
    return render_template('twitch.html', title='Twitch', form=form)

# @app.route("/twitchchart")
# def twitchchart():
#     return render_template('line_chart.html', title=title, max= max(line_values) + 10, labels=line_labels,values=line_values,img_url=img_url)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        passwordhash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        username = db.session.query(User.id).filter_by(username=form.username.data).first() is not None
        if username is False:
            mail = db.session.query(User.id).filter_by(email=form.email.data).first() is not None
            if mail is False:
                user = User(username=form.username.data, email=form.email.data, password=passwordhash)
                db.session.add(user)
                db.session.commit()
                flash(f'Account created for {form.username.data}!', 'success')
                return redirect(url_for('home')) # if so - send to home page
            else:
                flash(f'That email is already taken please try another','danger')
                return redirect(url_for('register'))
        else:
            flash(f'That username is already taken please try another','danger')
            return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = db.session.query(User.id).filter_by(username=form.username.data).first() is not None
        if username is True:
            password = db.session.query(User.password).filter_by(username=form.username.data).first()
            password = password[0]
            if bcrypt.check_password_hash(password, form.password.data):
                remember = request.form.get('Remember') #on if checked, None if not checked
                if remember == 'on':
                    remember = True
                else:
                    remember = False
                print(remember)
                flash(f'Logged in as {form.username.data}!', 'success')
                user = User.query.filter_by(username=form.username.data).first()
                login_user(user, remember=remember)
                return redirect(url_for('profile'))
            else:
                flash(f'Wrong password for {form.username.data}!','danger')
                return redirect(url_for('login'))
        else:
            flash(f'Account does not exist for {form.username.data}!','danger')
            return redirect(url_for('login'))
    return render_template('login.html',title='Login',form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'Logged out', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")