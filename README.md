# Welcome to Check Mate

Check Mate was developed out of necessity to streamline the project management process for software developers. The current tools available to manage the process of integrating new features into a project are cumbersome and not easy to work with. Most importantly, these options do not provide software developers with the most essential information to them so that they can easily communicate their priorities for the day during stand up meetings. By creating a more intuitive user flow, developers will be able to spend less time managing their projects and more time doing what they do best, solving problems.

## Table of Contents
<!-- [Project Requirements and Features List](#project-requirements-and-features-list) -->
* [Technologies Used](#technologies-used)
* [Installing and Launching Check Mate](#instructions-for-installing-check-mate)
* [Appendix: Planning Documentation](#appendix-planning-documentation)
  * [Entity Relationship Diagrams](#entity-relationship-diagram)
  * [Wireframes](#wireframes)

<!-- ## Project Requirements and Features List -->

## Technologies Used
  ### Development Languages and Libraries
  <img src="./src/images/django.svg" width="10%"></img> <img src="./src/images/python.svg" width="10%"></img>
  ### Development Tools
  <img src="./src/images/github.png" width="10%"></img> <img src="src/images/Adobe_XD_icon.svg.png" width="10%"></img> <img src="./src/images/git.png" width="10%"></img> <img src="./src/images/vscode.png" width="10%"></img>

## Instructions for Installing Check Mate
  - Create an empty directory to house your new project
  - run `virtualenv env` to create a virtual environment within that directory
  - run `source env/bin/activate` to initialize a virtual environment (`deactivate` to exit environment)
  - run `git clone [repository id]`
  - run `cd project`
  - run `pip install -r requirements.txt`

### Seed a Starter Database
  - Run `python manage.py makemigrations`
  - Run `python manage.py migrate`
  - If you want some data to play with, run `python manage.py loaddata db.json`
  - Initialize the project using the command line by typing `python manage.py runserver` in the main directory.
  - Access the application in a browser at `http://localhost:8000`.

### Congratulations! You are now experiencing Check Mate!

  ## Appendix: Planning Documentation

  ### Entity Relationship Diagram
  ![Check Mate ERD](/src/images/Check_Mate_ERD.png)

  ### Wireframes/ Mockups
  <img src="./src/images/Log_In.png" width="45%"></img> <img src="./src/images/View_All_Projects.png" width="45%"></img>
  <img src="./src/images/Project_Board.png" width="45%"></img> <img src="./src/images/Ticket_Details.png" width="45%">
