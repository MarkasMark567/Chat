import requests, os; from threading import Thread
import signal

running=True; inp=''

def server_up():
    if requests.get(url).status_code==404:
        return False
    return True

def disconnect():
    os.kill(os.getpid(), signal.SIGINT)

def update_msgs():
    chc=get_messages()
    while True:
        msgs=get_messages()
        if chc==msgs: continue
        elif chc+[f'{user}: {inp}']==msgs:
            chc=msgs[:]+[f'{user}: {inp}']
            continue
        os.system('cls')
        print('\n'.join(msgs))
        print(f'\n\033[F{user}: ',end='')
        chc=msgs[:]

url = 'https://5000-breathecode-pythonflask-urt11axljb1.ws-us115.gitpod.io'

if not server_up(): print("The server is currently not running.");disconnect()
os.system('cls')
user=input("Please enter your username for this application: ")

def send_message(username, message):
    if not server_up(): print("\nThe server is currently not running.");disconnect()
    response = requests.post(f"{url}/send-message", json={'username': username, 'message': message})
    if response.status_code!=200: raise Exception(f"An error has occurred: {response}")

def get_messages():
    if not server_up(): print("\nThe server is currently not running.");disconnect()
    m=requests.get(f"{url}/get-messages").json()['messages']
    return [f'{v["username"]}: {v["message"]}' for v in m]

def gemini_req(username, message):
    if not server_up(): print("\nThe server is currently not running.");disconnect()
    response = requests.post(f"{url}/req-gemini", json={'username': username, 'message': message})
    if response.status_code==400: print('\nWARNING: You have been automatically kicked from the server for innapropriate behavior.');disconnect()
    elif response.status_code!=200: print(f'\nWARNING: An error occurred: {response}');disconnect()

def stop_server(dev_code):
    if not server_up(): print("\nThe server is currently not running.");disconnect()
    response = requests.post(f"{url}/stop-server", json={'dev_code': dev_code})
    if response.status_code==400: raise PermissionError(response.text)
    else: print(response.text);disconnect()

chc=get_messages()
os.system('cls')
if chc: print('\n'.join(chc))
else: print("---No messages have been sent yet---")

Thread(target=update_msgs,daemon=True).start()

while True:
    inp=input(f'{user}: ')
    if inp.upper()=='/EXIT':
        os.system('cls')
        print('Exiting program...')
    elif inp.upper()[:8]=='@GEMINI:': Thread(target=gemini_req,args=[user,inp],daemon=True).start()
    elif inp.upper()[:6]=="/STOP ": stop_server(inp[6:])
    else: send_message(user, inp)
    msgs=get_messages()
