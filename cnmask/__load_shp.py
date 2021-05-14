
## Copyright(c) 2021 Yoann Robin
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

## Imports
##========

import os
import pathlib
import zipfile
import urllib.request as urlreq

import geopandas as gpd


## Functions
##==========

def load_gadm36(cnm_params):##{{{
	"""
	cnmask.load_gadm36
	==================
	
	"""
	src_split = cnm_params.src.split(",")
	subselect = None
	if len(src_split) == 3:
		_,country,level = src_split
	if len(src_split) == 4:
		_,country,level,subselect = src_split
	
	## Load data
	path = os.path.join( os.path.dirname(os.path.realpath(__file__)) , "data" )
	path_extract = os.path.join( path , "gadm36_{}_shp".format(country) )
	fzip   = os.path.join( path , "gadm36_{}_shp.zip".format(country) )
	plfzip = pathlib.Path(fzip)
	url    = "https://biogeo.ucdavis.edu/data/gadm3.6/shp/gadm36_{}_shp.zip".format(country)
	if not plfzip.exists():
		with open( fzip , "wb" ) as f: f.write(urlreq.urlopen(url).read())
	
	if not os.path.exists(path_extract):
		with zipfile.ZipFile( fzip , "r" ) as zf:
			zf.extractall( path_extract )
	
	## Read file
	data = gpd.read_file( os.path.join( path_extract , "gadm36_{}_{}.shp" ).format(country,level) )
	
	if cnm_params.list:
		print(data["NAME_{}".format(level)])
	
	if subselect is not None:
		key,key_value = subselect.split("=")
		data = data[data[key] == key_value]
	
	if data.index.size == 1:
		data.index = [0]
	
	return data
##}}}


