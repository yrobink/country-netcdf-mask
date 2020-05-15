# -*- coding: utf-8 -*-

## Copyright(c) 2020 Yoann Robin
## 
## This file is part of country-netcdf-mask
## 
## country-netcdf-mask is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## country-netcdf-mask is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with country-netcdf-mask.  If not, see <https://www.gnu.org/licenses/>.

###############
## Libraries ##
##{{{

import sys,os
import urllib.request as urlreq
import zipfile
import random
import string
import itertools as itt
import datetime as dt

## Scientific libraries
##=====================

import numpy as np
import geopandas as gpd
import xarray as xr
from shapely.geometry import Point

##}}}
###############

###############
## Fonctions ##
###############

def load_naturalearth( ne_file = "data/ne_10m_admin_0_countries.zip" , url_data = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip" ):##{{{
	if not os.path.isfile(ne_file):
		file_data = urlreq.urlopen( url_data )
		data_to_write = file_data.read()
		
		with open( ne_file , "wb" ) as f:
			f.write(data_to_write)
	
	return ne_file
##}}}


#############
## Classes ##
#############

class TemporaryFolder:##{{{
	def __init__( self , base ):
		tmp_dir = os.path.join( base , "tmp" )
		while os.path.isdir(tmp_dir):
			tmp_dir = os.path.join( base , "tmp" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) )
		os.mkdir(tmp_dir)
		self.dir = tmp_dir
	
	def clean( self ):
		for f in os.listdir(self.dir):
			os.remove( os.path.join( self.dir , f ) )
		os.rmdir(self.dir)
##}}}


##########
## main ##
##########

if __name__ == "__main__":
	
	## Define your parameters here
	##============================
	name_country = "France"  ## In English
	lonlatbox = -5,10,40,52  ## Lon/lat box
	dlon,dlat = 0.05,0.05    ## Resolution
	
#	name_country = "Italy"
#	lonlatbox = 5.5,20,36,48
#	dlon,dlat = 0.05,0.05
	
#	name_country = "Spain"
#	lonlatbox = -10,5,35,45
#	dlon,dlat = 0.05,0.05
	
#	name_country = "Germany"
#	lonlatbox = 5,16,47,55.5
#	dlon,dlat = 0.05,0.05
	
	
	## path input/output
	pathIO = os.path.join( os.path.dirname( os.path.abspath(__file__) ) , "data" )
	
	## Temporary folder
	##=================
	tmp = TemporaryFolder(pathIO)
	
	## Load shape file, extract, and read it
	##======================================
	ne_file = load_naturalearth()
	zfile   = zipfile.ZipFile(ne_file)
	zfile.extractall( tmp.dir )
	for f in os.listdir(tmp.dir):
		if f.split(".")[-1] == "shp":
			data = gpd.read_file(os.path.join(tmp.dir,f))
	
	
	## Select country
	##===============
	country = data[ data["NAME_EN"] == name_country ]
	
	## Define lat/lon box
	##===================
	min_lon,max_lon,min_lat,max_lat = lonlatbox
	lon = np.arange( min_lon , max_lon + dlon / 2 , dlon )
	lat = np.arange( min_lat , max_lat + dlat / 2 , dlat )
	
	lons,lats = np.meshgrid( lon , lat )
	
	lats = xr.DataArray( lats , dims = ["y","x"] )
	lons = xr.DataArray( lons , dims = ["y","x"] )
	
	
	## Define xarray mask
	##===================
	xrdims = ["time","y","x"]
	xrcoords = { "time" : [0] , "lon" : lons , "lat" : lats }
	mask = xr.DataArray( np.zeros((1,)+lons.shape) , dims = xrdims , coords = xrcoords )
	
	## Loop on lon lat to test if in country
	##======================================
	nx,ny = lons.shape
	for iy,ix in itt.product(range(nx),range(ny)):
		p           = Point( lons[iy,ix] , lats[iy,ix] )
		mask[0,iy,ix] = country.contains(p).values[0]
	
	## Final netcdf file
	##==================
	mask = xr.Dataset( {"mask":mask} )
	
	mask.attrs["title"] = "{} mask on the regulard grid [{},{}]x[{},{}] by {}x{} degrees".format(name_country,min_lon,max_lon,min_lat,max_lat,dlon,dlat)
	mask.attrs["Conventions"] = "CF-1.0"
	
	mask.mask.attrs["long_name"] = "{} mask on the regulard grid [{},{}]x[{},{}] by {}x{} degrees".format(name_country,min_lon,max_lon,min_lat,max_lat,dlon,dlat)
	mask.mask.attrs["units"]     = 1
	
	mask.time.attrs["units"]         = "day since {}".format(dt.datetime(1900,1,1))
	mask.time.attrs["axis"]          = "T"
	mask.time.attrs["long_name"]     = "time"
	mask.time.attrs["standard_name"] = "time"
	mask.time.attrs["calendar"]      = "gregorian"
	
	mask.lat.attrs["axis"]           = "y"
	mask.lat.attrs["long_name"]      = "Latitude"
	mask.lat.attrs["standard_name"]  = "latitude"
	mask.lat.attrs["units"]          = "degrees_north"
	
	mask.lon.attrs["axis"]           = "x"
	mask.lon.attrs["long_name"]      = "Longitude"
	mask.lon.attrs["standard_name"]  = "longitude"
	mask.lon.attrs["units"]          = "degrees_east"
	
	mask.to_netcdf( os.path.join( pathIO , "mask_{}_{}x{}.nc".format(name_country,dlon,dlat) ) )
	
	
	## Remove temporary
	##=================
	tmp.clean()
	
	print("Done")
