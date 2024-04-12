# SRL Buddy Django Web Application

SRL Buddy is a learning management system with a Learning Analytics Dashbored(LAD) and fetaures to help students manage their learning online. It incoporates features that help students improve self-regulated learning(SRL) such as data visualisations, planning prompts, and reflections, which help them engage their strategic-planning, time management and self-management skills.

## Setup
#### Prerequisites

*  Make sure to have Python3.x and pip downloaded 

    Python : check this by using ``` python3 --version ```. If it is downloaded it will show you a version number.

    If you find that you do not have Python3 installed on your computer, then you can download it for free from the following website: https://www.python.org/

    pip : check this by using ``` pip --version ```. If it is downloaded it will show you a version number.

    If you do not have pip installed, you can download and install it from this page: https://pypi.org/project/pip/

### Step 1 : Navigate to the project directory

```sh
cd studytool
```

### Step 2 : Create virtual environment

```sh
python3 -m venv venv
```
This will create a new directory named `venv` in your project directory, containing the virtual environment.

### Step 3 : Activate  virtual environment

On Windows run:

```sh
venv\Scripts\activate
```
On MacOS/Linux run:

```sh
source venv/bin/activate
```
You should see `(venv)` appear at the beginning of your command prompt, indicating that the virtual environment is active.

### Step 4 : Install Project dependencies

```sh
pip install -r requirements.txt
```

### Step 5 : Apply Migrations

```sh
python3 manage.py makemigrations

python3 manage.py migrate
```

### Step 6 : Populate database

```sh
python3 manage.py populate_db
```

This will create the objects used to demonstrate this project

### Step 7 : Run the server

```sh
python3 manage.py runserver
```
And navigate to `http://127.0.0.1:8000/polls/`.

## User Guide

### Sign up
The application is made with an existing student database in mind therefore sign up requires valid StudentIDs

You can sign up with the following ID, and provide your own password:
```
studentID : jack.doe
```
Signing up shows you a new user view where no plans or reflections have been made but the student is registered to modules and can use the Learning Analytics Dashboard.

### Login

One student account has been set up to show the use of the system over time. 

You can log in with the following user credentials :
```
studentID : peter.piper
password: Password123
```
This account is setup to have been used for 3 of the 5 weeks of data provided and shows pre made plans and reflections. You can also see the notification system. 

**Admin Account**

You can create a super user using the command :
```
python3 manage.py createsuperuser
```

This will prompt you to add a username, email and password, and then you can login to the admin site `http://127.0.0.1:8000/admin/`.
Here you will be able to see database tables.

### Functionality you can test

There are a number of ways you can canigate the system and a good place to start can be the 'Workload Overview' page. From there you will be able to see what features exist and you can navigate through to creating and editing plans and reflections.

Here are some features you can start with:

* Workload Overview - apply filters and interact with the charts
* Workload Overview Plan - type out information and save a plan
* Workload Overview Plan - edit information and save the plan
* Module page - check items and see progress changes in Workload Overview
* Plans - see old plans list and click on plans to view, edit or reflect on
* Reflection - reflect on plan
* Reflections - see old reflections list


