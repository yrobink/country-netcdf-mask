
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

###############
## Libraries ##
###############

import sys,os
import itertools as itt
import datetime as dt
import zipfile
import pathlib


import numpy as np
import xarray as xr
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point,Polygon,MultiPoint

import matplotlib as mpl
import matplotlib.pyplot as plt

import cnmask as cnm


###########################
## Classes and functions ##
###########################

class GridParams:##{{{
	
	def __init__( self , file_in ):##{{{
		lp = {}
		
		with open( file_in , "r" ) as f:
			lines = f.readlines()
			for line in lines:
				try:
					p,val = line.split("\n")[0].split("=")
					lp[p] = val
				except: pass
		
		for p in ["xmin","xmax","dx","ymin","ymax","dy","epsg"]:
			try:
				assert( p in lp.keys() )
			except:
				print("Grid params {} not given".format(p))
			try:
				if p == "epsg": lp[p] = int(lp[p])
				else: lp[p] = float(lp[p])
			except:
				print("Bad value for params {}".format(p))
		
		self.xmin = lp["xmin"]
		self.xmax = lp["xmax"]
		self.dx   = lp["dx"]
		self.ymin = lp["ymin"]
		self.ymax = lp["ymax"]
		self.dy   = lp["dy"]
		self.epsg = lp["epsg"]
		
		self.kwargs = { "xparams" : (self.xmin,self.xmax,self.dx),
						"yparams" : (self.ymin,self.ymax,self.dy),
						"epsg"    : self.epsg }
	##}}}
	
##}}}

class CNMParams:
	def __init__( self , *argv ):
		
		self.f_in    = None
		self.f_out   = None
		self.verbose = True
		self.src     = None
		self.list    = False
		
		for p in argv:
			idx = argv.index(p)
			if p == "-i":
				self.f_in = argv[idx+1]
			if p == "-o":
				self.f_out = argv[idx+1]
			if p == "-src":
				self.src = argv[idx+1]
			if p == "--not-verbose":
				self.verbose = False
			if p == "-list":
				self.list = True
	
	def src_is_gadm36(self):
		return self.src.split(",")[0].lower() == "gadm36"

##########
## main ##
##########

## TODO
## - Add software used to create the mask (the github)
## - Add reference of shapefile data used
## - weight instead of boolean

if __name__ == "__main__":
	
	cnm_params  = CNMParams(*sys.argv[1:])
	grid_params = GridParams(cnm_params.f_in)
	
	## Load data
	if cnm_params.src_is_gadm36():
		data = cnm.load_gadm36(cnm_params)
	
	## Infered grid params
	boxes = list(data["geometry"].bounds.values.squeeze())
	boxes[1],boxes[2] = boxes[2],boxes[1]
	boxes = np.round(boxes)
	boxes[[0,2]] -= 0.5
	boxes[[1,3]] += 0.5
	polygon = [(boxes[0],boxes[2]),(boxes[0],boxes[3]),(boxes[1],boxes[3]),(boxes[1],boxes[2]),(boxes[0],boxes[2])]
	bounds = gpd.GeoDataFrame( [ {"geometry" : Polygon(polygon) } ] , crs = "EPSG:4326" )
	print(boxes)
	
	## Define grid
#	grid = cnm.Grid(**grid_params.kwargs)
#	
#	## Build mask
#	mask_array = cnm.build_mask( data , grid )
#	
#	## To xarray
#	ncdata,encoding = cnm.to_dataset( mask_array , grid )
#	
#	## Into netcdf
#	ncdata.to_netcdf( cnm_params.f_out , encoding = encoding )
	
	print("Done")
