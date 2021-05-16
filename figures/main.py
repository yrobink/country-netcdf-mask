
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
import pickle as pk
import itertools as itt

import numpy  as np
import pandas as pd
import xarray as xr


import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cf
import cartopy.io.shapereader as shpreader
import matplotlib.gridspec as gridspec
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


####################
## Paramètres mpl ##
####################

mpl.rcParams['font.size'] = 15
#plt.rc('text', usetex=True)


###############
## Fonctions ##
###############

def plot_France_WGS84():##{{{
	## Path
	path = os.path.dirname(os.path.realpath(__file__))
	
	## Load mask
	dataF = xr.open_dataset( os.path.join( path , "../output" , "mask_France_WGS84.nc" ) )
	dataO = xr.open_dataset( os.path.join( path , "../output" , "mask_France_Occitanie_WGS84.nc" ) )
	
	## Data to plot
	lon,lat = dataF.lon,dataF.lat
	_,ny,nx = dataF.mask.shape
	X,Y = np.meshgrid(np.linspace(-np.pi,np.pi,nx),np.linspace(-np.pi,np.pi,ny))
	Z = np.sin(X**2 + Y**2)
	ZF = np.where( dataF.mask[0,:,:] > 0 , Z , np.nan )
	ZO = np.where( dataO.mask[0,:,:] > 0 , Z , np.nan )
	
	Zc = np.ones_like(Z)
	ZFc = np.where( dataF.mask[0,:,:] > 0 , np.nan , Zc )
	ZOc = np.where( dataO.mask[0,:,:] > 0 , np.nan , Zc )
	
	## Cartopy features
	shfileF   = os.path.join( path , "../cnmask/data/gadm36_FRA_shp/gadm36_FRA_0.shp" )
	featuresF = cf.ShapelyFeature( shpreader.Reader(shfileF).geometries() , ccrs.PlateCarree(), facecolor = 'none' )
	shfileO    = os.path.join( path , "../cnmask/data/gadm36_FRA_shp/gadm36_FRA_1.shp" )
	featuresO = cf.ShapelyFeature( shpreader.Reader(shfileO).geometries() , ccrs.PlateCarree(), facecolor = 'none' )
	
	## Plot itself
	fig = plt.figure( figsize = (2 * 9,10) )
	gs  = gridspec.GridSpec( 2 , 2 , height_ratios = [1,0.03] )
	
	levels = np.linspace( -1 , 1 , 50 )
	
	## Plot of the france
	ax = fig.add_subplot( gs[0,0] , projection = ccrs.Mercator() )
	im = ax.contourf( lon , lat , ZF  , cmap = plt.cm.turbo , levels = levels , zorder = 1 , transform = ccrs.PlateCarree() )
	ax.contourf( lon , lat , ZFc , cmap = plt.cm.Blues , levels = 1 , alpha = 0.4 , zorder = 1 , transform = ccrs.PlateCarree() )
	ax.add_feature( featuresF , edgecolor = "black" , zorder = 2 )
	ax.set_extent( [-6,11,40,52] )
	ax.set_title("Mask France (WGS84)")
	
	## Plot of Occitanie
	ax = fig.add_subplot( gs[0,1] , projection = ccrs.Mercator() )
	im = ax.contourf( lon , lat , ZO  , cmap = plt.cm.turbo , levels = levels , zorder = 1 , transform = ccrs.PlateCarree() )
	ax.contourf( lon , lat , ZOc , cmap = plt.cm.Blues , levels = 1 , alpha = 0.4 , zorder = 1 , transform = ccrs.PlateCarree() )
	ax.add_feature( featuresO , edgecolor = "black" , zorder = 2 )
	ax.set_extent( [-6,11,40,52] )
	ax.set_title("Mask Occitanie, in France (WGS84)")
	
	
	## And now colorbar
	cax = fig.add_subplot( gs[1,:] )
	plt.colorbar( mappable = im , cax  = cax , orientation = "horizontal" , ticks = [-1,-0.5,0,0.5,1] )
	
	fig.subplots_adjust( top = 0.95 , bottom = 0.03 , left = 0.03 , right = 0.97 , hspace = 0.05 , wspace = 0.01 )
	plt.savefig( os.path.join( path , "France_WGS84.png" ) )
	plt.close(fig)
##}}}

def plot_France_LambertII():##{{{
	## Path
	path = os.path.dirname(os.path.realpath(__file__))
	
	## Load mask
	dataF = xr.open_dataset( os.path.join( path , "../output" , "mask_France_LambertII.nc" ) )
	dataO = xr.open_dataset( os.path.join( path , "../output" , "mask_France_Occitanie_LambertII.nc" ) )
	
	## Data to plot
	lon,lat = dataF.lon,dataF.lat
	_,ny,nx = dataF.mask.shape
	X,Y = np.meshgrid(np.linspace(-np.pi,np.pi,nx),np.linspace(-np.pi,np.pi,ny))
	Z = np.sin(X**2 + Y**2)
	ZF = np.where( dataF.mask[0,:,:] > 0 , Z , np.nan )
	ZO = np.where( dataO.mask[0,:,:] > 0 , Z , np.nan )
	
	Zc = np.ones_like(Z)
	ZFc = np.where( dataF.mask[0,:,:] > 0 , np.nan , Zc )
	ZOc = np.where( dataO.mask[0,:,:] > 0 , np.nan , Zc )
	
	## Cartopy features
	shfileF   = os.path.join( path , "../cnmask/data/gadm36_FRA_shp/gadm36_FRA_0.shp" )
	featuresF = cf.ShapelyFeature( shpreader.Reader(shfileF).geometries() , ccrs.PlateCarree(), facecolor = 'none' )
	shfileO    = os.path.join( path , "../cnmask/data/gadm36_FRA_shp/gadm36_FRA_1.shp" )
	featuresO = cf.ShapelyFeature( shpreader.Reader(shfileO).geometries() , ccrs.PlateCarree(), facecolor = 'none' )
	
	## Plot itself
	fig = plt.figure( figsize = (2 * 9,10) )
	gs  = gridspec.GridSpec( 2 , 2 , height_ratios = [1,0.03] )
	
	levels = np.linspace( -1 , 1 , 50 )
	
	## Plot of the france
	ax = fig.add_subplot( gs[0,0] , projection = ccrs.Mercator() )
	im = ax.contourf( lon , lat , ZF  , cmap = plt.cm.turbo , levels = levels , zorder = 1 , transform = ccrs.PlateCarree() )
	ax.contourf( lon , lat , ZFc , cmap = plt.cm.Blues , levels = 1 , alpha = 0.4 , zorder = 1 , transform = ccrs.PlateCarree() )
	ax.add_feature( featuresF , edgecolor = "black" , zorder = 2 )
	ax.set_extent( [-6,11,40,52] )
	ax.set_title("Mask France (Lambert II)")
	
	## Plot of Occitanie
	ax = fig.add_subplot( gs[0,1] , projection = ccrs.Mercator() )
	im = ax.contourf( lon , lat , ZO  , cmap = plt.cm.turbo , levels = levels , zorder = 1 , transform = ccrs.PlateCarree() )
	ax.contourf( lon , lat , ZOc , cmap = plt.cm.Blues , levels = 1 , alpha = 0.4 , zorder = 1 , transform = ccrs.PlateCarree() )
	ax.add_feature( featuresO , edgecolor = "black" , zorder = 2 )
	ax.set_extent( [-6,11,40,52] )
	ax.set_title("Mask Occitanie, in France (Lambert II)")
	
	
	## And now colorbar
	cax = fig.add_subplot( gs[1,:] )
	plt.colorbar( mappable = im , cax  = cax , orientation = "horizontal" , ticks = [-1,-0.5,0,0.5,1] )
	
	fig.subplots_adjust( top = 0.95 , bottom = 0.03 , left = 0.03 , right = 0.97 , hspace = 0.05 , wspace = 0.01 )
	plt.savefig( os.path.join( path , "France_LambertII.png" ) )
	plt.close(fig)
##}}}

def plot_Italy_WGS84():##{{{
	## Path
	path = os.path.dirname(os.path.realpath(__file__))
	
	## Load mask
	dataF = xr.open_dataset( os.path.join( path , "../output" , "mask_Italy_WGS84.nc" ) )
	dataO = xr.open_dataset( os.path.join( path , "../output" , "mask_Italy_Sicily_WGS84.nc" ) )
	
	## Data to plot
	lon,lat = dataF.lon,dataF.lat
	_,ny,nx = dataF.mask.shape
	X,Y = np.meshgrid(np.linspace(-np.pi,np.pi,nx),np.linspace(-np.pi,np.pi,ny))
	Z = np.sin(X**2 + Y**2)
	ZF = np.where( dataF.mask[0,:,:] > 0 , Z , np.nan )
	ZO = np.where( dataO.mask[0,:,:] > 0 , Z , np.nan )
	
	Zc = np.ones_like(Z)
	ZFc = np.where( dataF.mask[0,:,:] > 0 , np.nan , Zc )
	ZOc = np.where( dataO.mask[0,:,:] > 0 , np.nan , Zc )
	
	## Cartopy features
	shfileF   = os.path.join( path , "../cnmask/data/gadm36_ITA_shp/gadm36_ITA_0.shp" )
	featuresF = cf.ShapelyFeature( shpreader.Reader(shfileF).geometries() , ccrs.PlateCarree(), facecolor = 'none' )
	shfileO    = os.path.join( path , "../cnmask/data/gadm36_ITA_shp/gadm36_ITA_1.shp" )
	featuresO = cf.ShapelyFeature( shpreader.Reader(shfileO).geometries() , ccrs.PlateCarree(), facecolor = 'none' )
	
	## Plot itself
	fig = plt.figure( figsize = (2 * 7,10) )
	gs  = gridspec.GridSpec( 2 , 2 , height_ratios = [1,0.03] )
	
	levels = np.linspace( -1 , 1 , 50 )
	extent = [6,19.5,34.5,48]
	
	## Plot of the france
	ax = fig.add_subplot( gs[0,0] , projection = ccrs.Mercator() )
	im = ax.contourf( lon , lat , ZF  , cmap = plt.cm.turbo , levels = levels , zorder = 1 , transform = ccrs.PlateCarree() )
	ax.contourf( lon , lat , ZFc , cmap = plt.cm.Blues , levels = 1 , alpha = 0.4 , zorder = 1 , transform = ccrs.PlateCarree() )
	ax.add_feature( featuresF , edgecolor = "black" , zorder = 2 )
	ax.set_extent( extent )
	ax.set_title("Mask Italy (WGS84)")
	
	## Plot of Occitanie
	ax = fig.add_subplot( gs[0,1] , projection = ccrs.Mercator() )
	im = ax.contourf( lon , lat , ZO  , cmap = plt.cm.turbo , levels = levels , zorder = 1 , transform = ccrs.PlateCarree() )
	ax.contourf( lon , lat , ZOc , cmap = plt.cm.Blues , levels = 1 , alpha = 0.4 , zorder = 1 , transform = ccrs.PlateCarree() )
	ax.add_feature( featuresO , edgecolor = "black" , zorder = 2 )
	ax.set_extent( extent )
	ax.set_title("Mask Sicily, in Italy (WGS84)")
	
	
	## And now colorbar
	cax = fig.add_subplot( gs[1,:] )
	plt.colorbar( mappable = im , cax  = cax , orientation = "horizontal" , ticks = [-1,-0.5,0,0.5,1] )
	
	fig.subplots_adjust( top = 0.95 , bottom = 0.03 , left = 0.03 , right = 0.97 , hspace = 0.05 , wspace = 0.01 )
	plt.savefig( os.path.join( path , "Italy_WGS84.png" ) )
	plt.close(fig)
##}}}


#############
## Classes ##
#############

##########
## main ##
##########

if __name__ == "__main__":
	
	plot_France_WGS84()
	plot_France_LambertII()
	plot_Italy_WGS84()
	
	print("Done")


