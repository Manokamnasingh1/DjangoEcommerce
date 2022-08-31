# DjangoEcommerce
https://mycart1.herokuapp.com/
Quick Start
Fork and Clone the repository using-
git clone https://github.com/Manokamnasingh1/DjangoEcommerce.git
Create a Branch-
git checkout -b <branch_name>
Create virtual environment-
python -m venv env
env\Scripts\activate
Install dependencies using-
pip install -r requirements.txt
If you have python2 and python3 installed you need to specify python3 by using command:

python3 -m pip install -r requirements.txt
Headover to Project Directory-
cd ecom
Make migrations using-
python manage.py makemigrations
If you have python2 and python3 installed you need to specify python3 by using command:

python3 manage.py makemigrations
Migrate Database-
python manage.py migrate
Create a superuser-
python manage.py createsuperuser
Run server using-
python manage.py runserver
