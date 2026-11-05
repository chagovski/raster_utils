import os
import subprocess
import time
from pathlib import Path

def run_cmd(cmd):
    print("\nRunning command:")
    print(" ".join(f'"{c}"' if " " in str(c) else str(c) for c in cmd))
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    start_time = time.perf_counter()

    in_rasters = [
        r"I:\PATH\TO\YOUR\RASTER_1.tif",
        r"I:\PATH\TO\YOUR\RASTER_2.tif"
    ]

    print("Input rasters: ", in_rasters)

    # Output directory where the mosaic will be saved
    out_dir = r"I:\YOUR\OUTPUT\DIRECTORY"
    os.makedirs(out_dir, exist_ok=True)

    # Define the filename for Your mosaic
    out_tif = os.path.join(
        out_dir,
        "YOUR_MOSAIC_FILENAME.tif"
    )

    gdal_exe = r"E:\RESOURCES\PYTHON\envs\gdal_312\Library\bin\gdal.exe"

    # optional: fail fast if an input is missing
    for raster in in_rasters:
        if not os.path.exists(raster):
            raise FileNotFoundError(f"Missing input raster: {raster}")

    cmd = [
        gdal_exe,
        "raster",
        "mosaic",
        "--overwrite",
        "--of", "GTiff",
        "--src-nodata", "0,0,0",
        "--dst-nodata", "0,0,0",
        "--co", "TILED=YES",
        "--co", "COMPRESS=LZW",
        "--co", "BIGTIFF=IF_SAFER",
        *in_rasters,
        out_tif,
    ]

    run_cmd(cmd)

    info_cmd = [
        gdal_exe,
        "raster",
        "info",
        out_tif,
    ]
    run_cmd(info_cmd)

    elapsed = time.perf_counter() - start_time
    print(f"\nDone. Mosaic written to: {out_tif}")
    print(f"Total runtime: {elapsed:.2f} seconds")
