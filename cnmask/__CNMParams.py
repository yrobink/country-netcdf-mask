
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
##########

import texttable as tt
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon


## Classes
##########

class CNMParams:
	
	def __init__( self , *argv ):##{{{
		
		self.f_in    = None
		self.f_out   = None
		self.verbose = True
		self.src     = None
		self.list    = False
		self.bounds  = False
		
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
			if p == "-bounds":
				self.bounds = True
	##}}}
	
	def src_is_gadm36(self):##{{{
		return self.src.split(",")[0].lower() == "gadm36"
	##}}}
	
	def find_bounds( self , data , grid ):##{{{
		boxes = list(data["geometry"].bounds.values.squeeze())
		boxes[1],boxes[2] = boxes[2],boxes[1]
		rboxes = np.round(boxes)
		rboxes[[0,2]] -= 0.5
		rboxes[[1,3]] += 0.5
		polygon = [(boxes[0],boxes[2]),(boxes[0],boxes[3]),(boxes[1],boxes[3]),(boxes[1],boxes[2]),(boxes[0],boxes[2])]
		bounds_4326 = gpd.GeoDataFrame( [ {"geometry" : Polygon(polygon) } ] , crs = "EPSG:4326" )
		bounds_epsg = bounds_4326.to_crs( epsg = grid.epsg )
		boxes_epsg  = list(bounds_epsg["geometry"].bounds.values.squeeze())
		
		tab = tt.Texttable(max_width = 0)
		tab.header( ["Projection","xmin","xmax","ymin","ymax"] )
		tab.add_row( ["EPSG:4326"] + boxes )
		tab.add_row( ["EPSG:4326, rounded"] + rboxes.tolist() )
		tab.add_row( ["EPSG:{}".format(grid.epsg)] + boxes_epsg )
		
		self.boxes_4326  = boxes
		self.boxesr_4326 = rboxes.tolist()
		self.boxes_epsg  = boxes_epsg
		self.bounds_tab  = tab
	##}}}
	


