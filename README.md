# Sql Runner
App to execute sql scripts against multiple databases.
Currently only supporting Microsoft Sql Server.

# Environment Setup

This app is based on the pinax-account application http://pinaxproject.com/pinax/starter_project_list/#pinax-project-account

It requires Python 3.5.2 and the following python packages:
- cick==5.1
- colorama==0.3.3
- django==1.9.8
- django-appconf==1.0.2
- django-bootstrap-form==3.2.1
- django-user-accounts==1.3.1
- jsonfield==2.0.2
- pinax-cli==1.0.0
- pinax-eventlog==1.1.2
- pinax-theme-bootstrap==7.10.1
- pinax-webanalytics==2.0.4
- pkg-resources==0.0.0
- pymssql==2.1.1
- pyodbc==4.0.17
- pytz==2017.2
- requests==2.7.0

pymssql to function requires FreeTDS to be installed. At the moment of creation of this app there were compatibility problems between FreeTDS and the latest version of pymssql that's why pymssql 2.1.1 was used instead. (https://stackoverflow.com/questions/39187089/tdsversion-keeps-defaulting-to-7-1-pymssql)
