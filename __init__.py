import hashlib
import sqlite3
import time
import datetime
import random
import uuid
from passlib.hash import sha256_crypt

conn = sqlite3.connect('DarkRooms.db')
c = conn.cursor()

hashed_password = ""


# UPPER cases for sql syntax, + room number gen save/load game, where you at
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS Players(id INTEGER PRIMARY KEY , username TEXT, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS Gameplay(username TEXT, Items TEXT, Deaths INTEGER)')


def data_entry():
    c.execute("INSERT INTO Players VALUES('Bill', 'pass1')")
    conn.commit()  # save - anytime you modify something in db, you use commit()
    c.close()
    conn.close()  # stop memory from being used


def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, old_pass):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + old_pass.encode()).hexdigest()


def register_user():
    username = input("Welcome to the registration. \nPlease enter your username: \n")
    ##  date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    password = input("Now please enter the password you wish to use: \n")
    global hashed_password;
    hashed_password = hash_password(password);
    print(hashed_password)
    c.execute("INSERT INTO Players(username, password) VALUES(?, ?)", (username, hashed_password))
    conn.commit()
    print("Great! Now you are registered. Please log in now!")
    return hashed_password;


def login():
    while True:
        global username;
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        # hashed_password = hash_password(password);  # this ruins the condition
        find_user = "SELECT * FROM Players WHERE username = ? AND password = ?"
        c.execute(find_user, [username, (
            hashed_password)])
        results = c.fetchall()
        print(hashed_password)

        if results and check_password(hashed_password, password):
            for i in results:
                print("Welcome, " + i[1] + "!");  # the name is i[1] and pass is i[2]
            break;
        else:
            print("Invalid username & password\n")
            again = input("Press 'enter' to try again.")


# read the player from the db and pass it on to 'username'
def gameplay():
    global username;
    c.execute("INSERT INTO Gameplay(username, Items, Deaths) VALUES(?, ?, ?)", (username, 'Nothing', 0))
    conn.commit()  # save - anytime you modify something in db, you use commit()
    print(
        "\n       ---!!!*** Welcome to the Mystery House! ***!!!--- \nThere are evil monsters in this building hidden "
        "in the shadows in different rooms.");
    print("You need to get past all 3 rooms in order to get all the valuable items and win the game.")
    print("Be careful! You only have 2 lives.")
    print("Let`s start!")
    print(
        "\nHint: Some rooms are safe but others are not, it`s up to you to discover little tricks in order to "
        "overcome them.")

    while True:
        enter = input("Press 'e' to enter the house.");
        if enter != 'e':
            print("Not a valid command.")
        else:

                                        # ROOM 1
            print("    Room 1   ");
            print("You enter the room, there`s a big shadow in the corner, but there`s also a golden necklace near.\n")
            answer_1 = input("What do you do?\n Press 'p' to pick the necklace.\n Press 'g' to go forward.")
            if answer_1 == 'p':
                print("You have picked the necklace, but a monster appeared in front of you, and now you are dead.")
                print("You have 1 more life.")
                c.execute("UPDATE Gameplay SET Items='Golden necklace', Deaths=1 WHERE username=?", (username,))
                conn.commit()

                                        # ROOM 2
                print(
                    "You have entered the second room - the living room. There`s a big TV in the middle with the "
                    "screen broken.\n");
                print("You go near it and there`s a note that says: 'Look behind you'")
                answer_2 = input(
                    "What do you do? \n  Press 'f' for going front to the next room. \n  Press 'l' to look behind you.")
                while True:
                    if answer_2 == 'f':
                        print("You run as fast as you can to enter the next room. Voila! You made it.")
                        break;
                    elif answer_2 == 'l':
                        print("A very rare pair of golden earrings have appeared in front you. You take them and "
                              "proceed to the next room.")
                        c.execute("SELECT * FROM Gameplay")
                        c.execute("UPDATE Gameplay SET Items='Golden necklace, golden earrings' WHERE username=?",
                                  (username,))
                        conn.commit()
                        break;
                    else:
                        print("No valid answer, please try again!")

            elif answer_1 == 'g':
                print(
                    "\n\nYou have entered the second room - the living room. There`s a big TV in the middle with the "
                    "screen broken.\n");
                print("You go near it and there`s a note that says: 'Look behind you'")
                answer_2 = input(
                    "What do you do? Press 'f' for going front to the next room. \nPress 'l' to look behind you.")
                while True:
                    if answer_2 == 'f':
                        print("You run as fast as you can to enter the next room. Voila! You made it.")
                        break;
                    elif answer_2 == 'l':
                        print("A very rare pair of golden earrings have appeared in front you. You take them and "
                              "proceed to the next room.")
                        c.execute("UPDATE Gameplay SET Items='Golden necklace, golden earrings' WHERE username=?",
                                  (username,))
                        conn.commit()

                        break;
                    else:
                        print("No valid answer, please try again!")

                                                    # ROOM 3

            print("Now you are in the 3rd and final room. Now multiple choices are ahead fo you.")
            print("You have 3 boxes: each one contains either the key for the door that is keeping \nyou away from freedom or some other treasures, or maybe something else.")
            print("You can only make 1 choice")
            print("Choose wisely, for there will be consequences if you make the wrong decision: ")
            answer_3 = input("\n Press \n 'a' to open the first box \n 'b' for the second box \n 'c' for the third one")
            if answer_3 == 'a':
                print('You die, now enter localhost, or check the files to see your results during the game and what you have achieved.')
                c.execute("SELECT * FROM Gameplay")
                c.execute("UPDATE Gameplay SET Deaths=2 WHERE username=?", (username,))
                conn.commit()
            elif answer_3 == 'b':
                        print('You found the key. You unlock the door and escape the haunted house of mysteries. Well done! Pleae enter localhost or check the files for your progress.')
                        c.execute("SELECT * FROM Gameplay")
                        c.execute("UPDATE Gameplay SET Items='Golden necklace, golden earrings, key to exit' WHERE username=?",
                                  (username,))
                        conn.commit()
            elif answer_3 == 'c':
                        print('You found the ring of infinity which gives you eternal life, but you are still trapped in the house. Sad ending, but at least you`ve got some precious things with you.')
                        c.execute("SELECT * FROM Gameplay")
                        c.execute("UPDATE Gameplay SET Items='Golden necklace, golden earrings, Ring of infinity' WHERE username=?",
                                  (username,))
                        conn.commit()
        break;


def read_from_db():  # * means select all
    c.execute("SELECT * FROM Players WHERE username='ersan'")
    data = c.fetchall();  # you also have fetch one
    for row in data:
        print(row);


def read_all_from_db():
    c.execute("SELECT * FROM Players")
    data = c.fetchall();  # you also have fetch one
    for row in data:
        print(row);


def delete_from_db():
    c.execute("DELETE FROM Players WHERE username = 'fasd'");
    conn.commit()


def update_db():
    c.execute("SELECT * FROM Players")
    c.execute("UPDATE Players SET username='ersan_b' WHERE username='ersan'")


#create_table()  # run this once
register_user();
login();
gameplay()
# read_from_db()
# delete_from_db()
# read_all_from_db();

#update_db()
#read_all_from_db()
# gameplay();
