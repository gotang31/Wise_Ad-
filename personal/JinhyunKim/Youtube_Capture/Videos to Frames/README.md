- IDE 폴더 : IDE 상에서 실행가능한 코드파일
- Application 폴더 : VtF.exe 파일 제작에 사용된 소스파일
# 주의사항
- ### Chrome 버전이 119.0- 인지 확인 필수!



# 필수 설치 패키지

| pip install **{package_name}** |
|--------------------------------|
| undetected_chromedriver        |
| selenium==4.9.0                |
| bs4                            |
| pandas                         |
| re                             |
| pytube                         |
| opencv-python                  |


# 프로그램 구현 방식
1. 크리에이터 ID / 최근 영상부터 저장할 영상 갯수 / 저장 경로 지정 / 추출할 이미지 간격(초) 입력
2. selenium 이용해 크리에이터의 유튜브 영상 목록 사이트로 접속
3. df로 영상 제목 및 url 저장 
4. pytube 이용해 영상을 저장 경로 안에 {영상제목}.mp4 파일로 저장 
5. OpenCV 이용해 {영상 제목} 폴더 안에 지정한 이미지 간격(초) 단위로 분할한 .jpg 이미지 생성
