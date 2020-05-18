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

def load_naturalearth( path , url_data = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip" ):##{{{
	ne_file = os.path.join( path , "ne_10m_admin_0_countries.zip" )
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
		tmp_dir = os.path.join( base , "country_ncdf" )
		while os.path.isdir(tmp_dir):
			tmp_dir = os.path.join( base , "country_ncdf" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)) )
		os.mkdir(tmp_dir)
		self.dir = tmp_dir
	
	def clean( self ):
		for f in os.listdir(self.dir):
			os.remove( os.path.join( self.dir , f ) )
		os.rmdir(self.dir)
##}}}


################
## Old script ##
##{{{

#	## Define your parameters here
#	##============================
#	name_country = "France"  ## In English
#	lonlatbox = -5,10,40,52  ## Lon/lat box
#	dlon,dlat = 0.5,0.5    ## Resolution
#	
#	name_country = "Italy"
#	lonlatbox = 5.5,20,36,48
#	dlon,dlat = 0.05,0.05
	
#	name_country = "Spain"
#	lonlatbox = -10,5,35,45
#	dlon,dlat = 0.05,0.05
	
#	name_country = "Germany"
#	lonlatbox = 5,16,47,55.5
#	dlon,dlat = 0.05,0.05

##}}}
################



##########
## main ##
##########

def main_function( argv ):
	
	## Global args
	##============
	ckwargs = { "--nedata"    : "none" ,
	            "--tmp"       : "none" ,
	            "--country"   : "none" ,
	            "--lonlatbox" : "none" ,
	            "--dlonlat"   : "none" ,
	            "--figure"    : False  ,
	            "--list"      : False  ,
	            "--output"    : "none"
	            }
	shortcut = { "-ne" : "--nedata"    ,
	             "-t"  : "--tmp"       ,
	             "-c"  : "--country"   ,
	             "-b"  : "--lonlatbox" ,
	             "-d"  : "--dlonlat"   ,
	             "-p"  : "--figure"    ,
	             "-l"  : "--list"      ,
	             "-o"  : "--output"
	            }
	
	
	## Read argv
	##==========
	if len(argv) == 1:
		return "Error: No arguments given, abort"
	
	for i in range(1,len(argv)):
		if "=" in argv[i]:
			arg,value = argv[i].split("=")
			if ckwargs.get(arg)  is not None: ckwargs[arg] = value
			if shortcut.get(arg) is not None: ckwargs[shortcut[arg]] = value
		else:
			if argv[i] in ["--figure","-p"]: ckwargs["--figure"] = True
			if argv[i] in ["--list"  ,"-l"]: ckwargs["--list"]   = True
	
	if ckwargs["--country"] == "none" and not ckwargs["--list"]:
		return "Warning: Country not set and list not asked, abort"
	
	if not ckwargs["--list"]:
		if ckwargs["--dlonlat"] == "none":
			return "Warning, dlonlat not set"
		try:
			dlonlat = float(ckwargs["--dlonlat"])
			dlonlat = [dlonlat,dlonlat]
		except:
			try: dlonlat = [float(x) for x in ckwargs["--dlonlat"].split(",")]
			except: return "Error, dlonlat malformed"
	
	box = ckwargs["--lonlatbox"]
	if not box == "none":
		try:
			box = [ float(x) for x in ckwargs["--lonlatbox"].split(",") ]
			assert(len(box) == 4)
		except:
			return "Error: lonlatbox malformed"
	
	pathOut = ckwargs["--output"]
	if not os.path.isdir(pathOut): pathOut = "."
	
	
	## Prepare temporary folder
	##=========================
	if os.path.isdir(ckwargs["--tmp"]): tmp = TemporaryFolder(ckwargs["--tmp"])
	elif os.path.isdir("/tmp"): tmp = TemporaryFolder("/tmp/")
	else: return "Error: No temporary folder available, abort"
	
	
	## Open natural earth data
	##========================
	nefile = ckwargs["--nedata"]
	if os.path.basename(nefile) == "ne_10m_admin_0_countries.zip" and os.path.isfile(nefile):
		pass
	elif os.path.isdir(nefile):
		nefile = load_naturalearth( nefile )
	else: nefile = load_naturalearth( tmp.dir )
	
	zfile   = zipfile.ZipFile(nefile)
	zfile.extractall( tmp.dir )
	for f in os.listdir(tmp.dir):
		if f.split(".")[-1] == "shp":
			data = gpd.read_file(os.path.join(tmp.dir,f))
	
	
	## Countries list
	##===============
	clist = data["NAME_EN"].values.tolist()
	clist.sort()
	
	
	## First output type: list countries
	##==================================
	if ckwargs["--list"]:
		tmp.clean()
		return "".join([ c + "\n" for c in clist])
	
	
	## Check country
	##==============
	ncountry = ckwargs["--country"]
	if not ncountry in clist:
		return "Error: country not find"
	country = data[ data["NAME_EN"] == ncountry ]
	if box is "none":
		box = country["geometry"].bounds.values.squeeze()
		box[1],box[2] = box[2],box[1]
	
	
	## Define lat/lon box
	##===================
	min_lon,max_lon,min_lat,max_lat = box
	dlon,dlat = dlonlat
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
	
	mask.attrs["title"] = "{} mask on the regulard grid [{},{}]x[{},{}] by {}x{} degrees".format(ncountry,min_lon,max_lon,min_lat,max_lat,dlon,dlat)
	mask.attrs["Conventions"] = "CF-1.0"
	
	mask.mask.attrs["long_name"] = "{} mask on the regulard grid [{},{}]x[{},{}] by {}x{} degrees".format(ncountry,min_lon,max_lon,min_lat,max_lat,dlon,dlat)
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
	
	mask.to_netcdf( os.path.join( pathOut , "mask_{}_{}x{}.nc".format(ncountry,dlon,dlat) ) )
	
	## Remove temporary
	##=================
	tmp.clean()


if __name__ == "__main__":
	
	
	message = main_function(sys.argv)
	
	if message is not None:
		print(message)




#	
#	
#	
#	## Remove temporary
#	##=================
#	tmp.clean()
	
