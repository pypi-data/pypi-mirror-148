# Tourmapper 

## What is this?

This is a script for generating interactive maps from GPS tracking data and geo-tagged images (see an example [here](https://tomfrankkirk.github.io/tour_maps/tdf.html)). 

<a href="https://tomfrankkirk.github.io/tour_maps/tdf.html">
<img title="Example map" src="demo.png" width="400px" style="display:block; margin:auto;"></a><br>

## Installation 

```
pip install tourmapper 
```

If you get an installation error along the lines of 
```
proj executable not found. Please set the PROJ_DIR variable. For more information see: https://pyproj4.github.io/pyproj/stable/installation.html
```
then there is an issue installing the `pyproj` package via pip. Installation via conda-forge may help correct this (`conda install -c conda-forge pyproj`), then re-attempt the original `pip install tourmapper`. Alternatively, [build pyproj from source](https://pyproj4.github.io/pyproj/stable/installation.html).  

## Usage 

The script wraps [Folium](http://python-visualization.github.io/folium/modules.html#module-folium.map) / [Leaflet](https://leafletjs.com/SlavaUkraini/reference.html), a very sophisticated library for producing interactive maps. Map generation is done using the `tourmapper.make_map()` function using the following arguments. There is some customisation that is possible, but for full control you may want to use those libraries directly (or edit this script). 

### Required arguments 

- `gps_dir` string path to directory containing `.gpx` files, all of which will be loaded in ascending date order. Each file will be a separate trace on the map. 

### Optional arguments 
- `outpath` string path to save map as single `.html` file, default `tourmap.html`
- `map_params` dict containing map-specific arguments passed to `folium.Map()` (see the [Folium](http://python-visualization.github.io/folium/modules.html#module-folium.map) or [Leaflet](https://leafletjs.com/SlavaUkraini/reference.html) documentation)
- `image_dir` string path to directory containing `.jpeg/.jpg` images with GPS EXIF tags, all of which will added to the map
- `line_colours` string, or list of strings which will be cycled, of colours to use when plotting each `.gpx` file. These can either be simple names eg `red` or hex colour code `#3388ff`
- `ride_text` list of strings, same length as number of `.gpx` files, of text to insert on the marker at the end of each file's trace on the map. HTML formatting will be respected. 
- `remote_image_url` string URL stub for remote loading of images (see below section)
- `image_width` default 500, popup size for landscape images
- `image_height` default 400, popup size for portrait images 

### Example usage 

An example with images and text descriptions can be found [here](https://github.com/tomfrankkirk/tour_maps/blob/master/tdf/france.ipynb). 

## Map customisation 

Some useful arguments to customise the map (these must be wrapped up in the `map_params` dict): 

- `api_key`, `style`, `tiles`: customising the basemap. Many options require a paid subscription (see the demos [here](https://github.com/leaflet-extras/leaflet-providers))
- `attr` the text attribution shown in the bottom corner of the map 
- `location` (latitude, longitude) coordinates to center the map
- `zoom_start` initial zoom level between 1 and 20 (far -> near)

## Local vs. remote images 

By default, images are embedded directly within the HTML file containing the map. This means the map and images are completely self-contained within that single file, which makes it very easy to share, but the file size will be large if there are lots of images. If the file is hosted online the load time could be slow.  

The alternative to this is to add the images as remote objects. This keeps the file size down, because they are not embedded into HTML, but means you need somewhere to store the images remotely (a website, hosting service etc) from which they will be loaded on-demand. Remote images can be added using the `remote_image_url` argument. 

### Example

The `image_dir` contains the images `A.jpg`, `B.jpg` and `C.jpg`. To insert them as remote images instead of local, first place them on a remote host (for example, `yourwebsite.com/assets/images`). Pass this URL as the `remote_image_url` argument, and the images A,B,C will be inserted into the map with the following URLs: `yourwebsite.com/assets/images/A.jpg`, `yourwebsite.com/assets/images/B.jpg` etc. 

Note that the resultant map *cannot be viewed using Jupyter notebook* (it must be viewed through a web browser for the associated JS to work). 

If you encounter problems with this functionality, the place to start is by ensuring you can actually access the remote image URLs that have been generated. For example, can you access `yourwebsite.com/assets/images/A.jpg` from a web browser?

## Feedback and bug reports 

Please feel free to provide any feedback or bug reports on this repo. 
