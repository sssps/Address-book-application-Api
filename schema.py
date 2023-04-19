from typing import Optional
from pydantic import BaseModel


class AddressBase(BaseModel):
	address_name:str
	latitude:float
	longitude:float


class Address(AddressBase):
	
	# Behaviour of pydantic can be controlled via the Config class on a model
	# to support models that map to ORM objects. Config property orm_mode must be set to True
	class Config:
	    orm_mode = True