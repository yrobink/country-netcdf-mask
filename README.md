# country-netcdf-mask
Script and examples to build a netcdf mask of a country

## Description
The python file `build_mask.py` use natural earth data to transform a shape
file to a netcdf file. Some mask are given in masks folder.

## Requirement

Packages used:

- urllib
- zipfile
- numpy
- geopandas
- xarray
- shapely

Use your package manager or pip to install them.

## Usage

Command line arguments:
- `--nedata` or `-ne` Natural earth file. If it is a path, Natural Earth data are downloaded here, else a temporary folder is used.
- `--tmp` or `-t` Temporary folder. If not set, `/tmp/country_ncdfRANDOM` is used.
- `--country` or `-c` Country
- `--lonlatbox` or `-b` Box, if not set, infered from Natural Earth data (can be VERY large)
- `--dlonlat` or `-d` Length of grid point.
- `--list` or `-l` Only print the list of countries available
- `--output` or `-o` Output path

## Example

~~~
python3 build_mask.py -d=0.05 -c=France  -b=-5,10,40,52  -ne=data/ne_10m_admin_0_countries.zip
python3 build_mask.py -d=0.05 -c=Spain   -b=-10,5,35,45  -ne=data/ne_10m_admin_0_countries.zip
python3 build_mask.py -d=0.05 -c=Italy   -b=5.5,20,36,48 -ne=data/ne_10m_admin_0_countries.zip
python3 build_mask.py -d=0.05 -c=Germany -b=5,16,47,55.5 -ne=data/ne_10m_admin_0_countries.zip
~~~

![Alt](/figure/example.png)

## Citation and acknowledgement

The script proposed here is based on the following [tutorial](https://www.wemcouncil.org/wp/wemc-tech-blog-3-calculating-eu-country-averages-with-era5-and-nuts/)

### Related to EOBS data (the figure)

"We acknowledge the E-OBS dataset from the EU-FP6 project UERRA 
(http://www.uerra.eu) and the Copernicus Climate Change Service, and the data
providers in the ECA&D project (https://www.ecad.eu)"

[[1]](https://doi.org/10.1029/2017JD028200) Cornes, R., G. van der Schrier, E.J.M. van den Besselaar, and P.D. Jones. 2018: An Ensemble Version of the E-OBS Temperature and Precipitation Datasets, J. Geophys. Res. Atmos., 123. doi:10.1029/2017JD028200"


