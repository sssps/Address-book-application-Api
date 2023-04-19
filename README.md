Assignment:
=============
 Create an address book application where API users can create, update and deleteaddresses.

The address should:
     - contain the coordinates of the address.
     - be saved to an SQLite database.
     - be validated

API Users should also be able to retrieve the addresses that are within a given distance and
location coordinates.


First of all create virtual environment :
======================================
install:
========
   - pip install virtualenv
   - virtualenv <virtual_env_name>

   To activate virtual environment using windows command prompt 
   change directory to your virtual env :
   ===================================
     $ cd <envname>
     $ Scripts\activate 

Then after install all packgae:
=================================
   - pip install -r requirement.txt


after install all package run the python program:
================================================
  - create db and create table run the python file:
     ==> python app.py


Typer is FastAPI's little sibling. And it's intended to be the FastAPI of CLI install:
===================================================================================
    --You will also need an ASGI server, for production such as Uvicorn
    -- pip install uvicorn

     Run the Fast API server with:
     ======================

         ==> uvicorn app:app --reload

         ==> http://127.0.0.1:8000/docs
