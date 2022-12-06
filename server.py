import socket as socket_library
import sqlite3
import random

# SOCKET connection
PORT = 12345

socket_server = socket_library.socket(socket_library.AF_INET, socket_library.SOCK_DGRAM)
socket_server.bind(("", int(PORT)))

connect, address = socket_server.recvfrom(1024)
print(f"Client {connect.decode()}, from address:{address[0]} & Port:{address[1]}")



# Card list card_id, contract, wallet
cards = [
    (100, "North", 50),
    (101, "Center", 100),
    (102, "South", 0),
    (103, "North", 150),
    (104, "South", 0),
    (105, None, 1000),
    (106, "Center", 0),
    (107, None, 750)
]
# database connection
database = sqlite3.connect(database="C:/Users/itayh/OneDrive/Desktop/DevOps/Python/project/D_B.sqlite")
cur = database.cursor()

# CREATE TABLE
create_table = '''CREATE TABLE IF NOT EXISTS cards
                    (card_id INTEGER(4),
                     contract TEXT,
                     wallet INTEGER,
                     PRIMARY KEY (card_id));'''
cur.execute(create_table)

# ADD DATA
for card in cards:
    cur.execute('INSERT OR REPLACE INTO cards VALUES(? ,? ,?)', card)
database.commit()


# SELECT card ids
ID = '''SELECT card_id 
         FROM cards;'''
cur.execute(ID)
results_id = cur.fetchall()
IDs = ''.join(str(x) for x in results_id)
# print(IDs)

# update cards contracts
select_check = '''SELECT *
                         FROM cards
                    WHERE card_id=?;'''

update_contract = '''UPDATE cards
                      SET contract=?
                      WHERE card_id=?
                      ;'''

select_contract = '''SELECT contract 
                     FROM cards
                     WHERE card_id=?
                     ;'''


# Update card wallet
update_wallet = '''UPDATE cards
                      SET wallet=?
                      WHERE card_id=?
                      ;'''

select_wallet = '''SELECT wallet
                     FROM cards
                     WHERE card_id=?
                     ;'''

# Client requests
while True:
    data, address = socket_server.recvfrom(1024)
    client_choice = data.decode()
    if client_choice == "1":
        print("Client asks for cards ID`s:", IDs)
        socket_server.sendto(IDs.encode(), address)

    elif client_choice == "2":
        new_card = (random.randint(1, 999), None, 0)
        cards.append(new_card)
        cur.execute('INSERT INTO cards VALUES(? ,? ,?)', new_card)
        database.commit()
        msg_new_card = f"Card Generated successfully, Card ID is: {new_card[0]}"
        socket_server.sendto(msg_new_card.encode(), address)
        print(f"Client Card {new_card[0]} Generated successfully")

    elif client_choice == "3":
        data_check, address = socket_server.recvfrom(64)
        check_id = data_check.decode()

        def show_results(query_name=None, params=None):
            global prod
            if params is None:
                cur.execute(query_name)
            else:
                cur.execute(query_name, params)
            print("The amount of found is: ", cur.rowcount)
            result = cur.fetchall()
            for prod in result:
                print(f"Client values: {str(prod)}")
            if check_id in IDs:
                msg_check = f"Your card values: Card_id- {str(prod[0])} - Contract- {str(prod[1])} - Wallet amount- {str(prod[2])}"
                socket_server.sendto(msg_check.encode(), address)
            else:
                msg_worng = f"The Card {check_id} is not in the list of cards, Please insert valid card!!!".encode()
                socket_server.sendto(msg_worng, address)
                print("Client insert Not available card")

        show_results(select_check, (check_id,))

    elif client_choice == "4":
        card_id, address = socket_server.recvfrom(64)
        card = card_id.decode()
        print(f"Client card:{card}")

        if card in IDs:
            choice, address1 = socket_server.recvfrom(64)
            choice = choice.decode()

            msg = f"Your card {card} is updated successfully ".encode()
            if choice == "1":
                ride, address2 = socket_server.recvfrom(64)
                ride = ride.decode()
                if ride == "1":
                    cur.execute(update_contract, ("North", int(card)))
                    database.commit()
                    socket_server.sendto(msg, address)
                    print(f"Client update contract to North")
                elif ride == "2":
                    cur.execute(update_contract, ("Center", int(card)))
                    database.commit()
                    socket_server.sendto(msg, address)
                    print(f"Client update contract to center")
                elif ride == "3":
                    cur.execute(update_contract, ("South", int(card)))
                    database.commit()
                    socket_server.sendto(msg, address)
                    print(f"Client update contract to South")
                elif ride == "4":
                    cur.execute(update_contract, (None, int(card)))
                    database.commit()
                    cancel_c = f"You have been canceled your contract successfully"
                    socket_server.sendto(cancel_c, address)
                    print(f"Client cancelled his contract")

            elif choice == "2":
                wallet_id, address = socket_server.recvfrom(64)
                change_wallet = int(wallet_id.decode())
                cur.execute(update_wallet, (change_wallet, int(card)))
                database.commit()
                socket_server.sendto(msg, address)
                print(f"Client update his wallet amount to {wallet_id.decode()}")

        else:
            msg = f"The card {card} is not available please insert available card !!".encode()
            socket_server.sendto(msg, address)
            print("Client insert Not available card")

    elif client_choice == "5":
        card_id, address = socket_server.recvfrom(64)
        card = card_id.decode()
        print(f"Client card:{card}")
        if card in IDs:
            choice, address1 = socket_server.recvfrom(64)
            choice = choice.decode()
            print(choice)

            cur.execute(select_contract, (card,))
            con = cur.fetchone()
            print(str(con))
            msg_ride = f"Your Ride is completed Successfully ! ".encode()
            msg_not = f"Your card:{card} contract:{con} is not match to the destenation, The Ride has charged from your wallet amount".encode()

            north = 25
            center = 40
            south = 30

            if choice == "1":
                if "North" in con:
                    socket_server.sendto(msg_ride, address)
                    print("Client Ride by Contract")
                else:
                    cur.execute(select_wallet, (card,))
                    wall = cur.fetchone()
                    wallet_amount = int(wall[0])
                    if wallet_amount >= north:
                        socket_server.sendto(msg_not, address)
                        charged = wallet_amount - north
                        cur.execute(update_wallet, (charged, int(card)))
                        database.commit()
                        print(f"Client Ride by wallet amount{wallet_amount} - {north}")

                    else:
                        not_amount = f"Your wallet amount is {wallet_amount} and the Ride cost {north}, please charge your wallet or add an contract".encode()
                        socket_server.sendto(not_amount, address)
                        print("Client does not have enough money to ride")

            elif choice == "2":
                if "Center" in con:
                    socket_server.sendto(msg_ride, address)
                    print("Client Ride by Contract")
                else:
                    cur.execute(select_wallet, (card,))
                    wall = cur.fetchone()
                    wallet_amount = int(wall[0])
                    if wallet_amount >= center:
                        socket_server.sendto(msg_not, address)
                        charged = wallet_amount - center
                        cur.execute(update_wallet, (charged, int(card)))
                        database.commit()
                        print(f"Client Ride by wallet amount{wallet_amount} - {north}")
                    else:
                        not_amount = f"Your wallet amount is {wallet_amount} and the Ride cost {center}, please charge your wallet or add an contract".encode()
                        socket_server.sendto(not_amount, address)
                        print("Client does not have enough money to ride")
            elif choice == "3":
                if "South" in con:
                    socket_server.sendto(msg_ride, address)
                    print("Client Ride by Contract")

                else:
                    cur.execute(select_wallet, (card,))
                    wall = cur.fetchone()
                    wallet_amount = int(wall[0])
                    if wallet_amount >= south:
                        socket_server.sendto(msg_not, address)
                        charged = wallet_amount - center
                        cur.execute(update_wallet, (charged, int(card)))
                        database.commit()
                        print(f"Client Ride by wallet amount{wallet_amount} - {north}")

                    else:
                        not_amount = f"Your wallet amount is {wallet_amount} and the Ride cost {south}, please charge your wallet or add an contract".encode()
                        socket_server.sendto(not_amount, address)
                        print("Client Ride by Contract")

        else:
            msg = f"The card {card} is not available please insert available card !!".encode()
            socket_server.sendto(msg, address)
            print("Client insert Not available card")


database.close()
