from PIL import Image
import sys
import os
import shutil
import re

src = sys.argv[1]
dest = sys.argv[2]

def isBlank(filename):

    image = Image.open(filename)
    #image.show()
    
    (w, h) = image.size
    
    allZeros = True


    print filename
    print "Testing if image is blank"
    pixels = image.load()
    for x in range(w):
        for y in range(h):
            value = pixels[x, y]
            if value != 0:
                allZeros = False

    print allZeros
    return allZeros



def getImageFiles(directory):

    results = []

    src_files = os.listdir(directory)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if (os.path.isfile(full_file_name)):
            lowercase_full_file_name = full_file_name.lower()
            if re.search('.tif', lowercase_full_file_name) or re.search('.tiff', lowercase_full_file_name) or re.search('.png', lowercase_full_file_name) or re.search('.bmp', lowercase_full_file_name):
                results += [full_file_name]

    return results



fileList = getImageFiles(src)


for full_file_name in fileList:
    if not(isBlank(full_file_name)):
        print "copying", full_file_name, "to", dest
        shutil.copy(full_file_name, dest)



# References
# http://stackoverflow.com/questions/2181292/using-the-image-point-method-in-pil-to-manipulate-pixel-data

