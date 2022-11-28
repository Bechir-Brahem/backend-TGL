steps to setup prod http server  
```bash
open port 80 
sudo su

# DJANGO
git clone https://github.com/Bechir-Brahem/backend-TGL
install pipenv
cd backend-TGL
# switch to the virtual environment
pipenv shell
pipenv install
# copy the .env file
python manage.py migrate
python manage.py createsuperuser
# [OPTIONAL] {
# test server files
python manage.py runserver 0.0.0.0:80
# }

# GUNICORN
sudo mkdir -pv /var/{log,run}/gunicorn/
gunicorn -c gunicorn-conf.py
# [OPTIONAL]
tail -f /var/log/gunicorn/dev.log

# NGINX
apt install nginx
systemctl start nginx
systemctl status nginx
# [OPTIONAL] {
# check nginx server on your domain.name
# it should return nginx home page (not your django app)
# }

# replace the server_name in nginx.conf/azure with your domain
# replace /static alias to your path to prod-static
# rename the nginx.conf/azure to nginx.conf/your-domain-name
cp nginx.conf/azure /etc/nginx/sites-available/
# [OPTIONAL]
sudo service nginx configtest /etc/nginx/sites-available/azure
cd /etc/nginx/sites-enabled
ln -s ../sites-available/azure .

cd /home/bb/backend-TGL
python manage.py collectstatic
# rm -r static , mv prod-static static
systemctl restart nginx
# http server with static files should be running



```
## references
https://realpython.com/django-nginx-gunicorn/
