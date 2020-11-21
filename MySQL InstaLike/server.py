from hashlib import sha256, md5
import mysql.connector
from sqlqueries import *
from PIL import Image, ImageShow
from datetime import datetime

sql_connection = mysql.connector.connect(user='Felix', 
                                         password='LittleVadim12',
                                         host='localhost',
                                         database='WeirInsta')

cursor = sql_connection.cursor()
current_user = object()

class User():

    def __init__(self, user_id, login, display_name, 
                 description):
        self.user_id = user_id
        self.login = login
        self.display_name = display_name
        self.description = description
        self.get_profile_pic()
        self.posts = []
        self.get_posts()

    def get_posts(self):
        cursor.execute(select_posts.format(self.user_id))
        for x in cursor:
            self.posts.append(x)

    def get_subs(self):
        pass

    def add_post(self):
        if self.logged == False:
            print("You are not logged")
            return
        pic, description, create_date = post_input()
        pic_name = str(datetime.now())
        pic_name = md5(pic_name.encode()).hexdigest()
        pic_hash = pic_name
        pic_name = ('Media/Posts/', str(self.user_id), '_', pic_name, '.jpg')
        pic_name = ''.join(pic_name)
        pic.save(pic_name)
        cursor.execute(insert_post, (self.user_id, pic_hash, description, create_date))
        sql_connection.commit()

    def subscribe_user(self):
        user_id = input("Enter a user id to subscribe: ")
        cursor.execute(select_user_byid.format(user_id))
        response = cursor.fetchone()
        if not response:
            print("Such user doesn't exist!")
            return
        cursor.execute(select_sub, (self.user_id, user_id))
        response = cursor.fetchone()
        if response:
            del response
            cursor.execute(delete_sub, (self.user_id, user_id))
            print("Unsibscribed")
        else:
            del response
            cursor.execute(insert_sub, (self.user_id, user_id))
            print("Subscribed")
        sql_connection.commit()

    def like_post(self):
        # First get likes
        post_id = input("Enter a post id: ")
        cursor.execute(select_like, (post_id, self.user_id))
        response = cursor.fetchone()
        cursor.execute(select_like_count.format(post_id))
        like = cursor.fetchone()[0]
        if response:
            print("You already liked this! Going back")
            like -= 1
            cursor.execute(delete_like, (self.user_id, post_id))
        else:
            like += 1
            cursor.execute(insert_like, (post_id, self.user_id))
        cursor.execute(update_like_count, (like, post_id))
        del response, like
        sql_connection.commit()

    def get_profile_pic(self):
        cursor.execute(select_profile_pic.format(self.user_id))
        pic = cursor.fetchone()
        pic = Image.open(f"Media/Profile/{self.user_id}_{pic[0]}.jpg", 'r')
        self.profile_pic = pic
        
    def show_user(self):
        print(self.user_id, self.login, self.display_name, self.description, self.logged, sep='|')
        # self.profile_pic.show()

def post_input():
    pic = input("Enter a picture path: ")
    pic = Image.open(pic, 'r')
    description = input("Enter a post description: ")
    create_date = str(datetime.now().date())
    return (pic, description, create_date)

def user_input(func=None):
    login = input("Enter a user login: ").lower()
    passwd = input("Enter a user password: ").encode()
    passwd = sha256(passwd).hexdigest()
    if func:
        display_name, bio, profile_pic = func()
        return (login, passwd, display_name, bio, profile_pic)
    else:
        return (login, passwd)

def user_input_reg():
    display_name = input("Enter a display name: ")
    bio = input("Enter a description: ")
    profile_pic = input("Enter a picture path: ")
    profile_pic = Image.open(profile_pic, 'r')
    return (display_name, bio, profile_pic)


def logging():
    global current_user
    print("Loggining:")
    cursor.execute(user_login, user_input())
    record = cursor.fetchone()
    if not record:
        print("Invalid login or password!")
        return
    current_user = User(*record)
    current_user.logged = True
    current_user.show_user()
    # Make a sql select to find user, otherwise 
    # tell a user that db hasn't this user

    # Then send information about user with json file

def register_user():
    print("Registration:")
    login, passwd, display_name, bio, profile_pic = user_input(user_input_reg)
    cursor.execute(select_user_bylogin.format(login))
    response = cursor.fetchone()
    if response:
        print("Such username already exists!")
        return
    del response
    cursor.execute(insert_user, (login, passwd, display_name, bio))
    last_id = cursor.lastrowid
    pic_name = str(last_id)
    pic_name = md5(pic_name.encode()).hexdigest()
    save_path = f"Media/Profile/{last_id}_{pic_name}.jpg"
    profile_pic.save(save_path)
    cursor.execute(insert_user_profile_pic, (last_id, pic_name))
    sql_connection.commit()

# register_user()
logging()
# current_user.add_post()
# current_user.subscribe_user()
