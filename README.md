# Frozen Hell map page thing
Can be found hosted online at https://thepiguy24.net/dfhmap/ and https://thepiguy24.net/afhmap/  
Based on [Leaflet.js](https://leafletjs.com/)  
  
The web stuff itself is located in the `site` subdir with a subdir further for each server  
The script `zoomlevels.py` can be used to split a full image of the map into correctly sized tiles, but is not needed if not changing the map data (its also jank and set up badly (and now its even worse thanks to threading that wasnt really needed ;3))
