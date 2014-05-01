.. _viramp_login_ref:

Login to your VIRAMP instance and start the server
==================================================

At this point you have successfully owned your own version of VIRAMP instance, so what's next?

Start exploring the VIRamp platform
------------------------------------

Open viramp from browser, type in public_IP:8080 (for example, the demo is viramp.com:8080), which public_IP is the IP assigned to your instance, by default the server is open to public via port 8080

.. image:: viramp-doc/viramp-web.png

(optional) Log in to the new instance
--------------------------------------

Alternatively, for experienced users, one can also modify the system based on the the specific requirement.
 
An instruction and overview of the basic steps and parameters you need to login to the instance is provided at the console

.. image:: viramp-doc/connect-info.png

Hit the "Connect" buttom to view information you need for login to the backend of the system

.. image:: viramp-doc/connect.png

Start your terminal and type the following command:

        ``chmod 400 inst-demo.pem``

Connect to your instance using your public IP:

        ``ssh -i inst-demo.pem ubuntu@viramp.com``

Change to the galaxy directory:

        ``cd /mnt/galaxy/galaxy-dist/``

Change viramp settings:

        ``vi universe_wsgi.ini``

Start the viramp server:

        ``sh run.sh``

