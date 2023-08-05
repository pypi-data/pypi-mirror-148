// function TEMPLATE to dynamically fetch and insert a remote image 
// from URL into a leaflet popup. This file should be templated using 
// python's string.Template().substitute() functionality, which will 
// replace the $$idx and $$img parameters with the appropriate
// index number and image name (eg, 12, ABC.jpeg). One of these must be 
// created per popup on the map, hence the need for templating. 

marker_image_$idx.on('click', function() {
    var url = "$remote_image_url/$img"
    var pop = marker_image_$idx.getPopup(); 
    getBase64FromUrl(url).then(
        function(img) {
            var style = popup_image_$idx.getContent().firstElementChild.style;
            var imgh = parseInt(style.height.slice(0,3)); 
            var imgw = parseInt(style.width.slice(0,3)); 

            var margh = window.innerHeight - imgh; 
            var margw = window.innerWidth - imgw; 

            if (margh < margw) { 
                console.log('constrained y')
                h = Math.min(window.innerHeight - 150, 500)
                w = (h / imgh) * imgw; 
            } else { 
                console.log('constrained x')
                w = Math.min(window.innerWidth - 100, 700)
                h = (w / imgw) * imgh; 
            }
            style.width = w + "px";
            style.height = h + "px"; 
            pop.options.maxWidth = "auto";
            pop.options.maxHeight = "auto";
            pop.setContent($$(`<div id="" style='$${style.cssText}'><img src='$${img}' alt='Could not load' style='$${style.cssText}'/></div>`)[0]) 
            var px = map_basemap.project(pop.getLatLng());
            px.y -= 0.7 * h; 
            map_basemap.panTo(map_basemap.unproject(px), {animate: true});

        },
        function(error) { console.log('Could not load b64 remote image'); }
    )

});
