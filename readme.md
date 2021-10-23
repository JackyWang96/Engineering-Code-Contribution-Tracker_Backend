# unimelb-COMP90082-SP-Backend
This is the backend for COMP90082 SP project.
It provides REST apis for students activities data on Confluence, Jira, and Git.


## Deploy methods

**require python3.7 or higher and MySQL**

1. Install all packages needed `pip install -r requirements.txt` (if python2 and python3 are both installed, use pip3 and python3)
2. start MySQL server on localhost:3306, and create a database named "sp90013" `CREATE DATABASE sp90013`
3. modify the MySQL username and password config in TeamSPBackend/Settings/dev.py and TeamSPBackend/Settings/prod.py (don't forget to modify 'DATABASES/default/TEST/PASSWORD' in prod.py)
4. create MySQL tables `python manage.py migrate`
5. start server `python manage.py runserver`
6. api web server is now running on: http://127.0.0.1:8000/api/v1


### Structuring files

To create new APIs or extend existing ones, kindly put the API endpoints (URLs) in "TeamSPBackend/api/urls_vX.py" (for version X) with their corresponding API functions. Kindly refer to "TeamSPBackend/api/urls_v1.py" for more info.

The functions called by the API endpoints are created and reside in "TeamSPBackend/api/views". For example, the functions related to any Team APIs reside in "TeamSpBackendd/api/views/team.py". The functions for Confluence and JIRA APIs reside in their own sub-folders ("TeamSPBackend/api/views/confluence" & "TeamSPBackend/api/views/jira") as they are comprised of multiple files.

The database models for the objects used in our APIs are written as modules of their own in "TeamSPBackend".

To create new models and/or APIs utilizing them, kindly follow the current directory structure and format:

- Database models in its own module. E.g. "TeamSPBackend/newModel/" containing the files "app.py" and "models.py"
- Functions for new APIs under "TeamSPBackend/api/views/". E.g. "TeamSPBackend/api/views/newModel.py"
- API endpoints (URLs) in "TeamSPBackend/api/urls_vX.py" for version X
- For any API functions that require multiple files, put those files under a sub-folder in "TeamSPBackend/api/views/". E.g. "TeamSPBackend/api/views/newModel/"

## System while runtime

### MySQL Database Update:

Some of functions will be called to update the database everytime running the backend server with `python manage.py runserver`. It is because these functions are scheduled in views.py (E.g. "TeamSPBackend/confluence/views.py"). The database should be updated successfully when there is no new log on the terminal. 

### APIs Usage:

The frontend can fetch data via RESTful APIs once the database is successfully updated. The usage of APIs related to different platforms will be briefly introduced below (More details on https://confluence.cis.unimelb.edu.au:8443/display/COMP900822021SM2SP/11.+API+Documents). 

**Confluence**
`api/v1/confluence/<space_key>/meeting_minutes` is for passing all information about meeting minutes on Confluence including title, time, type of meeting and URL. The required input is space key.
`api/v1/confluence/getNewstConfluence/spaces/<space_key>` is for passing all information related to documentation pages on Confluence including title, person who made lastest change and URL. The required input is space key.
`api/v1/confluence/getConfluenceUpdate/spaces/<space_key>` is for passing all information about history of modification on Confluence including title and modification history, and people who have made changes. The required input is space key.
`api/v1/confluence/getConfluenceLastestUpdate/spaces/<space_key>` is for passing information about the most recent update on Confluence. 
