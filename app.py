
#  ------------------------------------------------------------------------------------------------
# This is an API. which are having four end points to perform the CRUD operation with SQLite
#  ------------------------------------------------------------------------------------------------
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from fastapi import Request
# from typing import Any, Dict, List, Union
import models
import schema
from db_handler import SessionLocal, engine

import logging

logging.basicConfig(filename='logger.txt', 
    format='%(asctime)s %(levelname)s-%(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

models.Base.metadata.create_all(bind=engine)

# initiating app
app = FastAPI(
    title="Addres Details",
    description="You can perform CRUD operation by using this API",
    version="1.0.0"
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#retrieve all address
@app.get("/")
def get_alladdress(session: Session = Depends(get_db)):
    try:
        items = session.query(models.Address).all()
        return items
    except Exception as e:
        str(e)
        logging.error(str(e))

#retrieve a single address.
@app.get("/{id}")
def get_single_address(id:int, session: Session = Depends(get_db)):
    try:
        item = session.query(models.Address).get(id)
        return item
    except Exception as e:
        str(e)
        logging.error(str(e))

# add address
@app.post("/add_address")
def add_address(item:schema.Address, session = Depends(get_db)):
    try:
        item = models.Address(address_name = item.address_name, latitude=item.latitude,longitude=item.longitude,)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except Exception as e:
        str(e)
        logging.error(str(e))

# update address book
@app.put("/{id}")
def update_address(id:int, item:schema.Address, session = Depends(get_db)):
    try:
        itemObject.address_name = item.address_name
        itemObject.latitude = item.latitude
        itemObject.longitude = item.longitude
        session.commit()
        return 'Address update successfully!'
    except Exception as e:
        str(e)
        logging.error(str(e))

# delte address book
@app.delete("/{id}")
def delete_address(id:int, session = Depends(get_db)):
    try:
        itemObject = session.query(models.Address).get(id)
        session.delete(itemObject)
        session.commit()
        session.close()
        return 'Address was deleted'
    except Exception as e:
        str(e)
        logging.error(str(e))

#o retrieve the addresses that are within a given distance and location coordinates.
@app.post("/distance")
def distance(distance, location, req: Request,session: Session = Depends(get_db)):
    try:
        import pdb;pdb.set_trace();
        location_coordinates = []
        request_args = dict(req.query_params)
        print(request_args)
        distance=request_args['distance']
        location=request_args['location']
        if location:
            geolocator = Nominatim(user_agent="visa_bridge")
            location = geolocator.geocode(location)
            print(location)
            if location.latitude and location.longitude:
               filter_coordinates = (location.latitude, location.longitude)
               items = session.query(models.Address).all()
               for address in items:
                    if address.latitude and address.longitude:
                        job_coordinates = (address.latitude, address.longitude)
                        find_distance = geodesic(filter_coordinates, job_coordinates).miles
                        if find_distance <= int(distance):
                             location_coordinates.append(address.address_name)


        if location_coordinates:
            return location_coordinates
    except Exception as e:
        return location_coordinates
        logging.error(str(location_coordinates))