
# Blog_App_and_Api-Django


## Set Up

### Install Pip
	sudo apt-get install python-pip

### Clone library repository
	https://github.com/Neerajsinghtanwar/Blog_App_and_Api-Django.git

### Install Requirements
	pip install -r requirements.txt

### Set Up MySQL
	sudo apt-get install libmysqlclient-dev
	sudo apt-get install mysql-server
	mysql -u root -p --execute "create database blog; grant all on blog.* to root@localhost identified by 'Asdf@1234';"

### Set Database (Make Sure you are in directory same as manage.py)
    python manage.py makemigrations
    python manage.py migrate

### Run Server
	python3 manage.py runserver
	open localhost:8000 in your browser

### Authors
- [Neerajsinghtanwar](https://github.com/Neerajsinghtanwar/Blog_App_and_Api-Django.git)

  