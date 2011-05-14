hcrendu
=======

Dead simple application for teachers wanting to collect homework on time.

Licence
-------

This software is open source. Please use it and contribute to
this project. More information is available in the file LICENCE.

Dependencies
------------

This project is written in Python and uses the Django framework.

    pip -r requirements.txt

Local Installation
------------------

    cd <directory where manage.py lives>

# Edit the database configuration

    $EDITOR settings.py

# Load the data into the database

    python manage.py  syncdb

# Run the server

    python manage.py runserver

# Create your first project

    http://localhost:8000/admin


Remote Installation
-------------------

Please find a tutorial for a Django setup.

I've been using dotcloud for a few instances of this project and it's working quite well.
You'll find everything you need in the samples/dotcloud directory.


Support
-------

Please open a ticket on our bugtracker : https://github.com/madflo/hcrendu/issues