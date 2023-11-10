# 사용자에게 필요한 정보를 얻는 함수

def get_user_input():
    channel = str(input("youtube에서 검색할 크리에이터 아이디 : "))
    cnt = int(input("수집할 영상 갯수 : "))
    dir = str(input("결과값을 저장할 디렉토리 : "))


    print("\n")
    print("요청한 정보로 데이터를 수집중")
    return channel, cnt, dir