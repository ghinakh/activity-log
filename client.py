from os import system, name
import socket
from datetime import date, datetime
import pickle

h_name = socket.gethostname()
IP_addr = socket.gethostbyname(h_name)
TCP_IP = input("Enter IP Server: ")
TCP_PORT = 6000
BUFFER_SIZE = 4096


def main():
    menu()


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def send(command):
    log = {
        "ip_address": IP_addr,
        "date": date.today().strftime("%d/%m/%Y"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "activity": command[0],
        "value": command[1]
    }
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    base_log = pickle.dumps(log)
    s.send(base_log)
    data = s.recv(BUFFER_SIZE)
    data_decode = pickle.loads(data)
    s.close()
    return data_decode


def view_log():
    pilihan = input("""
1 : Lihat Semua Log
2 : Lihat Log Berdasarkan Tanggal
3 : Lihat Log Berdasarkan Jam
B : Kembali ke Menu Utama

Masukkan pilihan: """)
    clear()
    if pilihan.upper() == "1":
        print("Lihat Semua Activity Log: ")
        value = send(['view log', None])
        num = 1
        for i in value:
            print("{}. IP Address: {}, Date: {}, Time: {}, Activity: {}, Value: {}".format(
                num, i['ip_address'], i['date'], i['time'], i['activity'], i['value']))
            num += 1
    elif pilihan.upper() == "2":
        print("Lihat Log Berdasarkan Tanggal")
        tgl = input("Masukkan Tanggal (ex: 22/06/2021): ")
        value = send(['log date', tgl])
        num = 1
        for i in value:
            print("{}. IP Address: {}, Date: {}, Time: {}, Activity: {}, Value: {}".format(
                num, i['ip_address'], i['date'], i['time'], i['activity'], i['value']))
            num += 1
    elif pilihan.upper() == "3":
        print("Lihat Log Berdasarkan Jam")
        jam = input("Masukkan Jam (ex: 17): ")
        value = send(['log hour', jam])
        num = 1
        for i in value:
            print("{}. IP Address: {}, Date: {}, Time: {}, Activity: {}, Value: {}".format(
                num, i['ip_address'], i['date'], i['time'], i['activity'], i['value']))
            num += 1
    elif pilihan.upper() == "B":
        menu()


def menu():
    while True:
        pilihan = input("""
A : Lihat Item
B : Tambah Item
C : Edit Item
D : Hapus Item
E : Lihat Log
Q : Keluar

Masukkan pilihan: """)
        clear()
        if pilihan.upper() == "A":
            print("Lihat Item: ")
            print(send(["view", None]))
        elif pilihan.upper() == "B":
            print("Tambah Item: ")
            add = input("Add New Item: ")
            print(send(["insert", add.lower()]))
        elif pilihan.upper() == "C":
            print("Edit Item: ")
            old = input("Item yang mau diganti: ")
            if send(["search", old.lower()]):
                new = input("Item baru: ")
                print(send(["update", [old.lower(), new.lower()]]))
            else:
                print(old, "not found")
        elif pilihan.upper() == "D":
            print("Hapus Item: ")
            deleted = input("Item yang mau dihapus: ")
            if send(["search", deleted.lower()]):
                print(send(["delete", deleted.lower()]))
            else:
                print(old, "not found")
        elif pilihan.upper() == "E":
            view_log()
        elif pilihan.upper() == "Q":
            break
        else:
            print("You must only select from A to E")
            print("Please try again")
            menu()


menu()
# print("Can not connect to server", TCP_IP)
