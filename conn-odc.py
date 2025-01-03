import datacube
import rasterio

dc = datacube.Datacube(app="my_analysis")

with rasterio.Env(AWS_NO_SIGN_REQUEST="YES"):
    ds = dc.load(product="ga_ls9c_ard_3",
                 measurements=["nbart_blue"],
                 limit=1)
    print(ds)