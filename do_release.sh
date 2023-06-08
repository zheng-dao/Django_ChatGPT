#!/bin/bash
git stash
git pull origin master
sudo chmod +x do_release.sh
act
python manage.py makemigrations app
python manage.py migrate app
echo "Have you uploaded the scripts to the S3 bucket?"
read myvar
echo "Have you invalidated the js files in AWS CloudFront?"
read myvar
echo "Have you updated the Version api to a new version?"
read myvar
sudo service apache2 restart
sudo chmod +x flush_cache.sh
sudo ./flush_cache.sh
echo "make sure to run python manage.py collectstatic"