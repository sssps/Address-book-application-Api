

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
        """
        This method will return all address details which are present in database
        :param db: database session object
        :return: all the row from database
        """
        items = session.query(models.Address).all()
        if items:
            return items
        else:
            return "Does not retrieve all address Details"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to get all address: {e}")
        logging.error(str(e))

#retrieve a single address.
@app.get("/{id}")
def get_single_address(id:int, session: Session = Depends(get_db)):
    try:
        """
        This method will return single address details based on id
        :param db: database session object
        :param id: serial id of record or Primary Key
        :return: data row if exist else None
        """
        if id:
            item = session.query(models.Address).get(id)
            if item:
                return item
            else:
                raise HTTPException(status_code=404, detail=f"this id details not exist in database")
    except ValueError as e:
        print("Not a proper integer! Try it again")
        logging.ValueError("Value must be an integer")

# add address
@app.post("/add_address")
def add_address(item:schema.Address,  req: Request, session = Depends(get_db)):
    try:
        """
        this method will add a new record to database. and perform the commit and refresh operation to db
        :param db: database session object
        :param address: Object of class schema.Address
        :return: a dictionary object of the record which has inserted
        """
        item = models.Address(address_name = item.address_name, latitude=item.latitude,longitude=item.longitude,)
        if item:
            session.add(item)
            session.commit()
            session.refresh(item)
            return item
        else:
            raise HTTPException(status_code=200, detail=f"address_name {item.address_name} already exist in database: {address_name}")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to add_address: {e}")
        logging.error(str(e))

# update address book
@app.put("/{id}")
def update_address(id:int, item:schema.Address, session = Depends(get_db)):
    try:
        """
        this method will update the database
        :param db: database session object
        :param id: serial id of record or Primary Key
        :param item: Object of class schema.Address
        :return: updated address_book record
        """
        if item:
            itemObject.address_name = item.address_name
            itemObject.latitude = item.latitude
            itemObject.longitude = item.longitude
            session.commit()
        else:
            raise HTTPException(status_code=200, detail=f"No record found to update")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to update_address: {e}")
        logging.error(str(e))

# delte address book
@app.delete("/{id}")
def delete_address(id:int, session = Depends(get_db)):
       
        itemObject = session.query(models.Address).get(id)
        if not itemObject:
              raise HTTPException(status_code=404, detail=f"No record found to delete")
        try:
            """
            This will delete the record from database based on primary key
            :param db: database session object
            :param id: serial id of record or Primary Key
            :return: None
            """
            session.delete(itemObject)
            session.commit()
            session.close()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
            logging.error(str(e))

        return {"delete status": "success"}

#o retrieve the addresses that are within a given distance and location coordinates.
@app.post("/distance")
def distance(distance, latitude, longitude, req: Request,session: Session = Depends(get_db)):
    try:
        """
        API Users should also be able to retrieve the addresses that are within a given distance and
        location coordinates
        :param location_coordinates: store the new coordinate data
        :param distance: get the distance value
        :param latitude: get the latitude value
        :param longitude:get the longitude value
        :param geolocator: geopy is a Python client for several popular geocoding web services.
                           geopy makes it easy for Python developers to locate the coordinates of addresses, cities, countries, and landmarks across the globe using third-party geocoders and other data sources.
        :return: location coorduinates
        """
        location_coordinates = []
        request_args = dict(req.query_params)
        print(request_args)
        distance=request_args['distance']
        latitude=request_args['latitude']
        longitude=request_args['longitude']
        new_lat_long=str(latitude) + ',' + str(longitude)
        if latitude:
            geolocator = Nominatim(user_agent="visa_bridge")
            location = geolocator.reverse(new_lat_long)
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
