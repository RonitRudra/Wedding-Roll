# JANE AND JOE'S WEDDING ALBUM

## This Repo is a Simple Online Wedding Album Project

Features Include:
+ Minimalistic UI
+ User Signup and Login
+ Uploading Images To Gallery
+ Owners (in this case Jane and Joe) Approve Uploads Before They are Visible
+ Like/Unlike an Uploaded Image.
+ Sort Images in Ascending or Descending Order By Number of Likes or Date Posted.
+ 3 User Types: User, Owner and Admin

The Technology Stack I Used:
+ *Python 3*
+ *Django 2.0* as the Application Server
+ *HTML*
+ *CSS*
+ *AJAX*
+ *AWS S3* for serving user uploaded files
+ *PostgreSQL* for the database
+ *Gunicorn* as the Gateway Server
+ *NGINX* as the Web Server/Reverse Proxy
+ Separated Configuration from Source using *Python-Decouple*

The Application is Deployed on a *Digital Ocean* Droplet running Ubuntu 16.04 and available at http://178.128.147.79 (for now)

Followed a *TDD* Approach writing Functional and Unit Tests.


NOTE: Config files under config are not committed to VC
+ config
  + requirements.txt (contains required python modules)
  + development.env (x contains configuration for development)
  + production.env (x contains configuration for production)
  
The *development.env* requires the following keys:
+ AWS_STORAGE_BUCKET_NAME=ronitrudra
+ AWS_S3_REGION_NAME=<SECRET>
+ AWS_ACCESS_KEY_ID=<SECRET>
+ AWS_SECRET_ACCESS_KEY=<SECRET>
+ SECRET_KEY=<SECRET>
+ DEBUG=True
  
The *production.env* requires the following keys:
+ AWS_STORAGE_BUCKET_NAME=ronitrudra
+ AWS_S3_REGION_NAME=<SECRET>
+ AWS_ACCESS_KEY_ID=<SECRET>
+ AWS_SECRET_ACCESS_KEY=<SECRET>
+ SECRET_KEY=<SECRET>
+ DEBUG=False
+ ALLOWED_HOSTS=178.128.147.79,
+ DB_ENGINE=django.db.backends.postgresql_psycopg2
+ DB_NAME=<SECRET>
+ DB_USER=<SECRET>
+ DB_PASSWORD=<SECRET>
+ DB_HOST=<SECRET>
+ DB_PORT=5432
  
Also note that *manage.py* uses the development setting as default while *wsgi.py* uses production setting.
