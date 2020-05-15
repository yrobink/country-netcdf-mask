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
import itertools as itt
import pickle as pk

## Scientific libraries
##=====================
import numpy as np
import xarray as xr


## Plot libraries
##===============
import matplotlib as mpl
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

from cartopy.mpl.geoaxes import GeoAxes
from mpl_toolkits.axes_grid1 import AxesGrid


##}}}
###############

###############
## Fonctions ##
###############

def cgrid_to_bound( G ):##{{{
	pG = np.zeros(np.array(G.shape)+1)
	pG[:-1,:-1] = G
	pG[-1,:] = pG[-2,:] + 1 * (pG[-2,:] - pG[-3,:])
	pG[:,-1] = pG[:,-2] + 1 * (pG[:,-2] - pG[:,-3])
	pG -= 0.05
	
	return pG 
##}}}


#############
## Classes ##
#############


##########
## main ##
##########

if __name__ == "__main__":
	
	## Load data
	##==========
	l_data = [ xr.open_dataset( "data/{}_tg_mean_1961-1990.nc".format(cn) ) for cn in ["FR","DE","ES","IT"] ]
	
	## Find min / max
	##===============
	vmin,vmax = 1e9,-1e9
	for data in l_data:
		vmin = min( vmin , np.nanmin(data.tg.values) )
		vmax = max( vmax , np.nanmax(data.tg.values) )
	mean_EU = 9.66
	vmin -= mean_EU
	vmax -= mean_EU
	vmax = max( vmax , abs(vmin) )
	vmin = -vmax
	
	## Features of plot
	##=================
	f_country = cf.NaturalEarthFeature( "cultural" , "admin_0_boundary_lines_land" , "50m" )
	f_land    = cf.NaturalEarthFeature( "physical" , "land"  , "50m" )
	f_ocean   = cf.NaturalEarthFeature( "physical" , "ocean" , "50m" )
	proj0     = ccrs.PlateCarree()
	proj1     = ccrs.PlateCarree()
	kwargs = { "transform" : proj1 , "cmap" : plt.cm.seismic , "vmin" : vmin, "vmax" : vmax , "alpha" : 0.9 }
	
	fig = plt.figure( figsize = (12,8) )
	axes_class = ( GeoAxes , dict( map_projection = proj0 ) )
	axgr = AxesGrid( fig , rect = [0.01,0.01,0.95,0.95] , axes_class=axes_class,
                    nrows_ncols=(2, 2),
                    axes_pad=0.8,
                    cbar_location='right',
                    cbar_mode='single',
                    cbar_pad=0.1,
                    cbar_size='3%',
                    label_mode="")
	
	for data,ax in zip(l_data,axgr):
		lon,lat = np.meshgrid( data.longitude , data.latitude )
		lat = cgrid_to_bound(lat)
		lon = cgrid_to_bound(lon)
		
		im = ax.pcolormesh( lon , lat , data.tg.values.squeeze() - mean_EU , **kwargs )
		ax.add_feature( f_country , zorder = 1 , edgecolor = "black" , facecolor = "none")
		ax.add_feature( f_land    , zorder = 0 , edgecolor = "black" , facecolor = "wheat" )
		ax.add_feature( f_ocean   , zorder = 0 , edgecolor = "black" , facecolor = "cornflowerblue" )
		ax.set_extent( [-10,20,35,56] )
	
	cax = axgr.cbar_axes[0].colorbar( im )
	cax.set_label_text("European temperature (1961-1990, anomaly w.r.t. EU mean temperature)")
	plt.savefig("figure/example.png")
	
	print("Done")
