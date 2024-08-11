import requests, time; from threading import Thread

def update_msgs():
    chc=get_messages()
    if chc: print('\033c'+'\n'.join(chc))
    else: print("\033c---No messages have been sent yet---")
    while True:
        time.sleep(2)
        msgs=get_messages()
        if chc==msgs: continue
        print('\033c'+'\n'.join(msgs))
        print(f'\n\033[F{user}: ',end='')
        chc=msgs[:]

# Server URL (replace with your Gitpod URL)
server_url = 'https://5000-breathecode-pythonflask-urt11axljb1.ws-us115.gitpod.io'
user=input("\033cPlease enter your username for this application: ")

def send_message(username, message):
    try:
        response = requests.post(f"{server_url}/send-message", json={'username': username, 'message': message})
        if response.status_code!=200: raise Exception(f"An error has occurred: {response}")
    except requests.exceptions.RequestException:
        print('The server is not currently running.');exit()

def get_messages():
    try:
        m=requests.get(f"{server_url}/get-messages").json()['messages']
        return [f'{v["username"]}: {v["message"]}' for v in m]
    except requests.exceptions.RequestException:
        print('The server is not currently running.');exit()

# Example usage
Thread(target=update_msgs,daemon=True).start()
time.sleep(0.5)
while True:
    send_message(user, input(f'{user}: '))
