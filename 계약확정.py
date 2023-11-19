# 게시판에 있는 탑승시간을 저장하는 딕셔너리 예시
board = {"1게시물": "2023-10-27 03:30:00", "2게시물": "2023-10-27 04:00:00", "3게시물": "2023-10-27 04:15:00"}


# datetime 모듈을 임포트
import datetime

# 탑승시간보다 -10분한 시간을 제한시간으로 설정하는 함수
def set_deadline(time):
    # 문자열로 된 탑승시간을 datetime 객체로 변환
    boarding_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    # 탑승시간에서 10분을 빼서 제한시간을 계산
    deadline = boarding_time - datetime.timedelta(minutes=10)
    # 제한시간을 문자열로 반환
    return deadline.strftime("%Y-%m-%d %H:%M:%S")

# 게시판의 각 key에 대해 제한시간을 설정하고 출력하는 반복문
for key in board:
    # key값으로 탑승시간에 접근
    time = board[key]
    # 제한시간을 설정하는 함수를 호출
    deadline = set_deadline(time)
    # key와 제한시간을 출력
    print(f"{key}의 제한시간은 {deadline}입니다.")

# 현재 시간을 datetime 객체로 저장
now = datetime.datetime.now()
# 합승 계약이 확정된 key들을 저장할 리스트
confirmed = []

# 게시판의 각 key에 대해 현재 시간과 제한시간을 비교하고 합승 계약을 확정하는 반복문
for key in board:
    # key값으로 탑승시간에 접근
    time = board[key]
    # 제한시간을 설정하는 함수를 호출
    deadline = set_deadline(time)
    # 제한시간을 datetime 객체로 변환
    deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
    # 현재 시간이 제한시간보다 크거나 같으면
    if now >= deadline:
        # 합승 계약이 확정된 key들의 리스트에 key를 추가
        confirmed.append(key)
        # 합승 계약이 확정되었다고 출력
        print(f"{key}님의 합승 계약이 확정되었습니다.")

# 합승 계약이 확정된 key들의 리스트를 출력
print(f"합승 계약이 확정된 게시판들은 {confirmed}입니다.")