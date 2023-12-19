# 사용자에게 필요한 정보를 얻는 함수

def get_user_input():
    channel = str(input("youtube에서 검색할 크리에이터 아이디 : "))
    cnt = int(input("수집할 영상 갯수 : "))
    dir = str(input("결과값을 저장할 디렉토리 : "))
    frame_interval = int(input("Enter the frame interval in seconds: ")) # 사용자로부터 프레임 간격 입력 받기 (예: 5초마다)

    print("\n")
    print("요청한 정보로 데이터를 수집중")
    return channel, cnt, dir, frame_interval