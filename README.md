Fyyur
-----

### Introduction

Fyyur is an application where musical artists can meet musical venues. 

1. Artists and venues can visit this site in order to post information about themselves as well as find each other
2. This site lists information about different venues across different cities, as well as different artists that exist.
3. From here, you can also discover shows where different artists are playing at different venues.
4. On this site, you have a chance to post a venue and list a new venue if that venue hasn't yet been listed, you could do the same thing with artists as well as shows, you can also find artists and venues.
5. For a particular artist, you can view information about their genre, contact information, whether or not they are currently seeking talent, as well as information about their upcoming and past shows.
6. There's also information about artists here who are also seeking performance venues to play at, as well as information about their upcoming and past shows.

### Tech Stack (Dependencies)

## Backend Dependencies

Our backend tech stack will include the following:

* **A virtual environment** provided in the workspace
* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations


### Installing Backend Dependencies

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/ (i.e, step 1: cd desktop, step 2: cd fyyur-project)
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```
2. Install SQLAlchemy
```
  $ pip install SQLAlchemy
  ```
3. Install Postgres

```
  $ pip install postgres
  ```
4. Install Flask

```
  $ pip install Flask
  ```
5. Install Flask-Migration

```
  $ pip install Flask-Migrate
  ```

## Front Dependencies

* **HTML**
* **CSS**
* **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) 

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. 
                    "python3 app.py" to run after installing dependences
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py ***  Forms
  ├── models.py  *** SQL Alchemy models
  ├── requirements.txt 
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```


### Development Setup


To start and run the local development server,


1. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

2. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
  ```

3. Navigate to Home page [http://127.0.0.1:5000](http://127.0.0.1:5000)
