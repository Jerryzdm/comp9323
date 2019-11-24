import time
from socket import *
import json

#encode_pack, dict -> json_str -> bytes
def encode_request(pack):
    pack_j = json.dumps(pack)
    encode_pack = pack_j.encode('UTF-8')
    return encode_pack

#decode_pack, bytes -> json_str -> dict
def decode_response(pack):
    decode_pack = pack.decode('UTF-8')
    return json.loads(decode_pack)

#send request_order
def send_request(request_order):
    serverName = '127.0.0.1'
    serverPort = 12000 #change this port number if required
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    request_pack = encode_request(request_order)

    clientSocket.send(request_pack)
    response_pack  = clientSocket.recv(1024)
    response_order = decode_response(response_pack)

    print('From Server:', response_order)
    clientSocket.close()
    return response_order



'''
term = 'Term2'  # 'Term1' or 'Term2' or 'Term3' or 'Summer'
course_code = 'COMP9517'
phase = 'Postgraduate' #'Undergraduate' or 'Postgraduate'
email = 'jzoudiming@gmail.com'
query_type_flag = 'bind'  # 'bind' or 'unbind'
request_order = {'course_code':course_code, 'term':term,'phase':phase, 'email':email,
                 'query_type_flag':query_type_flag}
s = time.time()
response_order = send_request(request_order)
d = time.time()-s
print(d)
'''



