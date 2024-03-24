import argparse, random, socket, sys,threading, time

from email import message

MAX_BYTES = 65535
server_sock = []
sum1 = random.sample(range(1, 10), 4) #list形式


def server_action(sock, number):
    time_start = time.time()
    print('Listening at', sock.getsockname())
    print(sum1)
    while True:
        data, address = sock.recvfrom(MAX_BYTES)  
        data = data.decode('ascii')
       
        print('Server {}:'.format(number)+'The client at {} says {!r}'.format(address, data))
        a = b = 0
        data = list(data)
        for i in range(4):
            if int(data[i]) in sum1:
                if int(data[i]) == sum1[i]:
                    a += 1
                else:
                    b += 1
            else:
                    continue
        if a != 4:
            data = str(a)+"A"+str(b)+"B"
        #print('Server {}:'.format(number)+'The client at {} says {!r}'.format(address, text))
        # message = '"{}"'.format(text)+'is {} bytes long'.format(len(data))
            message = data
            sock.sendto(message.encode('ascii'), address)
        else:
            message = " You are right!!!!!"
            time_end = time.time()    #結束計時
            time_c= time_end - time_start   #執行所花時間

            
            print('time cost', time_c, 's')
            print('Congratulations', sock.getsockname())
            
            sock.sendto(message.encode('ascii'), address)
            sum = random.sample(range(1, 10), 4) 
            
            break
        
def server(interface, port):
    th = []
    for i in range(3):
        server_sock.append(socket.socket(socket.AF_INET,socket.SOCK_DGRAM))
        server_sock[i].bind((interface,port+i))
        th.append(threading.Thread(target=server_action, args = (server_sock[i],i)))
    for i in range(3):
        th[i].start()
    for i in range(3):
        th[i].join()
        

def client(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((hostname, port)) # 要先跟server建立連線，之後send資料不須指定地址
    print('Client socket name is {}'.format(sock.getsockname()))
    
    while True:
        text = input("Please enter the number >>>: ")
       
        if text == "|exit|":
            
            print(sock.getsockname(),'has leave the game')
            break

        if len(text) != 4:
            print("Wrong format,Please enter the correct format")
            continue
        if not text.isdecimal():
            print("Wrong format,Please enter the correct format")
            continue
        data = text.encode('ascii')
        sock.send(data) # sendto需指定接收ip，send不用(上面已經connect就可使用)

        data = sock.recv(MAX_BYTES)
        print('The server says {!r}'.format(data.decode('ascii')))
        if data.decode('ascii') == "You are right!!!!!":
            break

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP,'
                                     ' pretending packets are often dropped')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=5000,
                        help='UDP port (default 5000)')
    args, unknown = parser.parse_known_args()
    function = choices[args.role]
    function(args.host, args.p)