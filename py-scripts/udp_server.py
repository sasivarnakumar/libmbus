
# socket_echo_server_dgram.py

import socket
import sys
# import MySQLdb
import json
from datetime import datetime
import os
# import pika
# import requests
# check if picka package is available or not in the system
# if 'pika' in sys.modules:
#     import pika

today = datetime.now()
file = today.strftime("%d-%m-%Y-%H:%M:%S")
directory = today.strftime("%d-%m-%Y")

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('0.0.0.0', 5683)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)


# declare the pika connection

# credentials = pika.PlainCredentials(username='guest', password='monkatwork')

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='0.0.0.0',port=5672,credentials=credentials))
# channel = connection.channel()

# channel.queue_declare(queue='python_message')



# print(file)


while True:
     print('\nwaiting to receive message')
     data, address = sock.recvfrom(4096)
    
     print('received {} bytes from {}'.format(len(data), address))
     print(data)
     today = datetime.now()
     file = today.strftime("%d-%m-%Y %H:%M:%S")
     coap_path = '/var/www/html/coap/storage/app/public/coapdata/'
     directory = today.strftime("%d-%m-%Y")
     
     # i=0
     # ins_data=''
     # while i < len(data):
     #     s = str(data[i]) 
     #     ins_data += s 
     #     ins_data += '-' 
     ins_data = data
     # ins_data = bytes.hex(data)

     # insert data in db
     client_ip = address[0]
     client_port = address[1]
     insert_data=str(ins_data)
     
     # insert data
     # db = MySQLdb.connect("localhost","root","MonkatWork3434","coap")
     # cursor = db.cursor()
     # sql_insert_query = """ INSERT INTO `coap_data` (`mid`,`server_port`,`client_ip`,`client_port`,`raw_data`,`data`,`timestamp`,`uri_path`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
     # server_port = server_address[1]
     # client_ip,client_port = client_address
     # insert_tuple = [0,server_port,client_ip,client_port, ins_data,
     #                 '','','pudpud']
     # result  = cursor.execute(sql_insert_query, insert_tuple)
     # db.commit()
     # cursor.close()
     # end insert data
     # print('bava')
     filename=file+'.json'
     my_details={'server_port':server_address[1],'client_ip':client_ip,'client_port':client_port,'data':insert_data,'created_at':file}
     print(my_details)
     # channel.basic_publish(exchange='', routing_key='python_message', body=json.dumps(my_details),properties=pika.BasicProperties(delivery_mode = 2))

     # file creation in python 
     if not os.path.exists(coap_path+directory):
      # print('yes if')
      os.makedirs(coap_path+directory)


     with open(coap_path+directory+'/'+filename, 'w') as json_file:
     	json.dump(my_details, json_file)
     # print(json_file)
     # json.close


    
    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    # with open(directory+'/'+'bava.txt', 'w') as json_file:  
    #     json.dump(my_details, json_file)

    # print('bava:'+my_details)
     
     if data:
         send_data = b'data received raj length:'
         sent = sock.sendto(send_data, address)
         print('sent {} bytes back to {}'.format(sent, address))
