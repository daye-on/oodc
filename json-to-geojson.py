import geojson
import json

file = 'sample/91c7f57a-2571-42af-9cbf-0dfb325b91a1.stac-item.json'

def convert_json_to_geojson(fdata):
    parsed_json = json.load(open(fdata))
    feature = geojson.Feature(geometry=parsed_json['geometry'], properties=parsed_json['properties'])
    feature_collection = geojson.FeatureCollection([feature])
    return feature_collection

result = convert_json_to_geojson(file)
print(geojson.dumps(result, indent=2))