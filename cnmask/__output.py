
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

import datetime as dt
import xarray as xr
from .__grid import Grid


## Functions
##==========

def _to_dataset_4326( mask_array , grid : Grid ):##{{{
	
	## Define the grid mapping
	gm_name = "WGS_84"
	
	## Dims
	xrdims = ["time","y","x"]
	
	## Variables
	lat      = xr.DataArray( grid.lat , dims = ["y"] )
	lon      = xr.DataArray( grid.lon , dims = ["x"] )
	xrcoords = { "time" : [dt.datetime(1900,1,1)] , "lat" : lat , "lon" : lon }
	mask     = xr.DataArray( mask_array.reshape(1,grid.ny,grid.nx).astype(int)  , dims = xrdims , coords = xrcoords )
	ncdata   = xr.Dataset( { "mask" : mask , gm_name : 1 } )
	
	## Attributes
	ncdata.attrs["title"] = "Mask"
	ncdata.attrs["Conventions"] = "CF-1.0"
	ncdata.attrs["creation_date"] = str(dt.datetime.today())[:19]
	
	ncdata[gm_name].attrs["EPSG"]       = "{}".format(grid.epsg)
	ncdata[gm_name].attrs["references"] = "https://spatialreference.org/ref/epsg/{}/".format(grid.epsg)
	
	ncdata.mask.attrs["long_name"] = "Mask on the grid [{},{}]x[{},{}] by {}x{} degrees".format(grid.xmin,grid.xmax,grid.ymin,grid.ymax,grid.dx,grid.dy)
	
	ncdata.time.attrs["axis"]          = "T"
	ncdata.time.attrs["standard_name"] = "time"
	ncdata.time.attrs["long_name"]     = "time axis"
	
	ncdata.lat.attrs["axis"]           = "y"
	ncdata.lat.attrs["long_name"]      = "Latitude"
	ncdata.lat.attrs["standard_name"]  = "latitude"
	ncdata.lat.attrs["units"]          = "degrees_north"
	
	ncdata.lon.attrs["axis"]           = "x"
	ncdata.lon.attrs["long_name"]      = "Longitude"
	ncdata.lon.attrs["standard_name"]  = "longitude"
	ncdata.lon.attrs["units"]          = "degrees_east"
	
	## Encoding
	encoding = { "time" : { "dtype" : "double" , "zlib" : True , "complevel": 9 } ,
				 "lon"  : { "dtype" : "double" , "zlib" : True , "complevel": 9 } ,
				 "lat"  : { "dtype" : "double" , "zlib" : True , "complevel": 9 } ,
				 "mask" : { "dtype" : "int"    , "zlib" : True , "complevel": 9 } }
	
	return ncdata,encoding
##}}}

def _to_dataset_generic( mask_array , grid : Grid ):##{{{
	
	## Define the grid mapping
	gm_name   = grid.df.crs.coordinate_operation.name.replace(" ","_")
	gm_method = grid.df.crs.coordinate_operation.method_name.replace(" ","_").replace("(","").replace(")","")
	
	## Dims
	xrdims = ["time","y","x"]
	
	## Variables
	lat      = xr.DataArray( grid.lat , dims = ["y","x"] )
	lon      = xr.DataArray( grid.lon , dims = ["y","x"] )
	xrcoords = { "time" : [dt.datetime(1900,1,1)] , "y" : grid.y , "x" : grid.x }
	mask     = xr.DataArray( mask_array.reshape(1,grid.ny,grid.nx).astype(int)  , dims = xrdims , coords = xrcoords )
	ncdata   = xr.Dataset( { "mask" : mask , "lat" : lat , "lon" : lon , gm_name : 1 } )
	
	## Attributes
	ncdata.attrs["title"] = "Mask"
	ncdata.attrs["Conventions"]   = "CF-1.0"
	ncdata.attrs["creation_date"] = str(dt.datetime.today())[:19]
	
	ncdata[gm_name].attrs["grid_mapping_name"] = gm_method
	ncdata[gm_name].attrs["EPSG"]              = "{}".format(grid.epsg)
	ncdata[gm_name].attrs["references"]        = "https://spatialreference.org/ref/epsg/{}/".format(grid.epsg)
	
	ncdata.mask.attrs["long_name"]    = "Mask on the grid [{},{}]x[{},{}] by {}x{}".format(grid.xmin,grid.xmax,grid.ymin,grid.ymax,grid.dx,grid.dy)
	ncdata.mask.attrs["grid_mapping"] = gm_name
	
	ncdata.x.attrs["standard_name"] = "projection_x_coordinate"
	ncdata.x.attrs["long_name"]     = "x coordinate of projection"
	ncdata.x.attrs["units"]         = grid.df.crs.axis_info[0].unit_name
	ncdata.x.attrs["axis"]          = grid.df.crs.axis_info[0].abbrev
	
	ncdata.y.attrs["standard_name"] = "projection_x_coordinate"
	ncdata.y.attrs["long_name"]     = "x coordinate of projection"
	ncdata.y.attrs["units"]         = grid.df.crs.axis_info[1].unit_name
	ncdata.y.attrs["axis"]          = grid.df.crs.axis_info[1].abbrev
	
	ncdata.time.attrs["axis"]          = "T"
	ncdata.time.attrs["standard_name"] = "time"
	ncdata.time.attrs["long_name"]     = "time axis"
	
	ncdata.lat.attrs["axis"]           = "y"
	ncdata.lat.attrs["long_name"]      = "Latitude"
	ncdata.lat.attrs["standard_name"]  = "latitude"
	ncdata.lat.attrs["units"]          = "degrees_north"
	
	ncdata.lon.attrs["axis"]           = "x"
	ncdata.lon.attrs["long_name"]      = "Longitude"
	ncdata.lon.attrs["standard_name"]  = "longitude"
	ncdata.lon.attrs["units"]          = "degrees_east"
	
	## Encoding
	encoding = { "time" : { "dtype" : "double" , "zlib" : True , "complevel": 9 } ,
				 "x"    : { "dtype" : "double" , "zlib" : True , "complevel": 9 } ,
				 "y"    : { "dtype" : "double" , "zlib" : True , "complevel": 9 } ,
				 "lon"  : { "dtype" : "double" , "zlib" : True , "complevel": 9 } ,
				 "lat"  : { "dtype" : "double" , "zlib" : True , "complevel": 9 } ,
				 "mask" : { "dtype" : "int"    , "zlib" : True , "complevel": 9 } }
	
	return ncdata,encoding
##}}}

def to_dataset( mask_array , grid : Grid ):##{{{
	
	if grid.epsg == 4326:
		return _to_dataset_4326( mask_array , grid )
	
	return _to_dataset_generic( mask_array , grid )
##}}}


