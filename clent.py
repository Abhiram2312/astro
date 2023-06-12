import requests
import re
#import pdb
import time
import json

sender_id = "7655"
#receiver_id = input("Enter The Receiver's ID:\n")
#message = input("Enter Your Message:\n")

# def validity():
#     validity_url = "http://127.0.0.1:5000/login"
#     username=input("Enter your username:")
#     password=input("Enter your password:")
#     data={
#         username:password
#     }
#     response = requests.post(validity_url,data)
#     print(response.json())

def send_message(receiver_id, message):
    send_url = "http://127.0.0.1:5000/send_message"
    data = {'user_id':sender_id,
            'receiver_id':receiver_id,
            'message':message
            }
    resp = requests.post(send_url, json=data)
    print(resp.text)

def receive_message(receiver_id):
    receive_url = "http://127.0.0.1:5000/receive_messages"
    data= {'receiver_id':receiver_id}
    resp = requests.post(receive_url, json=data)
    #print(resp)
    #print(resp.json())
    return resp

def get_user_lookup():
    #breakpoint()
    user_lookup_url="http://127.0.0.1:5000/get_users"
    resp = None
    try:
        resp = requests.get(user_lookup_url)
    except requests.exceptions.ConnectionError:
        print("Server Offline")
    return resp
#TODO: 
def main():
    receiver_id = input("Enter The Receiver's ID:\n")
    #breakpoint()
    rev_user_id_mapping = {}
    while True:
        user_id_mapping = get_user_lookup()
        if user_id_mapping is None:
            time.sleep(10)
            continue
        if(user_id_mapping.status_code!=200):
            print("Internal Error")
            time.sleep(10)
            continue
        #pdb.set_trace()
        #user_id_mapping.json()
        for k, v in user_id_mapping.json().items():
            rev_user_id_mapping[v] = k
        #pdb.set_trace()
        messages = {}
        messages  = receive_message(receiver_id)
        if (messages.status_code!=200):
            print("Internal Error while reteriving messages")
            time.sleep(10)
            continue #really?...
        messages = messages.json()
        # print(type(messages))
        for user_id in messages.keys():
            # print(type(messages))
            for message in messages[user_id]:
                print(user_id_mapping[user_id],": ",message)

    input_message = input("You: ")
    match = re.search(r'@(.*?),(.*)', input_message)
    if match:
        user_name = match.group(1)
        message = match.group(2)
        user_id = rev_user_id_mapping[user_name]
        send_message(user_id, message)


if __name__ == "__main__":
    main()