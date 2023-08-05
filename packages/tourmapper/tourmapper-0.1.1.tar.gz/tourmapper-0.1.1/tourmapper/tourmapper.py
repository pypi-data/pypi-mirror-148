import base64
import itertools
import os
import os.path as op
import string

import folium
import geopandas as gpd
import gpxpy
import numpy as np
from folium import plugins
from PIL import Image

B64_LOAD_PATH = op.join(op.dirname(__file__), 'map_helpers', 'load_image_b64.js') 
POPUP_PATH = op.join(op.dirname(__file__), 'map_helpers', 'popup_handler.js') 


def get_img_latlong(img): 
    """
    Extract GPS EXIF data from PIL Image object. GPS 
    is assumed to be in (N,E) degs, mins, secs format, 
    and will be returned as a tuple of decimal floats. 
    """

    exif = img._getexif()
    try: 
        gps = exif[34853]
    except KeyError as e: 
        raise ValueError(f"Could not extract GPS tags from {img.filename}", str(e))

    if (gps[1] not in ['N','S']) or (gps[3] not in ['E','W']):
        raise ValueError("GPS data not in (N,E) format")  

    gps_n = [ float(i) for i in gps[2] ] 
    gps_e = [ float(i) for i in gps[4] ] 
    N = gps_n[0] + (gps_n[1] / 60) + (gps_n[2] / 3600)
    E = gps_e[0] + (gps_e[1] / 60) + (gps_e[2] / 3600)
    if gps[1] == 'S': N *= -1 
    if gps[3] == 'W': E *= -1 
    return (N,E)

def load_rides(from_dir): 
    
    files = os.listdir(from_dir)
    files = [ f for f in files if f.lower().endswith(('.gpx')) ]

    if not files: 
        raise FileNotFoundError(f"Did not find any GPX files in {from_dir}")

    rides = {}

    for fle in files: 
        print("Parsing", fle)
        with open(op.join(from_dir, fle), 'r') as f:
            gpx = gpxpy.parse(f)
        data = [] 
        try: 
            for track in gpx.tracks: 
                for seg in track.segments: 
                        for p in seg.points: 
                            data.append((p.time, p.latitude, p.longitude, p.elevation))

        except Exception as e: 
            raise RuntimeError(f"Could not extract GPS info from {fle}:", e)

        data = list(zip(*data))
        geom = gpd.points_from_xy(data[2], data[1], crs="EPSG:4326")
        gdf = gpd.GeoDataFrame({'geometry': geom, 'elevation': data[3]}, index=data[0])
        gdf = gdf.to_crs("EPSG:3310")
        gdf['distance'] = gdf.geometry.distance(gdf.geometry.shift(1)).fillna(0)
        gdf = gdf.to_crs("EPSG:4326")
        gdf['climb'] = gdf.elevation.diff(1).fillna(0).clip(0, None)
        rides[gdf.index[0]] = gdf 

    return [ rides[time] for time in sorted(rides) ]


def load_images(image_dir): 
    files = os.listdir(image_dir)
    images = [ op.join(image_dir, f) for f in files 
                if f.lower().endswith(('.jpg', '.jpeg')) ]

    return images
 

def make_map(gps_dir, map_params={}, outpath=None, image_dir=None, 
             line_colours=None, ride_text=None, remote_image_url=None, 
             image_width=500, image_height=400): 

    rides = load_rides(gps_dir)
    if not rides: 
        raise RuntimeError("Did not parse any GPX files from", gps_dir)

    if not ride_text: 
        ride_text = [ f"Stage {idx+1}: {r['distance'].sum() / 1000:.0f}km, "
                      f"{r['climb'].sum():.0f}m ascent" 
                      for idx,r in enumerate(rides) ]
    else: 
        if not len(ride_text) == len(rides): 
            raise ValueError("ride_text must contain same number of elements"
                f" as number of rides loaded from gps_dir '{gps_dir}' ({len(rides)})")

    lat_long_cent = np.concatenate([ r.geometry.values[0].xy for r in rides ])
    lat_long_cent = lat_long_cent.reshape(-1,2).mean(0)
    if 'location' not in map_params: 
        map_params['location'] = lat_long_cent[::-1]

    if 'zoom_start' not in map_params: 
        map_params['zoom_start'] = 7 

    mapp = folium.Map(**map_params)
    mapp._id = "basemap"

    if line_colours: 
        colours = itertools.cycle(line_colours)
    else:
        colours = itertools.repeat('#3388ff')

    for idx, (ride, text) in enumerate(zip(rides, ride_text)):
        pop = folium.Popup(text, min_width=200, max_width=300)
        icon = folium.Icon(prefix="fa", icon="fa-duotone fa-flag-checkered", color='blue')
        yx = np.array([ride.geometry.y.values, ride.geometry.x.values]).T
        folium.Marker(yx[-1,:].tolist(), icon=icon, popup=pop).add_to(mapp)
        folium.vector_layers.PolyLine(yx, color=next(colours)).add_to(mapp)

    images = load_images(image_dir) if image_dir else [] 
    if (image_dir) and (not images): 
        raise RuntimeError(f"Did not find any jpeg images in '{image_dir}'")
    if images: 
        print(f"Found {len(images)} images in '{image_dir}'")

    WIDTH = image_width 
    HEIGHT = image_height 

    photo_cluster = plugins.MarkerCluster(name='photo_cluster')
    photo_cluster._id = "photos"

    if remote_image_url and images: 
        print("Remote image URL base supplied, images will load on demand")
        def generate_popup(img, css_style): 
            return f"<img style='{css_style}' alt='Loading image'/>"

        with open(B64_LOAD_PATH) as f: 
            b64loader = f.read()

        with open(POPUP_PATH) as f: 
            popup_template = string.Template(f.read())

        remote_load_js = [ b64loader ] 

    elif images: 
        print("Images will be embedded within final HTML file "
              "(filesize may be very large)")

        remote_load_js = None
        def generate_popup(img, css_style): 
            with open(img.filename, 'rb') as f: 
                b64 = base64.b64encode(f.read()).decode('utf-8')
                b64 = f"data:image/jpeg;base64,{b64}"
                return f"<img src='{b64}' style='{css_style}' />"

    make_css_style = lambda w,h: f"width:{w}px; height:{h}px; object-fit:fill;"

    for idx, img_path in enumerate(images): 
        img = Image.open(img_path)
        gps_img = get_img_latlong(img)
        icon = folium.Icon(prefix="fa", icon="fa-light fa-camera", color='green')  

        landscape = img.size[0] > img.size[1]
        if landscape: 
            height = int(WIDTH / (img.size[0] / img.size[1]))
            style = make_css_style(WIDTH, height)
            pop_args = {'min_width': WIDTH, 'max_width': WIDTH}
        else: 
            width = int(HEIGHT / (img.size[1] / img.size[0]))
            style = make_css_style(width, HEIGHT)
            pop_args = {'min_width': width, 'max_width': width}
            
        popup = folium.Popup(generate_popup(img, style), **pop_args)  
        popup._id = f"image_{idx}"
        marker = folium.Marker(gps_img, icon=icon, popup=popup).add_to(photo_cluster)
        marker._id = f"image_{idx}"

        # now we need to template the popups for remote loading 
        if remote_image_url: 
            img_stub = op.split(img_path)[1]
            pop_load = popup_template.substitute(idx=idx, img=img_stub,
                                                remote_image_url=remote_image_url)
            remote_load_js.append(pop_load)

    photo_cluster.add_to(mapp)

    map_html = mapp.get_root().render()

    if remote_image_url and images: 
        remote_load_js = "\n".join(remote_load_js)
        start = map_html.rfind("<script>") + len("<script>")
        end = map_html.rfind("</script>")
        final = map_html[start:end] + remote_load_js
        map_html = map_html[:start] + final + "\n\n</script>"

    outpath = "tourmap.html" if not outpath else outpath 
    print(f"Writing output to '{outpath}'")
    with open(outpath, 'w') as f: 
        f.write(map_html)

    return mapp 

if __name__ == '__main__': 

    pass 