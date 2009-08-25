
import os


from socket import gethostname; hostname = gethostname()
if hostname == "panther":
        driveName = "o:"
        cytosegDataFolder = "c:/shared/cytoseg_data"
        contourOutputTemporaryFolder = "c:/temp/contour_output"

        #defaultPath = "O:\\images\\LFong\\cropped\\8bit_smaller\\"
        #defaultPath = "O:\\images\\LFong\\tif_8bit_partial\\"
        #defaultPath = "O:\\images\\LFong\\tif_8bit_partial\\"
        #defaultPath = "O:\\images\\LFong\\tif_8bit_20_images\\"
        #defaultPath = "O:\\images\\LFong\\tif_8bit_10_images\\"
        #defaultPath = "O:\\images\\denk\\smallcube2\\"
        #defaultPath = "O:\\images\\denk\\smallcube_region2\\"
        #defaultPath = "O:\\images\\denk\\70x70x70_cube\\"
        #defaultPath = "O:\\images\\LFong\\one_file\\8bit\\"
        #defaultPath = "O:\\images\\test_watershed\\"
        #defaultPath = "O:\\images\\test_watershed\\original\\"
        #defaultPath = "I:\\ncmir_data\\caulobacter\\approximately_cubical_volume\\"
        #defaultPath = "O:\\images\\HPFcere_vol\\HPF_rotated_tif\\seg3D\\tifs\\"
        #defaultPath = "O:\\images\\3D-blob-data\\"
        #defaultPath = "O:\\images\\3D-blob-data\\crop\\"
        defaultPath = "O:\\images\\HPFcere_vol\\HPF_rotated_tif\\seg3D\\tifs\\cropped\\"
        #defaultPath = ""
        
        defaultOutputPath = "O:\\temp\\output\\" 


elif hostname == "user-desktop":
        driveName = "/media/blackshiny"
        cytosegDataFolder = "/media/shared/cytoseg_data"
        contourOutputTemporaryFolder = "/home/user/temp/contour_output"

        #defaultPath = "/crbsdata1/rgiuly/input/cb017_NA1000_set2/cropped204x150/"
        defaultPath = "/crbsdata1/rgiuly/input/triple_tilt/cb024/tifs_small/"
        defaultOutputPath = "/home/user/temp/output/"
else:
        defaultTemporaryFolder = os.tempnam()
        os.mkdir(defaultTemporaryFolder)
        driveName = "/folder_not_set/"
        cytosegDataFolder = defaultTemporaryFolder
        contourOutputTemporaryFolder = defaultTemporaryFolder
        defaultPath = "/folder_not_set/"
        defaultOutputPath = defaultTemporaryFolder

