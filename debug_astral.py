"""
Debug script to see what's in Astral's database
"""
from astral import geocoder

db = geocoder.database()

print(f"Total keys: {len(db.keys())}")
print("\nFirst 10 keys:")
for i, key in enumerate(sorted(db.keys())[:10]):
    print(f"  {key}: {type(db[key])} = {db[key]}")

print("\nChecking for city-like entries:")
for key in sorted(db.keys()):
    value = db[key]
    if not isinstance(value, dict):
        print(f"  {key}: {type(value)} = {value}")
        break

