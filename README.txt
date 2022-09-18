Project title: Lecture Attendance Management System
Supervisor: Richard Lawlor
Student Name: Yuanpei Teng
Student Number: D18124423
Course: TU856/4

Project running environment setup instructions

This project is a local project, therefore in order to run this project, several softwares need to be pre-installed on the laptop:

1. Install Anaconda, Redis, MySql Database, Navicat, Pycharm, VS Code, Python, Node.js
2. After installation these required softwares, we are now going to install the required libraries and plugins
	Step 1: Import the "fyp_environment.yaml" file to the anaconda, this is the environment file extracted from my own laptop, it will save a lot of time for you
		to install all required libraries one by one.
	Step 2: If the import file report some errors or failed during the installation, that is very normal, so please follow the following steps:
		Step 2.1: Now import "fyp_dependencies.yaml" file to the anaconda, this file will only used to install the dependencies on the anaconda environment.
		Step 2.2: Now if previous step success, open the cmd window as admin and run this line of commands below to install pip:
			conda activate online_face36      /* this is the virtual environment name in your anaconda, if different, change it*/
			pip install -r fyp_pip.txt
		* if any errors occur, such as no such moudule, or required a higher version, etc. 
			pip install the_error_modulename == version  /* the_error_modulename is the module you want to install, version is the version number you want to intall*/
	
	Step 3: Install vue cli using the command:      npm install -g @vue/cli

	Step 4: In my fyp project folder that I submitted, open the "online_face_recognition"folder in Pycharm, this is the backend of my project
	Step 5: Set the anaconda vitural environment that you just installed as interperter of the "start.py" file
	Step 6: In the "Config.py" file, change the "username", password, host, port and database varibale to meet your computer
	Step 7: The database for this project should be pre build, therefore, create a sql database called "student" through Navicat
	Step 8: Open Redis server
	Step 9: Run start.py   /* if install successful, you should see a localhost port 5000 is opened
	Step 10: open "front-end"folder in VS Code, this folder is the front-end of my project
	Step 11: Open terminal in VS Code, run command:   npm install    
	Step 12: If no error, then run command:  npm run serve           /* that will run the front-end server for you locally*/
	Step 13: In VS Code, Check the port number in the terminal 
	Step 14: if the port number is 8081, then no need to change, you can directly run the code using chrome with localhost:8081
	Step 15: if the port number is not 8081, change the port number to 8081, otherwise, there will be lots of configuration in both 'front-end' 
		and "online_face_recognition"folder need to reset. Tips: use find method, to search all set relate to port 8081, change them to your port. 
