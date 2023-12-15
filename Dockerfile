# escape=`

#Get the latest base image
FROM python:latest

#Labels as key value pair
LABEL Maintainer="weevil44"

# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app

#to COPY the remote file at working directory in container
COPY site_monitor.py /usr/app
# The script will now located at '/usr/app/src/web_monitor.py' when a Docker container is spun up from this image

#ENTRYPOINT is used to execute the script in Python on the container using the argument passed at run time '-d .'
ENTRYPOINT [ "python", "site_monitor.py" ]