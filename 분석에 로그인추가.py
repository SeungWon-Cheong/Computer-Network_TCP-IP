import socket #소켓통신을 위한 모듈 
import threading #쓰레드 모듈을 쓰는 이유:
from queue import Queue #큐 모듈을 쓰는 이유: 먼저 들어온 채팅 입력값을 먼저 처리해야하기 떄문 
import pymysql
from datetime import datetime
#write() 함수 구현 #멀티 쓰레드 안에서 send 함수 수행됨
def Send(group, send_queue): #group에는 보낼 클라이언트의 소켓정보(튜플), send_queue에는 큐에담긴 데이터가 모두 들어감
    print('Thread Send Start')
    while True: #종료조건이 Ture인 무한루프
        try:
            #새롭게 추가된 클라이언트가 있을 경우 Send 쓰레드를 새롭게 만들기 위해 루프를 빠져나감
            recv = send_queue.get() #큐 안에있는 데이터를 리스트 자료형으로 받는 객체 recv생성
            if recv == 'Group Changed': #보내는 그룹(소켓정보)가 바뀐 경우 출력
                print('Group Changed')
                break #반복문 종료

                #recv가 'Group Changed'가 아닌경우
            #for 문을 돌면서 모든 클라이언트에게 동일한 메시지를 보냄(연결된 순서대로)

            ##문자열 보내는 부분##
            for conn in group: #??????????? #소켓정보(변수)를 클라이언트 채팅방 목록속 채팅방의 리스트 요소만큼 순서대로 반복 ex)[[1,a,b,c,0]]??
                message = str(recv[0])# 정수나 실수를 문자열의 형태로 변환하는 str함수에 큐의 첫번째
                                    #즉, send_queue의 첫번째 데이터를 넣어서 문자열화 시킨다.
                if recv[1] != conn: #만약 recv[]의 1번 인덱스(2번째 인덱스)가 conn(변수):client 본인이 아니면   
                    #client 본인이 보낸 메시지는 받을 필요가 없기 때문에 제외시킴
                    print(message) # 문자열로 변환시킨 메시지를 출력한다

                    #==========이부분에서 조건식 추가해야함 같은 리스트 구성원들에게만 보낼 수 있게=================================
                    conn.send(bytes(message.encode())) #masssage 객체의 인코딩(부호화된 바이트)값이 들어있는 바이트 객체-받는 표준은 UTF-8
                                                        #(1바이트 단위의 값을 연속적으로 저장하는 시퀀스 자료형)를 생성하고 
                                                        #이것을 conn(그룹리스트중 현재 소켓정보)에게 send(모듈에 포함되어있는 함수)한다
                
                else:
                    pass #구문상 필요하지만 작업이 필요없어서 내부동작 x
        except:
            pass #구문상 필요하지만 작업이 필요없어서 내부동작 x

#recv[0] == 문자열, recv[1] == 보낸 클라이언트의 소켓정보 , recv[2~]: 보낼 클라이언트의 소켓저보


def Recv(conn, count, send_queue): #read() 함수 구현 #멀티 쓰레드 안에서 recv 함수 수행됨
    print('Thread Recv(' + str(count) + ') Start\n')#몇번째 쓰레드가 시작되었는지 출력
    ## 문자열 출력 부분 ##
    while True:
        message = conn.recv(1024).decode()#부호화된 내부코드를 디코딩해서 문자열로 변경 후 
                                        #recv함수로 해당 소켓(conn)에게 온 문자열로 이루어진 메세지 객체생성
        print(f"RECEIVE([{SERVER}:6060][Thread:{str(count)}]{message})") #클라이언트 쓰레드 번호문자열을 서버 터미널창에 출력 이때 닉네임은 문자열안에[닉네임] ㅇㅇㅇ으로있음
        send_queue.put([message, conn, count]) #([닉네임] 문자열)의 문자열 값을 지닌 메세지 값과, conn(소켓정보)값, 쓰레드번호값을 각각 큐에 추가한다.
        #이러면 큐 리스트에 순서대로 message, conn, count값이 추가됨(큐는 선입 선출)이므로 메세지부터 들어가고 메세지부터 나옴
        #각각의 클라이언트의 메시지, 소켓정보, 쓰레드 번호를 send로 보냄
#이 .py파일이 모듈로 사용되지 않고 직접쓰일때만 사용되게함 

if __name__ == '__main__': 

    # 큐 생성, 무엇을 위한 큐? -> 보내려는 데이터를 큐에 저장한다. (큐는 무한)
    send_queue = Queue()  #큐는 아마도 리스트 자료형으로 저장됨

    # PORT 지정
    PORT = 6060

    # SERVER 정보 설정
    SERVER = socket.gethostbyname(socket.gethostname())
    # socket.gethostname() -> PC Name, 로컬호스트 이름 반환
    # socket.gethostbyname(PC Name) -> IP Adress, 로컬 호스트 ip주소 반환

    # Final Server Aress
    ADDR = (SERVER, PORT) #ADDR은 주소의 의미를 가진다, 따라서 고정값인 튜플 자료형으로 생성
    # result : ('PC Adress(IPV4)', PORT(6060))

    #서버 ip주소와 포트번호를 안내해주는 안내문
    print(f"\n서버 시작 중......\n서버 주소와 포트번호: {SERVER}:{PORT}\n") 

    # socket 설정
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # 사용할 통신 영역: AF_INET -> 해당 소켓은 IPV4(IP version 4)로 사용을 의미
    # 프로토콜 타입: SOCK_STREAM -> 해당 소켓에 TCP 패킷을 받겠다는 의미

    # 서버와 PORT 연결
    server.bind(ADDR)
    # 서버(PC Adress(IPV4))에 PORT(6060)를 연결
    # bind는 값을 튜플로 받기에 괄호가 두개가 된다.
    # result :('PC Adress', 6060)

    server.listen() #인자는 외부 연결을 거부하기 전에 최대 (?)개의 연결 요청을 큐에 넣기를 원한다는 것을 소켓 라이브러리에 알립니다.
    # server에 새로운 연결을 listen
    # 소켓 연결, 여기서 파라미터는 접속수를 의미
    print(f"※LISTENING※\nserver is listening on {SERVER}\n")

    count = 0 
    # 쓰레드(클라이언트) 번호 카운트
    group = [] #연결된 클라이언트의 소켓정보를 리스트로 묶기 위한 그룹
    ######서버(소켓) 작동준비 끝 #####
try:
    while True:
        count += 1 #클라이언트를 받기위한 쓰레드 번호 1증가 #처음엔 1번쓰레드
        conn, addr = server.accept() # 해당 소켓을 열고 클라이언트의 연결 요청을 대기
        #API에서, 데이터 송수신을 위한 새로운 소켓(Socket)을 만들고 서버 소켓의 대기 큐에 쌓여있는 첫 번째 연결 요청을 매핑시킨다
        #반환 값은 (conn, address) 튜플쌍입니다. 여기서 conn는 연결에서 데이터를 보내고 받을 수 있는 새로운 소켓 객체이고, 
        #address는 연결의 다른 끝에 있는 소켓에 바인드 된 주소입니다.

        group.append(conn) 
        #연결된 클라이언트의 소켓정보를 group 리스트에 추가한다. 즉 [(소켓정보, IP주소)(소켓정보, IP주소)(소켓정보, IP주소)] 형태로 group에 추가됨.
        print(f"※신규 연결※\n{str(addr)} 접속했습니다..") #접속한 클라이언트의 IP주소를 출력한다.
        global rooms 
        rooms = [] # 생성되는 채팅방들
                    #################### 여기부터 채팅영역을 위한 쓰레드생성#########################################
        #쓰레드란? 한개의 프로세스로 2가지 이상의 일을 하기위한 작업 수행 주체, 2개이상이므로 멀티 쓰레드가 된다.
        #소켓에 연결된 모든 클라이언트에게 동일한 메시지를 보내기 위한 쓰레드(브로드캐스트)
        #연결된 클라이언트가 1명 이상일 경우 변경된 group 리스트로 반영
        if count > 1: #만약 쓰레드(클라이언트가 2명 이상이면)
            send_queue.put('Group Changed') #send_queue큐에 'Group Changed'즉 소켓정보가 새로 바뀌었다(추가됨)는 정보를 삽입
            #threading 모듈의 threading.Thread()호출로 쓰레드 객체생성
            sendthread = threading.Thread(target=Send, args=(group, send_queue))#send쓰레드가 실행할 함수 와 그 함수의 인자값(튜플)이 인자로 들어감
            sendthread.start() #Thread 객체의 start() 메서드를 호출하여 send쓰레드 시작
            pass
        else: #클라이언트 첫입장(1명)
            sendthread = threading.Thread(target=Send, args=(group, send_queue))#쓰레드가 실행할 함수 와 그 함수의 인자값(튜플)이 인자로 들어감
            sendthread.start()

            #소켓에 연결된 각각의 클라이언트의 메시지를 받을 쓰레드
            recvthread = threading.Thread(target=Recv, args=(conn, count, send_queue))#recv쓰레드 객체 생성및 위의 주석과 같은 역할
            recvthread.start() #recvThread 객체의 start() 메서드를 호출하여 recv쓰레드 시작

        # MySQL 데이터베이스에 연결
        db_connection = pymysql.connect(
            host="localhost",  # 호스트 주소
            user="root",   # MySQL 사용자 이름
            password="0000",  # MySQL 비밀번호
            database="cuktaxi"  # 데이터베이스 이름
        )

        # 커서 생성
        cursor = db_connection.cursor()

        #### 사용자 정보 확인 및 추가
        def check_user(phone_number):
            cursor.execute('SELECT * FROM users WHERE phone_number = %s', (phone_number))
            user = cursor.fetchone()
            cursor.execute('SELECT user_id FROM users WHERE phone_number = %s', (phone_number))
            user_id = cursor.fetchone()
            # print(user_id)
            if user:
                print(f'사용자 {phone_number}의 보증금 포인트는 {user[2]}점입니다.')
                return user_id
            else:
                # 새 사용자를 추가하고 초기 포인트를 설정
                sql='INSERT INTO users (phone_number, point) VALUES (%s, %s);'
                cursor.execute(sql, (phone_number, 500))
                db_connection.commit()
                print(f'새로운 사용자 {phone_number}가 추가되었습니다. 초기 보증금 포인트는 500점입니다.')

                return user_id

        ###########이부분은 아마도 클라이언트 창에 생성?
        print("반갑습니다! CUKTAXI 입니다!")
        phone_number = input('전화번호를 입력하세요: ')


        #######클라이언트 한테 넘겨받아서 DB에저장######
        user_id=check_user(phone_number)

        #### POSTS
        def show_menu():
            print("1. 게시글 생성")
            print("2. 게시글 참여")
            choice = input("원하는 역할을 선택하세요 (1 또는 2): ")
            return choice

        role = show_menu()
        if role == '1':  # 게시글 생성
            ride_time_str = input("탑승 시간을 입력하세요 (HH:MM 형식): ")
            ride_time_datetime = datetime.strptime(ride_time_str, "%H:%M")
            formatted_ride_time = ride_time_datetime.strftime("%H:%M:%S")
            # "formatted_ride_time"에서 시간 부분만 추출
            formatted_ride_time = formatted_ride_time[:5]

            pickup_location = input("탑승지를 입력하세요: ")
            destination = input("목적지를 입력하세요: ")

            sql = "INSERT INTO posts (user_id, ride_time, pickup_location, destination) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (user_id, formatted_ride_time, pickup_location, destination))

            db_connection.commit()
            print("게시글이 생성되었습니다.")

            #이제 채팅방을 생성해야함
            def createChatRoom(createUser, createNumber):
                room = [createNumber, createUser, 0, 0, 0]# [방번호, 유저, 유저, 유저, 유저]로 구성된 리스트를 생성
                rooms.append(room) #채팅방 리스트에 첫번째요소:방번호, 두번째 요소 유저명 리스트를 추가 ex)[[createNumber, createUser], [createNumber, createUser]...]
                #아래 쓰레드에서 할일: send와 recv를 리스트마다 적용시키게 하기
                return 0
            
            createUser = user_id
            createNumber = #생성된 게시판 번호
            createChatRoom(createUser, createNumber)


        elif role == '2':  # 게시글 참여
            # 게시글 목록 가져오기
            cursor.execute("SELECT id, ride_time, pickup_location, destination, user_id FROM posts")
            posts = cursor.fetchall()
        
            # 게시글 목록 출력
            for post in posts:
                post_id, ride_time, pickup_location, destination, owner_id = post
                print(f"게시글 ID: {post_id}, 탑승 시간: {ride_time}, 탑승지: {pickup_location}, 목적지: {destination}, 소유자 ID: {owner_id}")

            post_id_to_join = input("참여하려는 게시글의 ID를 입력하세요: ")

            # 게시글에 참여
            sql = "INSERT INTO participants (post_id, user_id) VALUES (%s, %s)"
            cursor.execute(sql, (post_id_to_join, user_id))
            db_connection.commit()
            print("게시글에 참여되었습니다.")
        ## 게시글 테이블에 유저 1,2,3 컬럼에 각 참여자 id 추가
        # 이제 채팅방에 참여해야함
        def joinChatRoom(joinUser, joinNumber):
            if rooms[joinNumber][0] == joinNumber: # joinNumber(방번호)가 joinNumber(방번호)번째 리스트에 첫번째 인덱스가 joinNumber(방확인 번호)이 맞으면
                rooms.insert(rooms[joinNumber],joinUser) #joinNumber번째 리스트의 n번째 요소로joinUser를 추가
                                                            #ex)[[createNumber, createUser, joinUser]]
            else:
                print("해당 채팅방이 생성되어 있지 않습니다.")
            return 0
            joinUser = user_id
            joinNumber = post_id_to_join
            joinChatRoom(joinUser, joinNumber)

        # 연결 종료
        cursor.close()
        db_connection.close()
finally:
    server.close()# 서버 소켓 닫기
