from PIL import Image
import sys

image = Image.open(sys.argv[1])
#image.show()

(w, h) = image.size

allZeros = True

print "Testing if image is blank"
pixels = image.load()
for x in range(w):
    for y in range(h):
        value = pixels[x, y]
        if value != 0:
            allZeros = False

print allZeros

if allZeros:
    print "Using exit status 1. The image is blank."
    exit(1)
else:
    print "Using exit status 0. The image is not blank."
    exit(0)


# References
# http://stackoverflow.com/questions/2181292/using-the-image-point-method-in-pil-to-manipulate-pixel-data

