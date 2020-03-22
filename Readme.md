# HUSH!!!

![HUSH](previews/HUSH.jpg?raw=true "HUSH.jpg")


# An awesome end-to-end encrypted chat application using TCP sockets

## Features:
-public key and private key encryption which means even server can't peek into your message
-log in/register system with password
-your friend need not be online, the sqlite3 db stores the messages when friend is offline and pushes the messages tonce the friend logs in
-works in different devices over a lan
-robust error handling features

## How to run:
1. Navigate to client folder
2. Run 'python3 renew_keys.py' and enter username. Each time you run the script and and enter a username, encryption keys for the username will be created(first time) or renewed. For this example we will show a chatting between two users sayan1 and sayan2.
3. Created keys for sayan2 and sayan1. 

![key_generation](previews/key_generation.png?raw=true "key_generation.png")

5. Start the server. Open a terminal and navigate into server folder. Run "python3 server.py localhost 8080" (here I am running the server in localhost and port 8080, input might change to your preference)

![server_run](previews/server_run.png?raw=true "server_run.png")

4. Sign in to the server. Open a terminal and navigate into client folder. Run "python3 server.py localhost 8080" (this host and port should be same as that of server). Here we have two clients interacting. For first time you have to sign up. Your signup credentials will be remembered by the server on your next sign in with same username, even if the server was shutdown in the middle.

![server_login](previews/server_login.png?raw=true "server_login.png")

5. Once login or sign in done, a prompt saying 'New Recipient' will appear. All unread messages will flood into the user interface. Enter the name of the user you want to chat with. If the user is offline, the messages will be stored at the server. If the user is online real time chatting will take place. If no user with the name is registered, you can't chat with him/her and you will have to enter another username.

![basic_chatting](previews/basic_chatting.png?raw=true "basic_chatting.png")

![backup_pushedin](previews/backup_pushedin.png?raw=true "backup_pushedin.png")

6. You can send messages to one person at a time. Enter a name, send messages to him/her and enter "exit" and < new user name > to switch to new recipient.
7. CTRL+C will simply close the client and CTRL+D for the server.