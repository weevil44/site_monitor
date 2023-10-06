This is an application written in Python that monitors the performance of web sites and alerts when sites are down or degraded beyond a certain threshold.  It generates a status.html page under the site_monitor directory.  It can be used for rudimentary monitoring of your applications to receive email alerts when they are experiencing issues.

To use:
1. Clone the repo
1. Edit the urllist.txt file with the URLs of the sites you would like monitored
1. Edit the App Config section of the site_monitor.py script with values for youe environment
1. On linux, copy the sitemonitor file to /etc/cron.d and edit it for your environment.  On Windows, add a task to the Task Scheduler to automate the execution of the script 

To enable the status page to be accessible in a browser when using Apache web server, a symbolic link needs to be added under /app/apache/www/html (or wherever your web root has been configured on your system).


