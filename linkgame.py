from linker import Linker
from PIL import Image as img, ImageDraw as drawer
import os

box_size = 0
bar_size = 0
bg_color = None
box_color = None
# x1,y1 x2,y2
map_range = [20,350,1060,1220]

# get map
# start 20,350 -> 1060 1220
def analyze(timg):
	def __isfamiler(rgb1, rgb2, threshold=5):
		for i in len(rgb1):
			if abs(rgb1[i]-rgb2[i]) > threshold:
				return False
		return True
	# know box size and bg_color
	def __base_scan(timg):
		bg_color = timg.getpixel((map_range[0],map_range[1]))
		# box is grey, then r==g==b
		def __isbox(rgb):
			return rgb[0] == rgb[1] and rgb[1] == rgb[2]
		_size = 0
		for _y in xrange(map_range[1],map_range[3]):
			for _x in range(map_range[0],map_range[2]):
				if __isbox(timg.getpixel((_x,_y))):
					_size += 1
				elif _size > 0:
					if _size < 50:
						_size = 0
						continue
					box_size = _size
					box_color = timg.getpixel((_x-2,_y))
					print("box size is : ",_size)
					print("box color is : ",box_color)
					map_range[1] = _y
					break
			if box_size > 0:
				break

		# get range
		for _y in range():
			pass
			pass
		
	if not box_color:
		__base_scan(timg)

im = img.open("2.png").convert("RGB")
analyze(im)
