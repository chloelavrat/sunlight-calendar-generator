"""
Script to generate locations.json from Astral's database
"""
import json
from astral import geocoder

def generate_locations_json():
    db = geocoder.database()
    locations = {}
    
    # The database is organized by regions (continents)
    for region_name, region_data in db.items():
        if not isinstance(region_data, dict):
            continue
            
        # Each region contains cities
        for city_key, city_list in region_data.items():
            if not isinstance(city_list, list) or len(city_list) == 0:
                continue
                
            # Get the first LocationInfo object
            location = city_list[0]
            
            # Use the proper name from LocationInfo
            city_name = location.name
            
            locations[city_name] = {
                "country": location.region,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "timezone": location.timezone
            }
    
    # Add Rovaniemi if not present (not in Astral database)
    if "Rovaniemi" not in locations:
        locations["Rovaniemi"] = {
            "country": "Finland",
            "latitude": 66.5039,
            "longitude": 25.7294,
            "timezone": "Europe/Helsinki"
        }
    
    # Write to JSON file
    with open("locations.json", "w", encoding="utf-8") as f:
        json.dump(locations, f, indent=2, ensure_ascii=False)
    
    print(f"Generated locations.json with {len(locations)} cities")

if __name__ == "__main__":
    generate_locations_json()

