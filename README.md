hcrendu
=======

Dead simple application for teachers wanting to collect homework on time.

1. Create a project, add your subject and questions.

2. Invite your students to register, they will receive a secure submission link

3. Your students will be able to upload their answers (text or files) during the timeframe specified in the project

4. Enjoy your freetime and less-crowed e-mail inbox

Licence
-------

This software is open source. Please use it and contribute to
this project. More information is available in the file LICENCE.

Dependencies
------------

This project is written in Python and uses the Django framework.

    pip -r requirements.txt

Installation
------------

### Local

    cd <directory where manage.py lives>

1. Edit the database configuration + the EMAIL_* vars

        $EDITOR settings.py

2. Load the data into the database

        python manage.py syncdb

3. Run the server

        python manage.py runserver 0.0.0.0:8000

4. Create your first project

        http://localhost:8000/admin

5. Add questions

        http://localhost:8000/admin

6. Invite students to register

        http://<public_ip>:8000/

### Remote

Please find a tutorial for a Django setup.

I've been using dotcloud for a few instances of this project and it's working quite well.
You'll find everything you need in the samples/dotcloud directory.


Support
-------

Please open a ticket on our bugtracker : https://github.com/madflo/hcrendu/issues
