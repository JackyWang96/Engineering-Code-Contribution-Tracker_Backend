# UniMelb_COMP90082_SP_Backend
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

**Essential Updates on the databse**

1. coordinator table:
The system need a coordinator record to run a series of functions, we suggest to set "admin" as one of the coordinator_name  
2. project_coordinator_relation table:  
Fill each attributes in this table, please pay attention to attribute "coordinator_id", this attribute should be the same as the "id" of coordinator "admin" in coordinator table.  
we potentially consider "git_url" attribute as the frontend repository url of your project.  
Besides, git_token can be acquired from your github account which have access to the "git_url" and "git_backend_url", the tutorial is available on https://catalyst.zoho.com/help/tutorials/githubbot/generate-access-token.html.  
3. user_list table:  
this table may be automatically update once backende server is started, but it will only update data of users who made update on confluence page. developer should add "git_username" to correcponding account. But this attribute can also be edited by frontend project overview page.


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

### Curl Test:

https://confluence.cis.unimelb.edu.au:8443/display/COMP900822021SM2SP/17-2.+Quality+Assurance+and+Testing  

**Configuration** 

`api/v1/sso/login` is for login. The required input is username and password. Run `curl -X POST -d "{""username"":""admin"", ""password"": ""123""}" http://127.0.0.1:8000/api/v1/sso/login` to test it.   

`api/v1/confluence/updateGitUsername` is for setting git_username in user_list table. The required input is user_id and git_username. Run `curl -X POST -d "{""user_id"":""your_user_id"",""git_username"":""your_git_username""}" http://127.0.0.1:8000/api/v1/confluence/updateGitUsername` to test it. 

`api/v1/confluence/updateJiraUsername` is for setting jira_username in user_list table. The required input is user_id and jira_username. Run `curl -X POST -d "{""user_id"":""your_user_id"",""jira_username"":""your_jira_username""}" http://127.0.0.1:8000/api/v1/confluence/updateJiraUsername` to test it. 

`api/v1/confluence/updateJiraUsername` is for setting jira_username in user_list table. The required input is user_id and jira_username. Run `curl -X POST -d "{""user_id"":""your_user_id"",""jira_username"":""your_jira_username""}" http://127.0.0.1:8000/api/v1/confluence/updateJiraUsername` to test it. 


**Github** 

`updateCommits` is for updateCommits. The required input is space_key. Run `curl -X POST -d "{""space_key"":""COMP900822021SM2SP""}" http://127.0.0.1:8000/updateCommits` to test it.   

`getCommits` is for getCommits. The required input is space_key. Run `curl -X POST -d "{""space_key"":""COMP900822021SM2SP""}" http://127.0.0.1:8000/getCommits` to test it.   

`listContribution` is for listContribution. The required input is space_key. Run `curl -X POST -d "{""space_key"":""COMP900822021SM2SP""}" http://127.0.0.1:8000/listContribution` to test it.   

`getLastCommit` is for getLastCommit. The required input is space_key. Run `curl -X POST -d "{""space_key"":""COMP900822021SM2SP""}" http://127.0.0.1:8000/getLastCommit` to test it.   

`api/v1/git/config` is for configurate project accessment. The required input is space_key, jira_url, git_username, git_password, git_token, git_url, git_backend_url. Run `curl -X POST -d "{""space_key"":""COMP900822021SM2SP"",""jira_url"":""https://jira.cis.unimelb.edu.au:8444/projects/COMP900822021SM2SP"",""git_username"":""admin"",""git_password"":""123"",""git_token"":""your_git_token"",""git_url"":""https://github.com/Melb-Uni/SP-Boxjelly_Frontend"",""git_backend_url"":""https://github.com/Melb-Uni/SP-Boxjelly_Backend""}" http://127.0.0.1:8000/api/v1/git/config` to test it.   


**SciTools** 

`getFileMetrics` is for getFileMetrics. The required input is space_key. Run `curl -X POST -d "{""space_key"":""COMP900822021SM2SP""}" http://127.0.0.1:8000/getFileMetrics` to test it.   


**Confluence**  

`api/v1/confluence/<space_key>/meeting_minutes` is for passing all information about meeting minutes on Confluence including title, time, type of meeting and URL. The required input is space key. Run `curl --location --request GET http://127.0.0.1:8000/api/v1/confluence/<space_key>/meeting_minutes` to test it.   

`api/v1/confluence/getNewstConfluence/spaces/<space_key>` is for passing all information related to documentation pages on Confluence including title, person who made lastest change and URL. The required input is space key. Run `curl --location --request GET http://127.0.0.1:8000/api/v1/confluence/getNewstConfluence/spaces/<space_key>` on command to test it.  

`api/v1/confluence/getConfluenceUpdate/spaces/<space_key>` is for passing all information about history of modification on Confluence including title and modification history, and people who have made changes. The required input is space key. Run `curl --location --request GET http://127.0.0.1:8000/api/v1/confluence/getConfluenceUpdate/spaces/<space_key>` on command to test it.  

`api/v1/confluence/getConfluenceLastestUpdate/spaces/<space_key>` is for passing information about the most recent update by team members on Confluence. Run `curl --location --request GET http://127.0.0.1:8000/api/v1/confluence/getConfluenceLastestUpdate/spaces/<space_key>` to test it.  


