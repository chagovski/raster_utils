import os
import arcpy

# This script is intended for PLANET imagery.
# The script reorders the RGB bands from 3, 2, 1 to 1, 2, 3
# and saves the reordered raster(s) as a new .tif file
# in their original location with "_reordered.tif" suffix.

arcpy.env.overwriteOutput = True

# Provide one or more input rasters here
input_rasters = [
        r"I:\PATH\TO\YOUR\RASTER_1.tif",
        r"I:\PATH\TO\YOUR\RASTER_2.tif"
    ]

print(f"Found {len(input_rasters)} input raster(s).")

for i, raster_path in enumerate(input_rasters, start=1):
    print(f"\n--- [{i}/{len(input_rasters)}] ---")
    print(f"Input: {raster_path}")

    if not arcpy.Exists(raster_path):
        print("Skipping: input raster does not exist.")
        continue

    desc = arcpy.Describe(raster_path)
    band_count = desc.bandCount

    if band_count < 3:
        print(f"Skipping: raster has only {band_count} band(s).")
        continue

    folder = os.path.dirname(raster_path)
    base_name = os.path.splitext(os.path.basename(raster_path))[0]
    output_raster = os.path.join(folder, f"{base_name}_reordered.tif")

    input_bands = [
        raster_path + r"\Band_3",
        raster_path + r"\Band_2",
        raster_path + r"\Band_1",
    ]

    arcpy.management.CompositeBands(
        in_rasters=input_bands,
        out_raster=output_raster
    )

    print(f"Created: {output_raster}")

print("\nDone.")
