import socket
import pickle


item = ["bola", "permen", "palu"]
act_log = [
    {"ip_address": '169.254.125.49', "date": '20/06/2021', "time": '17:20:38',
     "activity": 'view', "value": None},
    {"ip_address": '169.254.125.49', "date": '20/06/2021', "time": '17:30:38',
     "activity": 'view log', "value": None},
    {"ip_address": '169.254.125.49', "date": '20/06/2021', "time": '20:32:00',
     "activity": 'insert', "value": "palu"},
    {"ip_address": '169.254.125.49', "date": '23/06/2021', "time": '18:39:21',
     "activity": 'view', "value": None},
    {"ip_address": '169.254.125.49', "date": '23/06/2021', "time": '18:39:31',
     "activity": 'view log', "value": None},
    {"ip_address": '169.254.125.49', "date": '23/06/2021', "time": '18:41:05',
     "activity": 'log date', "value": "22/06/2021"},
    {"ip_address": '169.254.125.49', "date": '23/06/2021', "time": '20:41:44',
     "activity": 'log date', "value": "20/06/2021"}
]

h_name = socket.gethostname()
IP_addr = socket.gethostbyname(h_name)
TCP_IP = "192.168.1.4"
TCP_PORT = 6000
BUFFER_SIZE = 4096
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for connection, Server started on", TCP_IP, " and port", TCP_PORT)

while 1:
    conn, addr = s.accept()
    data = conn.recv(BUFFER_SIZE)
    data_decode = pickle.loads(data)

    act_log.append({"ip_address": data_decode['ip_address'], "date": data_decode['date'], "time": data_decode['time'],
                    "activity": data_decode['activity'], "value": data_decode['value']})
    if data_decode['activity'] == "view":
        base_item = pickle.dumps(item)
        conn.send(base_item)
    elif data_decode['activity'] == "insert":
        item.append(data_decode['value'])
        reply = "insert success"
        conn.send(pickle.dumps(reply))
    elif data_decode['activity'] == "search":
        if data_decode['value'] in item:
            reply = 1
        else:
            reply = 0
        conn.send(pickle.dumps(reply))
    elif data_decode['activity'] == "update":
        idx = item.index(data_decode['value'][0])
        item[idx] = data_decode['value'][1]
        reply = "update success"
        conn.send(pickle.dumps(reply))
    elif data_decode['activity'] == "delete":
        item.remove(data_decode['value'])
        reply = "delete success"
        conn.send(pickle.dumps(reply))
    elif data_decode['activity'] == "view log":
        filter = [stu for stu in act_log if stu['ip_address']
                  == data_decode['ip_address']]
        base_log = pickle.dumps(filter)
        conn.send(base_log)
    elif data_decode['activity'] == "log date":
        filter = [stu for stu in act_log if (stu['ip_address']
                                             == data_decode['ip_address'] and stu['date'] == data_decode['value'])]
        base_log = pickle.dumps(filter)
        conn.send(base_log)
    elif data_decode['activity'] == "log hour":
        filter = [stu for stu in act_log if (stu['ip_address']
                                             == data_decode['ip_address'] and stu['time'][:2] == data_decode['value'])]
        base_log = pickle.dumps(filter)
        conn.send(base_log)
    print(data_decode['date'], data_decode['time'], ": IP", data_decode['ip_address'],
          "melakukan", data_decode['activity'])

conn.close()
