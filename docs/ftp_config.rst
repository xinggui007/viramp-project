FTP configuration for large dataset uploading
==============================================

Galaxy's generic uploading function cannot handle files larger than 2GB properly.  Use FTP to upload data instead. ProFTPd has been preinstalled in the instance, and most of the configuration is already done, but users still may need to log in to the instance for some change.

* Log in to the instance with instructions showing in the :ref:`previous page <viramp_login_ref>`.

* Change to galaxy home directory 
	``cd /mnt/galaxy/galaxy-dist``

* Edit the config file (`universe_wsgi.ini`), change the `ftp_upload_site` parameter to the IP address of the instance.  

* The FTP configuration file is located at `/usr/local/etc`. In general, it has been configed to fit in the system.  Only experienced users may want to modify for further adjustment

For more information about general ftp configuration on Galaxy, please visit the `Galaxy wiki <https://wiki.galaxyproject.org/Admin/Config/UploadviaFTP>`_ 
