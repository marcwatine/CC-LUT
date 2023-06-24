import os
import geopandas as gpd
import requests
import logging
import urllib.request
import rarfile
from pyunpack import Archive

def descargar_opccc(id_capa, save_dir):
    # Found inspecting the website. Function is 'descargar' from the js file in:
    # top/www.opccc-ctp.org/sites/all/libraries/geoportal/js/function.js --> line 1987 CTRL+F "function descargar(id_capa)"
    ruta_estandar = "https://www.opcc-ctp.org/sites/all/libraries/geoportal/"
    ruta_services = ruta_estandar + "services/"
    url = ruta_services + "descargar.php?id=" + id_capa
    # ---- Read Filename ----
    response = requests.head(url)
    content_disposition = response.headers.get("Content-Disposition")
    try:
        # Extract the filename from the Content-Disposition header
        filename = content_disposition.split("filename=")[1].strip('"')
    except:
        logging.ERROR(
            f"No Filename {id_capa}, see content dispo: {content_disposition}"
        )

    # ---- Download .rar file ----
    if filename not in os.listdir(save_dir):
        logging.warning(f'Downloading {filename}')
        urllib.request.urlretrieve(url, save_dir+filename)

    # ---- Unzip file ----
    Archive(save_dir+filename).extractall(save_dir)

    # ---- Convert shapefile to geojson (because we don't like shapefiles) ----
    shp_filename = filename.split('_id')[0] + '.shp'
    geojson_filename = filename.split('_id')[0] + '.geojson'
    gdf = gpd.read_file(save_dir+shp_filename)
    gdf.to_file(save_dir+geojson_filename, driver='GeoJSON')

    # ---- Return the filepath to keep track of the now useful file ---- 
    return save_dir+geojson_filename