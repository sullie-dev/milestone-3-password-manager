# Password Manager


[View project here](https://milestone-3-password-manager.herokuapp.com/) password is  `pw123`.  
This is a demo project please **do not store any real passwords** as passwords are returned as plain text to the users when viewing passwords

---

For this project I have built a terminal password manager in python, the program allows the user to input & save new passwords along with view passwords based on the website name, username/email, or password name.

All the passwords are encrypted and stored on a PostgreSQL database on Heroku, when the user retrieves the passwords they are decrypted and displayed to the user

![Am I responsive](https://i.imgur.com/JYgG0h5.png)

Responsiveness was checked using
[Am I responsive](http://ami.responsivedesign.is/), although I’ve used the template provided mobile input does not seem to work 

## Deployment

The project and database are deployed on Heroku, under the same project using the hobby plan

#### Python Project
* Once project is ready enter `pip3 freeze > requirments.txt` 
into the command line to build requirements file

1. Head to [Heroku](https://heroku.com)
2. New > Create new app
3. Add a unique name and choose the region 
   * Europe was used for this project
4. Create app
5. Set the build packs as
   * Python
   * Node.js
6. Add Config Vars
    * `PORT 8000` needs to be included
7. Link the GitHub repository
8. Deploy the project

#### PostgreSQL database
1. In the Heroku project head to Resources
2. Search for `PostgreSQL` in add-ons
3. Select plan
    * Hobby plan was used for this
4. Get database credentials by clicking on the database name
5. Set up preferred database tool with the info

## Features
![Features password manager offer](https://i.imgur.com/sbKdO6Z.png)
### Current features
Currently, the password manager offers its users the ability to:

* Login via authentication 
* Create a new password entry
    * Username 
    * Password 
    * Website name
    * Unique password name 
* Generate a random password between 8 and 25 characters long 
* Save the password to the database
* Search the database for a password by
    * Website name
    * Password name
    * Search for all passwords 

### Future features
In future build if this password manager I would like to offer the abilities:
* Update the master password for authentication 
* Edit passwords:
    * Username
    * Password
    * Website name
    * Password name
---

### Validation Testing
The code base was checked using [PEP8 online check](http://pep8online.com/), there are several E501 errors showing that lines are too long, 
![PEP8 errors](https://i.imgur.com/9wqNrxg.png)

When reviewing the code in PyCharm IDE, the errors showing up are that some variable may be referenced before assignment, there is also a typo error  shown for the opening string when signing in but the word ‘Kittridge’ is spelt right.

![PyCharm errors](https://i.imgur.com/FucM8Gy.png)


## Bugs:

---

### Solved bugs:
* One of the main bugs I was running into with the project was I encrypted the password using base64 but was decrypting it in base16 which caused an illegal key error: `None-base16 digit found`

![base16 error](https://i.imgur.com/I65TPSw.png)

This was resolved by changing the decode function to use `base64` format

* Another bug I ran into was when I attempted to convert the original key of 2 separate sales into bytes there was an encoding error, this was caused by not adding  `utf-8` to the conversion


![bytes encoding error](https://i.imgur.com/eIc6k89.png)

* The main bug I encountered was with the decrypt function, where for some passwords the decryption method was looking for additional padding being added to the encrypted password, when being passing in via a variable. When I was passing the string in directly the password was bing decrypted as expected.

![Additional padding error](https://i.imgur.com/BFfBi6N.png)

These 2 bugs were resolved by rewriting how the passwords were encrypted and decrypted. I used a python package called cryptography which handled encoding and decoding the passwords by using a randomly generated key

### Unsolved bugs:

There are no unsolved bugs

## Content

---

### Credits
When researching for this project I came across several articles and a GitHub repository to help with aspects of the project

* Project was inspired by the YouTuber Kalle Hallden, [GitHub - KalleHallden/pwManager](https://github.com/KalleHallden/pwManager)
* [Medium article on password generation](https://link.medium.com/9bV7eNhjslb)
* [Python PostgreSQL CRUD - Insert, Update and Delete table data](https://pynative.com/python-postgresql-insert-update-delete-table-data-to-perform-crud-operations/#h-python-postgresql-insert-into-database-table)
* [Create tables in Python](https://link.medium.com/swWtzRkjslb)

### Media
No media used in this project, the code template used to show the terminal 
[GitHub - Code-Institute-Org/python-essentials-template: Deployment template for students to use for P3](https://github.com/Code-Institute-Org/python-essentials-template)

##Technologies used

---

* [Deployment template](https://github.com/Code-Institute-Org/python-essentials-template)
* Python
* PostgreSQL
* [Heroku](https://heroku.com)
* [pgAdmin4](https://www.pgadmin.org/)
