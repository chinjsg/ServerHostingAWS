# Server Hosting (AWS)

Cloud Computing Project  
Demo Link: https://youtu.be/adp6Ay_Jh6U  

### Files:
 * api
 * create_server
 * terminate_server
 * main
 * monitor_node
 * process
 * database_adapter.py
 * server.jar
 * bashrc

### Notes:
- A server.jar, version 1.17.1, file is included to be manually transferred via SCP to each newly created instance rather than to download it directly from the Minecraft website. This is intentionally done so because a major Minecraft 1.18 update is set to be released on November 30, 2021, and this is to avoid any potential compatibility issues with the Java version that is being used.  
- bashrc is a configuration file which replaces .bashrc in /home/ec2-user of the newly created instance. This includes path names for the Java installation.  
- In my main instance, server.jar and bashrc is placed in /home/ec2-user. Everything else is placed in the /cgi-bin directory.

### Webpage Example URL:  
http://<ip_address>/cgi-bin/main

### Description of files:  
[api]  
This script handles the REST api and displays information of all records of created instances in JSON format. If the server is ready to be used, the
public IP address will be displayed, otherwise, it will appear blank.  
Supports:
/cgi-bin/servers
/cgi-bin/servers/<id>

[create_server]  
This script handles the creation of a new instance and inserts a new record with the instance information into the database. Another script, monitor_node, is triggered
in the background. When used with either curl or the web browser, the user will quickly be redirected /cgi-bin/servers/<id_assigned> where they will be able to view
the information of their instance.

[terminate_server]  
This scripts handles the termination of a running instances and removes it from the database

[main]  
This script is responsible for generating the front-end website which the user interacts which. Cookie sessions are used for log ins and last 10 minutes per session.
When expired, the user simply needs to re-log in with the same username and the expiry will be refreshed. Provides functionality to log in, view all served owned by
the user, view an individual server information in more detail, creation, and termination of a server. Relies on api/servers to retrieve server information.

[monitor_node]  
This script is called by create_server which takes in an instanceID to monitor. It will also perform the Java installation and configurations of the Minecraft server
on the newly created instance. It then starts the Minecraft server, and repeatedly check if the server is up and running. Once the server is ready, the script will
update the ready column for that instance record on the database.

[process]  
This scripts handles creation/setting of cookie headers. It will create each cookie which expires in 10 minutes. The expiry is refreshed when the user logs in with an
existing session that has expired.

[database_adapter.py]  
This script handles all database interactions across the other scripts. You will need to create a passwords file called dbinfo which includes your credentials to access
the RDS instance.

[server.jar] (Note: omitted from repository)  
This a file to be transferred into the new instance through monitor_node script.

[bashrc]  
This a file to be transferred into the new instance through monitor_node script.
