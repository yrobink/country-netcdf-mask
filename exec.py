
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
import cnmask as cnm


###########################
## Classes and functions ##
###########################

def main(*argv):##{{{
	cnm_params  = cnm.CNMParams(*argv)
	grid_params = cnm.GridParams(cnm_params.f_in)
	
	## Load data
	if cnm_params.src_is_gadm36():
		data = cnm.load_gadm36(cnm_params)
	
	## Define grid
	grid = cnm.Grid(**grid_params.kwargs)
	cnm_params.find_bounds( data , grid )
	
	## If bounds
	if cnm_params.bounds:
		print(cnm_params.bounds_tab.draw())
	
	if cnm_params.list or cnm_params.bounds:
		return
	
	## Build mask
	mask_array = cnm.build_mask( data , grid )
	
	## To xarray
	ncdata,encoding = cnm.to_dataset( mask_array , grid , cnm_params )
	
	## Into netcdf
	ncdata.to_netcdf( cnm_params.f_out , encoding = encoding )
##}}}


##########
## main ##
##########

## TODO
## - Add software used to create the mask (the github)
## - Add reference of shapefile data used
## - weight instead of boolean

if __name__ == "__main__":
	
	main(*sys.argv[1:])
	
	print("Done")
