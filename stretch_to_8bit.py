import os
import arcpy
from arcpy.ia import Apply


def stretch_to_8bit(rft: str, inp: str) -> str:
    """
    Apply a Raster Function Template to stretch an input raster and write
    the result to an 8-bit TIFF in the same folder as the input.

    Args:
        rft (str): Path to the Raster Function Template (.rft.xml).
        inp (str): Path to the input raster.

    Returns:
        str: Path to the output raster.
    """
    if not os.path.isfile(rft):
        raise FileNotFoundError(f"Raster Function Template not found: {rft}")

    if not os.path.isfile(inp):
        raise FileNotFoundError(f"Input raster not found: {inp}")

    base, _ = os.path.splitext(inp)
    out = base + "_stretchedXX.tif"

    arcpy.CheckOutExtension("ImageAnalyst")
    arcpy.env.overwriteOutput = True

    print(f"\nApplying stretch .rft to RGB raster:\n{inp}\n")

    src = arcpy.Raster(inp)
    stretched = Apply(src, rft)

    arcpy.management.CopyRaster(
        in_raster=stretched,
        out_rasterdataset=out,
        background_value="0",
        nodata_value="0",
        pixel_type="8_BIT_UNSIGNED",
        scale_pixel_value="ScalePixelValue",
        format="TIFF"
    )

    print(f"\nStretched raster saved to:\n{out}\n")

    return out


if __name__ == "__main__":
    # path to the input RGB raster file (.tif; 16bit)
    input_raster = r"I:\IMAGERY\TCD_Iridimi2_PNEO_08Aug2026\TCD_Iridimi2_PNEO_08Aug2026_RGB.tif"
    # path to .rft STRETCH template
    rft_path = r"E:\MDCS\Parameter\RasterFunctionTemplates\Stretching\ITEM_Stretch_PercMinMax_025_05_Stats_AutoGamma_1_255.rft.xml"

    stretch_to_8bit(rft_path, input_raster)
