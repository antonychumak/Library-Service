# Library-Service


### How to run:
 - git clone https://github.com/anton-chumak-main/Library-Service.git
 - python3 -m venv venv
 - source venv/bin/activate
 - Copy .env.sample -> .env and populate with all required data
 - 'docker compose up --build'
 - Install [ModHeader](https://chrome.google.com/webstore/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj?hl=en) extention and use Bearer < Your access token >
 - Create schedule for running sync in DB


## Features:

- Admin panel 
- JWT authentication
- Swagger documentation
- Add permissions for different users and services
- Add filtering for the Borrowings List endpoint
- Book counting and inventory
- Implement return Borrowing functionality
- Implement the possibility of sending notifications on each Borrowing creation
- Implement a function for checking borrowings overdue
- Add Celery with Flower monitoring tool

# Components:
Books Service:
* API:
    - POST: books/ - add new 
    - GET: books/ - get a list of books
    - GET: books/<id>/      - get book's detail info 
    - PUT/PATCH: books/<id>/      - update book (also manage inventory)
    - DELETE: books/<id>/      - delete book

Users Service:
* API:
  - POST:users/ - register a new user 
  - POST:users/token/ - get JWT tokens 
  - POST:users/token/refresh/  - refresh JWT token 
  - GET:users/me/  - get my profile info 
  - PUT/PATCH: users/me/  - update profile info 

Borrowings Service:
* API:
  - POST:borrowings/ - add new borrowing (when borrow book - inventory should be made -= 1) 
  - GET:borrowings/?user_id=...&is_active=...  - get borrowings by user id and whether is borrowing still active or not.
  - GET:borrowings/<id>/  - get specific borrowing 
  - POST:borrowings/<id>/return/ - set actual return date (inventory should be made += 1)
  - POST:borrowings/
  - Notifications Service (Telegram):
  - Notifications about new borrowing created, borrowings overdue
  - Usage of Telegram API, Telegram Chats & Bots.
