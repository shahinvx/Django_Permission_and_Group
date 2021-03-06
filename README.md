## Run This Django app (instructions)

- `Take a live demo`  [Click Here](https://django-perm.herokuapp.com/ "Heroku APP Demo") `or go django-perm.herokuapp.com`
- `YouTube link` [Click for YouTube](https://www.youtube.com/watch?v=ERmFW2bkFXY "For Video demo") 
- `git clone github.com/shahinvx/Django_Permission_and_Group.git`
- `cd Django_Permission_and_Group`
- `pip install -r requirements.txt`
- `python manage.py runserver`
- `open http://127.0.0.1:8000/ in your browser` or [Click Here](https://django-perm.herokuapp.com/ "Heroku APP Demo")
- `Admin/Login user : shahinvx | pass : shahin `
- `User Delete Secret Key : shahin | don't think it will always same as password`

## All API in Swagger Documentation

- `http://127.0.0.1:8000/swagger/` or `django-perm.herokuapp.com/swagger` [Click Here](https://django-perm.herokuapp.com/swagger "Swagger API DOC")
- `http://127.0.0.1:8000/redoc/` or `django-perm.herokuapp.com/redoc` [Click Here](https://django-perm.herokuapp.com/redoc "Redoc API DOC")

## About this APP

In short this APP is about to Understand Django User Permission and Group Permission , Session and Token Authentication.

- User
  - User Create, Update, Login, Register 
  - Assign Permission, Assaing to Group, Remove from Group | [Pemission and Group Control]
  - Delete User with Confirmation of Secret Key [Secret Key : shahin].
  
- Group
  - Group Create, Update, Delete
  - Assign and Remove Group Permission, Update Group Properties and Pemission, Delete Group | [Group Permission Control]
  
- Authentication
  - Session and Token Authentication
  
- Additional INFO
  - DRF (Django Rest Framework)
  - Swagger and Redoc for Documentation
  - Django Templates with ajax and javascript

## Swegger Documentation preview

![Swegger Documentation](/Screen_Doc/all_api.png)

## Redoc Documentation preview

![Redoc Documentation](/Screen_Doc/redoc_2.PNG)

## All View inside APP

<img src="/Screen_Doc/login.png" width="412" height="235"> <img src="/Screen_Doc/register.png" width="412" height="235">
<img src="/Screen_Doc/home.PNG" width="412" height="235"> <img src="/Screen_Doc/group.png" width="412" height="235">
<img src="/Screen_Doc/perm_off.png" width="412" height="235"> <img src="/Screen_Doc/perm_on.png" width="412" height="235">
<img src="/Screen_Doc/user_control.png" width="995" height="460"> 
<img src="/Screen_Doc/update_info.png" width="412" height="235"> <img src="/Screen_Doc/del_confirm.png" width="412" height="235">

#
### The MIT License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
