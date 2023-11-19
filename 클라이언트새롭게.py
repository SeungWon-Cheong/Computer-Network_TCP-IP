import socket
import threading
from datetime import datetime

def Send(client): #accept 이후 처음 서버에 송신 
    while True:
        str = input()
        if str != '':#비어있는 문자열이 아니라면
            message = "[" + phoneNumber + "] " + str
            # 사용자 입력
            client.send(bytes(message.encode()))  #문자열을 인코딩해서 서버에 send한다.
            # Client -> Server 데이터 송신 

######이부분을 고치면 될거같기도?#####
#1. 서버에서 보낼때 클라이언트를 가려서 보낸다.
#2. 클라이언트가 받을 때 가려서 받는다.
def Recv(client):
    while True:
        recv_data = client.recv(1024).decode()  
        # Server -> Client 데이터 수신
        print(recv_data) #디코딩된 문자열을 출력한다. 

if __name__ == '__main__':
    # client 설정
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # AF_INET -> 해당 소켓은 IPV4(IP version 4)로 사용을 의미
    # SOCK_STREAM -> 해당 소켓에 TCP 패킷을 받겠다는 의미

    SERVER = input("IP:")
    # 통신할 대상의 IP 주소
    PORT = int(input("PORT:"))
    # 통신할 대상의 Port 주소
    print("반갑습니다! CUKTAXI 입니다!")
    phoneNumber = input("phoneNumber:")
    sendPhoneNumber = phoneNumber
    client.send(bytes(sendPhoneNumber.encode())) #처음에 전화번호를 인코딩해서 한번 서버로 송신함

    # Server Aress
    ADDR = (SERVER, PORT)
    # result : ('PC Adress(IPV4)', PORT(6060), 'NAME')
    
    # server에 연결
    client.connect(ADDR)
    # 서버로 연결시도
    print(f'Connecting to {SERVER}:{PORT}')

while True:
    def show_menu(): ##메뉴 생성
        print("1. 게시글 생성")
        print("2. 게시글 참여")
        choice = input("원하는 역할을 선택하세요 (1 또는 2): ")
        return choice
    
    role = int(show_menu())
    client.send(bytes(role.encode())) #메뉴 번호를 인코딩해서 한번 서버로 송신함

    if role == 1:
        ride_time_str = input("탑승 시간을 입력하세요 (HH:MM 형식): ")
        client.send(bytes(ride_time_str)) #탑승 시간를 서버로 송신함

        pickup_location = input("탑승지를 입력하세요: ")
        client.send(bytes(pickup_location.encode())) #탑승 시간를 인코딩해서 서버로 송신함

        destination = input("목적지를 입력하세요: ")
        client.send(bytes(destination.encode())) #탑승 시간를 인코딩해서 서버로 송신함

        created_noti1 = client.recv(1024).decode()#서버로부터 게시글 생성 공지를 받음
        print(created_noti1)

    elif role == 2:

        
########반복문으로 어떻게 모든 게시판 목록을 출력하지????? ====================================
        created_noti2 = client.recv(1024).decode()#서버로부터 게시글 생성 공지를 받음(게시글 개수만큼 받아야함)
        print(created_noti2)
#===========================================================================================


        post_id_to_join = input("참여하려는 게시글의 ID를 입력하세요: ")
        client.send(bytes(post_id_to_join.encode())) #메뉴 번호를 인코딩해서 한번 서버로 송신함
        break
    else: 
        print("잘못된 메뉴 입력")
    
    #Client의 메시지를 보낼 쓰레드
    sendthread = threading.Thread(target=Send, args=(client, ))
    sendthread.start()

    #Server로 부터 다른 클라이언트의 메시지를 받을 쓰레드
    recvthread = threading.Thread(target=Recv, args=(client, ))
    recvthread.start()