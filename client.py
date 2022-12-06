import socket as socket_library

PORT = 12345
HOST = socket_library.gethostbyname(socket_library.gethostname())

socket_client = socket_library.socket(socket_library.AF_INET, socket_library.SOCK_DGRAM)

socket_client.sendto("Connected successfully!!".encode(), (HOST, PORT))

while True:
    choice = input(
        "Menu:\n1) see all existing cards\n2) Generated a new card\n3) Check card values\n4) Update card values\n5) Pay for Ride\n0) To Exit ")
    if choice == "0":
        print("""
        *****************        
        *** BYE BYE:) ***
        *****************
        """)
        break

    elif choice == "1":
        socket_client.sendto("1".encode(), (HOST, PORT))
        data, address = socket_client.recvfrom(1024)
        cards = data.decode()
        print("Valid cards:\n ", cards)

    elif choice == "2":
        print("Generating a new card for you...")
        # sleep(3)
        socket_client.sendto("2".encode(), (HOST, PORT))
        data, address = socket_client.recvfrom(128)
        print(data.decode())

    elif choice == "3":
        socket_client.sendto("3".encode(), (HOST, PORT))
        check_choice = str(input("Please enter your card ID to check card values:"))
        socket_client.sendto(check_choice.encode(), (HOST, PORT))
        data, address = socket_client.recvfrom(128)
        print(data.decode())

    elif choice == "4":
        socket_client.sendto("4".encode(), (HOST, PORT))
        change_id = str(input("Please enter your card ID: "))
        socket_client.sendto(change_id.encode(), (HOST, PORT))

        update_choice = str(input("1) Change card Contract\n2) Change card Wallet\nYour Choice: "))
        if update_choice == "1":
            socket_client.sendto("1".encode(), (HOST, PORT))
            change_contract = str(input("""Change Contract To:\n1) North\n2) Center\n3) south
4) Cancel card contract\nYour Choice: """))
            if change_contract == "1":
                socket_client.sendto("1".encode(), (HOST, PORT))
            elif change_contract == "2":
                socket_client.sendto("2".encode(), (HOST, PORT))
            elif change_contract == "3":
                socket_client.sendto("3".encode(), (HOST, PORT))
            elif change_contract == "4":
                socket_client.sendto("4".encode(), (HOST, PORT))
            else:
                print("Enter 1-4 Only !!!")

        elif update_choice == "2":
            socket_client.sendto("2".encode(), (HOST, PORT))
            change_wallet = str(input("Pleas set an amount for the wallet:\nYour amount is:  ")).encode()
            if int(change_wallet) in range(0, 99999):
                socket_client.sendto(change_wallet, (HOST, PORT))
            else:
                print("Enter valid Number!!!")

        data, address = socket_client.recvfrom(128)
        print(data.decode())

    elif choice == "5":
        socket_client.sendto("5".encode(), (HOST, PORT))
        ride_id = str(input("Please enter your card ID: "))
        socket_client.sendto(ride_id.encode(), (HOST, PORT))

        charge = str(input("Where you want to Ride?:\n1) North=25\n2) Center=40\n3) south=30\nYour choice:"))
        if int(charge) == 1:
            socket_client.sendto("1".encode(), (HOST, PORT))
        elif int(charge) == 2:
            socket_client.sendto("2".encode(), (HOST, PORT))
        elif int(charge) == 3:
            socket_client.sendto("3".encode(), (HOST, PORT))
        else:
            print("Enter only 1-3 Choice !!!")

        data, address = socket_client.recvfrom(128)
        print(data.decode())
        # data1, address1 = socket_client.recvfrom(128)
        # print(data1.decode())

    else:
        print("Enter Only 1-5 Choice!!!")

