from visual import *
from PIL import Image

#path = "c:/proj/orbital-2/jsorrery-master/img/new"
#path = "c:/proj/orbital-2/V2.0/img"
path = "c:/proj/orbital/new images"
pathOut = "c:/proj/orbital/img"
#TGAarrayIn = ["sunmapalpha2k","jupiter2k","earth2k","mercurymap2k","moon2k","neptune2k","saturn2k","pluto-grey2k","uranus1k","venus2k", "mars2k","eris2k","makemake2k","haumea2k","sedna2k", "asteroidmap2k"]
#TGAarrayOut = ["sun","jupiter","earth","mercury","moon","neptune","saturn","pluto","uranus","venus", "mars","eris","makemake","haumea","sedna","asteroid"]
#TGAarrayIn = ["8k_earth_daymap"]
#TGAarrayOut = ["earthnocloud"]
TGAarrayIn = ["FH2stage"]
TGAarrayOut = ["FH2S"]

width = 4096 #2048 # must be power of 2
height = 2048 #1024 # must be power of 2

for i in range (0, len(TGAarrayIn), 1):
	nameIn = path+"/"+TGAarrayIn[i]

	print nameIn + ".jpg"
	im = Image.open(nameIn + ".jpg")
	print(im.size) # optionally, see size of image

	# Optional cropping:
	#im = im.crop((x1,y1,x2,y2)) # (0,0) is upper left

	im = im.resize((width,height), Image.ANTIALIAS)
	materials.saveTGA(pathOut+"/"+TGAarrayOut[i], im)
