**Tournament Management System API**

- Python version - 3.8
- Requirements are added to *requirements.txt* file

Execute the following command to run the system 

`python manage.py runserver`

Django Authentication System is used to manage users, groups and permissions

Dummy data and sample users are created in system startup (No extra commands are required). Following dummy users are created.

| group | user | psw |
| ------ | ------ | ------ |
| admin | admin | admin123 |
| admin | super_user | super123 |
| coach | john | john123 |
| player | andrew | andrew123 |
  
         
A super user is created to view group and user information/permission through Django Admin Dashboard (http://127.0.0.1:8000/admin/)

**Endpoints**

[http://127.0.0.1:8000/management_app/rounds/](http://127.0.0.1:8000/management_app/rounds/)
- Return all round, match details
- Permitted groups: all groups, but login required

[http://127.0.0.1:8000/management_app/teams/](http://127.0.0.1:8000/management_app/teams/)
- Return all teams with public details
- Permitted groups: all groups, but login required

[http://127.0.0.1:8000/management_app/teams/1](http://127.0.0.1:8000/management_app/teams/1)
- Return the specific team with details such as average score
- Permitted groups: admin can view any group. Coach and player can view only their team 

[http://127.0.0.1:8000/management_app/best-players/](http://127.0.0.1:8000/management_app/best-players/)
- Return the best players of the team, that is players in 90th percentile of the team. Sorted such that player with highest average score is first
- Permitted groups: Coach can view his team. Player has no access 
- Permitted groups: Admin have to send a request parameter specifying the team-id. Admin can view any team when team-id is given. [http://127.0.0.1:8000/management_app/best-players/?team-id=1](http://127.0.0.1:8000/management_app/best-players/?team-id=1)

[http://127.0.0.1:8000/management_app/players/](http://127.0.0.1:8000/management_app/players/)
- Return player details (name, height, average score, number of matches played)
- Permitted groups: admin can view all players. Coach can view all players of the his team, Player can view himself.

[http://127.0.0.1:8000/management_app/coaches/](http://127.0.0.1:8000/management_app/coaches/)
- Return coach details (name, experience)
- Permitted groups: only admin can view

[http://127.0.0.1:8000/management_app/coaches/1/](http://127.0.0.1:8000/management_app/coaches/1/)
- Return coach details of the specific details (name, experience)
- Permitted groups: only admin can view

[http://127.0.0.1:8000/management_app/statistics/](http://127.0.0.1:8000/management_app/statistics/)
- Return site usage statistics (user login count, time spent in site, login status)
- Permitted groups: only admin can view


**Assumptions and concerns**

- Tournament has ended. 
- System is only used to view the data.
- Hence team average, user average is calculated in system startup. 
- If the system is reused for adding new data, then the average score calculation must be triggered.
- Average team scores are only visible depending on user groups. That is, only admins can view all team average scores. Both coaches and players can only view team average of their own team.
- Authenticated system user has to be explicitly mapped to a player or coach in the system. This is done for dummy users in startup
