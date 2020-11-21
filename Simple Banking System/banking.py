import random
import os
import _sqlite3

class Card:
    card_number = str()
    card_pin = str()
    card_balance = int()
    
    def check_balance(self, number):
        balance = connection.execute("SELECT balance FROM card WHERE number = {}".format(number)).fetchall()
        print("Balance {}".format(balance[0][0]))
    def card_menu(self, connection, card_number):
        print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
        choice = int(input())
        if choice == 1:
            self.check_balance(card_number)
            return True
        elif choice == 2:
            print("Enter income:")
            connection.execute("UPDATE card SET balance = balance + {0} WHERE number = {1}".format(int(input()), card_number))
            print("Income was added!")
            connection.commit()
            return True
        elif choice == 3:
            print("Transfer\nEnter card number:")
            transfer_number = int(input())
            if str(transfer_number)[0] != '4':
                print("Such a card does not exist.")
                return True
            if lun_alg(str(transfer_number)[:-1]) != str(transfer_number):
                print("Probably you made mistake in the card number.\nPlease try again!")
                return True
            check = connection.execute("SELECT number FROM card WHERE number = {}".format(transfer_number)).fetchall()
            if transfer_number == card_number:
                print("You can't transfer money to the same account!")
                return True
            if not check:
                print("Such a card does not exist.")
                return True
            print("Enter how much money you want to transfer:")
            transfer_money = int(input())
            balance = connection.execute("SELECT balance FROM card WHERE number = {}".format(card_number)).fetchall()
            if transfer_money >= balance[0][0]:
                print("Not enough money!")
                return True
            else:
                connection.execute("UPDATE card SET balance = {0} WHERE number = {1}".format(transfer_money, transfer_number))
                connection.execute("UPDATE card SET balance = balance - {0} WHERE number = {1}".format(transfer_money, card_number))
                print("Success")
                connection.commit()
                return True
        elif choice == 4:
            connection.execute("DELETE FROM card WHERE number = {}".format(card_number))
            print("The account has been closed!")
            connection.commit()
            return False
        elif choice == 5:
            print("You have successfully logged out!")
            return False
        elif choice == 0: 
            print("Bye!")
            exit()
            return
    def logging(self, card_number, card_pin, connection):
        check = connection.execute("SELECT COUNT(1) FROM card WHERE number = {0} AND pin = {1};".format(card_number, card_pin)).fetchall()
        if not check[0][0]:
            print("Wrong card number or PIN!")
        else:
            print("You have successfully logged in!")
            while self.card_menu(connection, card_number):
                pass
card1 = Card()
def length_rand(num, switch):  # 0 - for number; 1 - for PIN
    if len(str(num)) < 9 and switch == 0:
        temp = str(num)
        temp = temp[::-1]
        while len(temp) < 9:
            temp += '0'
        temp = temp[::-1]
        return temp
    elif len(str(num)) < 4 and switch == 1:
        temp = str(num)
        temp = temp[::-1]
        while len(temp) < 4:
            temp += '0'
        temp = temp[::-1]
        return temp
    else:
        return str(num)

def lun_alg(card_number):
    checksum = 0
    i = 1
    for a in card_number:
        if i % 2 != 0:
            if int(a) * 2 >= 10:
                checksum += int(a) * 2 - 9
            else:
                checksum += int(a) * 2
        else:
            checksum += int(a)
        i += 1
    if checksum % 10 == 0:
        card_number = card_number + '0'
    else:
        add = (checksum // 10 + 1) * 10 - checksum
        card_number = card_number + str(add)
    return card_number

def number_with_lun_alg():
    digits = length_rand(random.randint(0, 999999999), 0)
    card_number = "400000" + digits
    return lun_alg(card_number)
    
def main_menu(connection):
    global id

    print("1. Create an account\n2. Log into account\n0. Exit")
    choice = int(input())
    if choice == 1:
        print("Your card has been created")
        card_number = number_with_lun_alg()
        card1.card_number = card_number
        card_pin = length_rand(random.randint(0, 9999), 1)
        card1.card_pin = card_pin
        print("Your card number:\n{0}\nYour card PIN:\n{1}".format(card1.card_number, card1.card_pin))
        connection.execute("INSERT INTO card (id,number,pin)VALUES({0},{1},{2});".format(id, card_number, card_pin))
        connection.commit()
        id += 1
        return True
    elif choice == 2:
        card_pin = 0
        card_number = 0
        print("Enter your card number:")
        card_number = str(input())
        print("Enter your PIN:")
        card_pin = str(input())
        card1.logging(card_number, card_pin, connection)
        return True
    else:
        print("Bye!")
        return False

# main program block
database = open('card.s3db', 'a+')
connection = _sqlite3.connect('card.s3db')

if os.stat('card.s3db').st_size == 0:
    connection.execute("CREATE TABLE card( id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")

id = 0
while  main_menu(connection):
    pass

database.close()
