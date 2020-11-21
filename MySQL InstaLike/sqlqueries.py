create_table_users = ("CREATE TABLE IF NOT EXISTS Users (\
    user_id INT AUTO_INCREMENT PRIMARY KEY,\
    nickname VARCHAR(30) NOT NULL,\
    display_name VARCHAR(50),\
    bio VARCHAR(150) DEFAULT '',\
    password VARCHAR(64) NOT NULL);")

create_table_user_pic = "CREATE TABLE \
    IF NOT EXISTS Users_profile_pic (\
    pic_path VARCHAR(40) NOT NULL,\
    user_id INT,\
    FOREIGN KEY(user_id)\
        REFERENCES Users(user_id));"

create_table_posts = "CREATE TABLE IF NOT EXISTS Posts (\
    post_id INT AUTO_INCREMENT PRIMARY KEY,\
    owner_id INT,\
    FOREIGN KEY (owner_id)\
        REFERENCES Users(user_id),\
    pic_path VARCHAR(40) NOT NULL,\
    likes INT DEFAULT 0,\
    description VARCHAR(150) DEFAULT '',\
    create_date DATE);"

create_table_likes = "CREATE TABLE IF NOT EXISTS Post_likes (\
    post_id INT,\
    FOREIGN KEY (post_id)\
        REFERENCES Posts(post_id),\
    user_id INT,\
    FOREIGN KEY (user_id)\
        REFERENCES Users(user_id));"

# user_id - тот, на кого подписаны, sub_id - кто подписан
create_table_subs = "CREATE TABLE IF NOT EXISTS User_subs (\
    user_id INT,\
    FOREIGN KEY (user_id)\
        REFERENCES Users(user_id),\
    sub_id INT,\
    FOREIGN KEY (sub_id)\
        REFERENCES Users(user_id));"

insert_user = "INSERT INTO Users \
    (nickname, password, display_name, bio)\
    VALUES (%s, %s, %s, %s);"

insert_user_profile_pic = "INSERT INTO Users_profile_pic\
    (user_id, pic_path) VALUES (%s, %s);"

insert_post = "INSERT INTO Posts \
    (owner_id, pic_path, description, create_date)\
    VALUES (%s, %s, %s, %s);"

insert_like = "INSERT INTO Post_likes \
    (post_id, user_id) VALUES (%s, %s);"

# user_id - тот, на кого подписаны, sub_id - кто подписан
insert_sub = "INSERT INTO User_subs \
    (user_id, sub_id) VALUES (%s, %s);"

select_user_bylogin = "SELECT nickname FROM Users WHERE nickname = '{}';"

select_user_byid = "SELECT user_id FROM Users WHERE user_id = {};"

user_login = "SELECT user_id, nickname, display_name, bio\
    FROM Users WHERE \
    nickname = %s AND password = %s;"

select_sub = "SELECT sub_id FROM User_subs\
    WHERE user_id = %s AND sub_id = %s;"

select_posts = "SELECT * FROM Posts\
    WHERE owner_id = {};"

select_like = "SELECT * FROM Post_likes\
    WHERE post_id = %s AND user_id = %s;"

select_profile_pic = "SELECT pic_path FROM Users_profile_pic\
    WHERE user_id = {};"

select_like_count = "SELECT likes FROM Posts\
    WHERE post_id = {};"

update_like_count = "UPDATE Posts\
    SET likes = %s\
    WHERE post_id = %s;"

delete_like = "DELETE FROM Post_likes\
    WHERE user_id = %s AND post_id = %s;"

delete_sub = "DELETE FROM User_subs\
    WHERE user_id = %s AND sub_id = %s;"

if __name__ == "__main__":
    exit()