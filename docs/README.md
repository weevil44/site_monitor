This is an application written in Python that monitors the performance of web sites and alerts when sites are down or degraded beyond a certain threshold.  It generates a status.html page under the site_monitor directory.  It can be used for rudimentary monitoring of your web applications to receive email alerts when they are experiencing issues. If you have a Linux VM, you can set it up to execute via cron.  If you want to run via a container, there is a 

To use:
1. Clone the repo
1. Edit the urllist.txt file with the URLs of the sites you would like monitored
1. Edit the App Config section of the site_monitor.py script with values for your environment
1. To setup execution of the script directly on your PC or server.  On Linux, copy the sitemonitor file to /etc/cron.d and edit it for your environment.  On Windows, add a task to the Task Scheduler to automate the execution of the script
1. To run in a container:
    1. Build a Docker image using the Dockerfile
        ````
        Powershell: Get-Content Dockerfile | docker build --tag python-site:0.0.1 .
        Linux command line: docker build -t python-site:0.0.1
        ````
    1. Push the image to your container registry to ensure you have an external copy, you will need to authenticate to the registry before pushing or pulling.  You should tag the new image as latest and with a version number so different versions can be used in different environments and you will have the ability to revert back to an old version if necessary.<br>
        ````
        docker tag python-site:0.0.1 myregistry.azurecr.io/samples/python-site:latest<br>
        docker tag python-site:0.0.1 myregistry.azurecr.io/samples/python-site:0.0.1<br>
        docker push --all-tags myregistry.azurecr.io/samples/python-site:0.0.1<br>
        ````
    1. Pull the image from the registry, this will pull the latest version since we are not specifying<br>
        ````
        docker pull myregistry.azureacr.io/python-site
        ````
    1. Run the container
        ````
        docker run --name site-monitor -v C:\Users\weevi\Documents\code\python\site_monitor\src:/usr/app/src/src -it python-site:0.0.1 python site_monitor.py -d ./
        ````

To enable the status page to be accessible in a browser when using Apache web server, a symbolic link needs to be added under /app/apache/www/html (or wherever your web root has been configured on your system).


