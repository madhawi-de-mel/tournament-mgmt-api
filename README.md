**Tournament Management System API**

- Python version - 3.8
- Requirements are added to *requirements.txt* file

Execute the following command to run the system 

`python manage.py runserver`

Dummy data and sample users are created in system startup. Following dummy users are created.

| group | user | psw |
| ------ | ------ | ------ |
| admin | admin | admin123 |
| admin | super_user | super123 |
| coach | john | john123 |
| player | andrew | andrew123 |
  
         
A super user is created to view group and user information (as an admin)

Assumptions and concerns: 

- Tournament has ended. 
- System is only used to view the data.
- Hence team average, user average is calculated in system startup. 
- If the system is reused for adding new data, then the average score calculation must be triggered.
- Average team scores are only visible depending on user groups. That is, only admins can view all team average scores. Both coaches and players can only view team average of their own team.
