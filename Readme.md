# !!!HUSH!!!

## Demo
[![HUSH](previews/cover.png)](https://youtu.be/MF9u-173SDE "Hushchat Demo")

# An awesome end-to-end encrypted chat application using TCP sockets

# Platform
For linux, windows or mac OS, with python installed

## Features:
1. Public key and private key encryption which means even server can't peek into your message
2. Log in/register system with password
3. Your friend needs not be online, the sqlite3 db stores the messages when friend is offline and pushes the messages to your friend once friend logs in
4. Works in different devices over a lan
5. Robust error handling features
6. Less overhead than chat applications that use http or other standard protocols

## How to run:

### Dependencies:
termcolor

To install this run:
```
python3 -m pip install -r requirements.txt
```
1. Navigate to client folder
2. Run 'python3 renew_keys.py' and enter username. Each time you run the script and and enter a username, encryption keys for the username will be created(first time) or renewed. For this example we will show a chatting between two users sayan1 and sayan2.
3. Here for instance we have created keys for sayan2 and sayan1. 

<p align="center">
  <h2 style="text-align:center">Key Generation</h2><br>
  <img src="previews/key_generation.png?raw=true">
</p>


5. Start the server. Open a terminal and navigate into server folder. Run "python3 server.py localhost 8080" (here I am running the server in localhost and port 8080, input might change to your preference)

<p align="center">
  <h2 style="text-align:center">Starting the server</h2><br>
  <img src="previews/server_run.png?raw=true">
</p>

4. Sign in to the server. Open a terminal and navigate into client folder. Run "python3 client.py localhost 8080" (this host and port should be same as that of server). Here we have two clients interacting. For first time you have to sign up. Your signup credentials will be remembered by the server on your next sign in with same username, even if the server was shutdown in the middle.

<p align="center">
  <h2 style="text-align:center">Client Log In / Sign Up</h2><br>
  <img src="previews/server_login.png?raw=true">
</p>

5. Once login or sign in done, a prompt saying 'New Recipient' will appear. All unread messages will flood into the user interface. Enter the name of the user you want to chat with. If the user is offline, the messages will be stored at the server. If the user is online real time chatting will take place. If no user with the name is registered, you can't chat with him/her and you will have to enter another username.

<p align="center">
  <h2 style="text-align:center">Chatting</h2><br>
  <img src="previews/basic_chatting.png?raw=true">
</p>

<p align="center">
  <h2 style="text-align:center">Messages for user1 are backed up at server and sent when user1 logs in</h2><br>
  <img src="previews/backup_pushedin.png?raw=true">
</p>

6. You can send messages to one person at a time only but recieve from multiple clients simultaneously. Enter a name, send messages to him/her and enter "exit" and < new user name > to switch to new recipient.
7. CTRL+C will simply close the client and CTRL+D for the server.
