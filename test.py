from pyproj import Proj, transform

# Define the source and destination projections
source_proj = Proj(init='epsg:4326')  # EPSG:4326 - WGS 84
dest_proj = Proj(init='epsg:3857')   # EPSG:3857 - Web Mercator

# Example coordinate in EPSG:4326 (longitude, latitude)
lat, lon = 47.608013, -122.335167  # Example coordinate for Seattle, WA

# Convert from EPSG:4326 to EPSG:3857
x, y = transform(source_proj, dest_proj, lon, lat)

print(f"Original EPSG:4326 coordinates: ({lon}, {lat})")
print(f"Converted EPSG:3857 coordinates: ({x:.0f}, {y:.0f})")
