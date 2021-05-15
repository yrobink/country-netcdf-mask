
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

import numpy as np
import geopandas as gpd
from shapely.geometry import MultiPoint


## Classes
##########


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

class Grid:##{{{
	
	def __init__( self , xparams , yparams , epsg = 4326 ):##{{{
		self.xparams = xparams
		self.yparams = yparams
		self.epsg    = epsg
		
		self.x  = np.arange( self.xmin , self.xmax + self.dx / 2 , self.dx )
		self.y  = np.arange( self.ymin , self.ymax + self.dy / 2 , self.dy )
		X,Y     = np.meshgrid(self.x,self.y)
		self.df = gpd.GeoDataFrame( [ {"geometry" : MultiPoint([(x,y) for x,y in zip(X.ravel(),Y.ravel())]) } ] , crs = "EPSG:{}".format(self.epsg) )
		
		self.lat = None
		self.lon = None
		self._build_latlon()
		
	##}}}

	def _build_latlon(self):##{{{
		if self.epsg == 4326:
			self.lon,self.lat = self.x,self.y
			return
		
		latlon   = np.array(self.df.to_crs( epsg = 4326 )["geometry"][0].array_interface()["data"]).reshape(-1,2)
		self.lon = latlon[:,0].reshape(self.ny,self.nx)
		self.lat = latlon[:,1].reshape(self.ny,self.nx)
		
	##}}}
	
	## Properties ##{{{
	@property
	def xmin(self):
		return self.xparams[0]
	
	@property
	def xmax(self):
		return self.xparams[1]
	
	@property
	def dx(self):
		return self.xparams[2]
	
	@property
	def nx(self):
		return self.x.size
	
	@property
	def ymin(self):
		return self.yparams[0]
	
	@property
	def ymax(self):
		return self.yparams[1]
	
	@property
	def dy(self):
		return self.yparams[2]
	
	@property
	def ny(self):
		return self.y.size
	
	##}}}
##}}}

