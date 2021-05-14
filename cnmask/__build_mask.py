
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
import pandas as pd
import geopandas as gpd


## Function
###########

def build_mask( data , grid ):
	dI = gpd.overlay( grid.df , data.to_crs(epsg=grid.epsg) , how = "intersection" , keep_geom_type = False )
	dO = gpd.overlay( grid.df , data.to_crs(epsg=grid.epsg) , how = "difference"   , keep_geom_type = False )
	
	dataI = np.array(dI["geometry"][0].array_interface()["data"]).reshape(-1,2)
	dataO = np.array(dO["geometry"][0].array_interface()["data"]).reshape(-1,2)
	dataM = pd.DataFrame( np.vstack((dataI,dataO)) , columns = ["x","y"] )
	dataM["mask"] = np.nan
	dataM.iloc[:dataI.shape[0],2] = True
	dataM.iloc[dataI.shape[0]:,2] = False
	dataM = dataM.sort_values(["x","y"])
	
	mask_array = dataM["mask"].values.astype(int).reshape(grid.nx,grid.ny).T
	
	return mask_array

