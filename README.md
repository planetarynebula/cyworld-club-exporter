# Cyworld Club Grep

# 현재 싸이월드 서버가 죽어서 프로그램이 작동하지 않습니다. 

## 무엇인가요?
- javascript 코드: 싸이월드 클럽을 추출해서 json 으로 저장하는 스크립트입니다.
- python 코드: json으로 저장된 파일들을 폴더 형식으로 분류해주는 스크립트입니다.

그리기 게시판, 메모 게시판, 프리톡 게시판은 지원하지 않습니다.

## 저작권
MIT 라이센서를 따릅니다.
변경 및 재배포는 자유입니다! 
다만 원 라이센스의 github 경로는 명시해주세요.

[https://github.com/bab2min/cyworld-club-exporter](https://github.com/bab2min/cyworld-club-exporter) 에서 포크함.

## 필요한것은?
- node.js
- npm modules
  - http
  - https
  - querystring
  - async
  - crypto
  - stream
  - fs
  - iconv-lite
  - cheerio
  - html-entities
  - follow-redirects
  - progress
 
- python3
  - bs4

## 설정은
- core/config.js 에서 아래의 항목을 수정하여 주세요!!
  - userId : 싸이월드 아이디
  - password : 싸이월드 패스워드
  - clubId : 싸이월드 클럽아이디 (ex: http://club.cyworld.com/ClubV1/Home.cy/52172895 -> 52172895 만 작성)

## 실행은
먼저 npm module 설치를 위해 `npm install`을 실행.

순차적으로 실행.
```
node 01_articleListGrep.js // 전체 글보기 리스트 파일로 저장
node 02_articleViewGrep.js // 전체 글보기 게시물 파일로 저장
node 03_galleryListGrep.js // 전체 사진보기 리스트 파일로 저장
node 04_galleryViewGrep.js // 전체 사진보기 게시물 파일로 저장
node 05_commentGrep.js // 모든 게시물 댓글 파일로 저장
node 06_imageQueueGrep.js // 게시물내 첨부 이미지 저장 준비
node 07_imageGrep.js // 첨부 이미지 다운로드
```
result 폴더에 게시글 정보가 json 형식으로 저장되고, images 폴더에 사진과 첨부 파일이 저장됨.

`python3 script.py` 실행.

article 폴더에 게시글이, gallery 폴더에 사진첩이 저장됨.

폴더가 `카테고리명/[작성일] 게시글 명 (작성자)` 형식으로 생성되며 폴더 안에 게시글(`html` 파일), 사진 및 첨부파일, 댓글(`txt` 파일)이 저장 됨.
