# 2026_PBL_BE_DJANGO

멋쟁이사자처럼 대학 백엔드(Python) Django 커리큘럼을 위한 실습 레포지토리입니다.  
본 레포지토리는 **콘솔 기반 Python 학습 이후**,  
**웹 프레임워크 Django의 기본 구조와 요청–응답 흐름을 이해하는 것**을 목표로 합니다.

---

## 📌 레포지토리 목적

- Django 프로젝트의 기본 구조를 이해합니다.
- URL → View → Template 흐름을 직접 구현합니다.
- 서버 상태와 화면 렌더링의 관계를 학습합니다.
- Form 처리와 데이터 저장 과정을 경험합니다.
- 이후 REST API / Spring Boot / DRF 학습으로 확장 가능한 기초를 다집니다.

> 본 레포지토리는 **Django 입문 과정 (4~5주차)** 를 다룹니다.

---

## 🧭 Python → Django 전환 포인트

### 콘솔 프로그램까지 했던 것
- 입력 → 처리 → 출력
- 함수와 클래스
- 객체 책임 분리

### Django에서 새롭게 등장하는 것
- URL을 통한 요청(Request)
- View 함수가 요청을 처리
- Template으로 화면 응답(Response)
- 서버 상태(DB)와 화면의 연결

> Django는 “새 문법”이 아니라  
> **지금까지 만든 로직을 웹 구조에 얹는 단계**입니다.

---

## 🗂 디렉토리 구조

```text
2026_PBL_BE_DJANGO/
├── class4/                         # 4주차: Django 기본 구조
│   ├── lion_project/               # Django 프로젝트 설정
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── lions/                      # Django 앱
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── templates/                  # HTML 템플릿
│   │   ├── home.html
│   │   └── lions.html
│   │
│   ├── db.sqlite3                  # SQLite 데이터베이스
│   └── manage.py
│
└── class5/                         # 5주차: Form 처리와 데이터 저장
    ├── lion_form_project/
    ├── lions/
    │   ├── migrations/
    │   ├── models.py
    │   ├── urls.py
    │   └── views.py
    │
    ├── templates/
    │   └── lions/
    │       ├── base.html
    │       ├── home.html
    │       ├── list.html
    │       └── new.html
    │
    ├── db.sqlite3
    └── manage.py
```
## 🎯 주차별 학습 내용

4주차 (class4)

- Django 기본 구조와 화면 렌더링
- Django 프로젝트 생성
- 앱(App)의 개념
- URL 설정 (urls.py)
- View 함수 작성
- Template을 이용한 화면 출력
- 서버 실행 흐름 이해

핵심 흐름
```
브라우저 요청
 → urls.py
   → views.py
     → template(html)
```

5주차 (class5)

- Form 처리와 서버 상태 변경
- HTML Form 이해
- GET / POST 요청 차이
- 사용자 입력 처리
- Model을 통한 데이터 저장
- 목록 화면 / 등록 화면 분리
- POST → Redirect 패턴 이해

핵심 흐름
```
사용자 입력
 → POST 요청
   → View 처리
     → DB 저장
       → Redirect
         → 목록 화면
```

## 🛠 주요 파일 설명

manage.py
- Django 명령어 실행 진입점
- 서버 실행, 마이그레이션, 앱 생성 등 담당

settings.py
- 프로젝트 전체 설정
- 앱 등록, 템플릿 경로, DB 설정

urls.py
- URL과 View 연결
- 요청의 진입점

views.py
- 요청을 처리하는 함수
- 화면 또는 응답 반환

models.py
- 데이터 구조 정의
- Django ORM 기반 DB 연동
