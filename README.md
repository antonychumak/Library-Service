# Library-Service

There is a library in your city, where you can borrow books and pay 
for your borrowings using cash, depending on the days you read the book.

### How to run:
To run the app, `docker` and `docker-compose` must be installed on your system. For installation
instructions refer to the Docker [docs](https://docs.docker.com/compose/install/).
 - ```git clone``` https://github.com/anton-chumak-main/Library-Service.git
 - Create venv: ```python3 -m venv venv```
 - Activate it: ```source venv/bin/activate```
 - Create .env files in the root of the project 
 - Copy all the variables with .env.sample into .env
 - Populate with all required data. To test functionality use: 
   - login: admin@example.com
   - password: mypass123
 - Bring up the docker stack: ```docker compose up --build```
 - Get access token via /api/users/token/ (set email and password for django user according to your .env file)
 - Install [ModHeader](https://chrome.google.com/webstore/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj?hl=en)
    extension and use Bearer < Your access token >
 - Create schedule for running sync in DB


## Features:
- JWT authentication
- Powerful admin panel for advanced managing /admin/
- Documentation is located at /api/doc/swagger/ OR api/doc/redoc/
- Add permissions for different users and services
- Add filtering for the Borrowings List endpoint
- Book counting and inventory
- Implement return Borrowing functionality
- Implement the possibility of sending notifications on each Borrowing creation
- Implement a function for checking borrowings overdue
- Add Celery with Flower (monitor tasks in flower: http://localhost:5555)

# Components:
Books Service:
* API:
    - POST: books/ - add new 
    - GET: books/ - get a list of books
    - GET: books/< id >/   - get book's detail info 
    - PUT/PATCH: books/< id >/  - update book (also manage inventory)
    - DELETE: books/< id >/     - delete book

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
  - GET:borrowings/< id >/  - get specific borrowing 
  - POST:borrowings/< id >/close_borrow/ - set actual return date (inventory should be made += 1)
  - POST:borrowings/
  - Notifications Service (Telegram):
  - Notifications about new borrowing created, borrowings overdue
  - Usage of Telegram API, Telegram Chats & Bots.
