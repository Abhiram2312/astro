from flask import Flask,request,jsonify
import collections
#import logging
#import pdb

app = Flask(__name__)
#logging.basicConfig(filename='server.log',level=logging.DEBUG)

message_board ={
    "7655":collections.deque([]),
    "7762":collections.deque([]),
    "9655":collections.deque([])
}

user_lookup={
    "7655" : "Abhi",
    "7762" : "Karthik",
    "9655" : "Sam"
}



# @app.route("/login",methods=['POST'])
# def login():
#     users= {
#     "Abhi":"Seesh",
#     "Karthik":"Granddilema",
#     "sam":"whimperingeel"
# }
#     username = request.json.get('username')
#     password = request.json.get('password')
#     if username in users and password == users[username]:
#         return jsonify({'success': True})
#     else:
#         return jsonify({'success': False})


@app.route("/send_message", methods=['POST'])
def publish_to_message_board():
    data = request.json
    sender_id = data['user_id']
    receiver_id = data['receiver_id']
    message = data['message']
    ref = (sender_id, message)
    message_board[receiver_id].append(ref)


@app.route("/receive_messages", methods=['POST'])
def message_board_lookup():
    data = request.json
    receiver_id = data['receiver_id']
    #print(receiver_id)
    ref = {}
    #logging.debug(print(message_board))
    for k in message_board.keys():
        if(k!=receiver_id):
            ref[k]=[]
    while message_board[receiver_id]:
        sender_id, message= message_board[receiver_id].leftpop()
        ref[sender_id].append(message)
        return ref   

@app.route("/get_users",methods=['GET'])
def users_lookup():
    return user_lookup
    


if __name__ == '__main__':
    app.run()