from linker import Linker
from PIL import Image as img, ImageDraw as drawer
import os
import time

box_size = 0
bar_size = 0
bg_color = None
box_color = None
# x1,y1 x2,y2
map_range = [20,350,1060,1220]

# get map
# start 20,350 -> 1060 1220
"""
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
		for _y in range(1):
			pass
		
	if not box_color:
		__base_scan(timg)
"""
# return head and block
W,H = 6,6
size = 108
_startn = (173,368)
startn = (_startn[0]+size//2,_startn[1]+size//2)
endn = (907,1102)
bar = 17
def buildmap(timg):
	if timg.width != 1080 or timg.height != 1920:
		raise Exception("remote device screen size is not 1080 x 1920")
	_head = None
	_blocks = []
	for iy in range(H):
		for ix in range(W):
			_x,_y = ix*(size+bar)+startn[0],iy*(size+bar)+startn[1]
			r,g,b = timg.getpixel((_x,_y))
			if r+g+b < 65*3:
				_blocks.append((ix,iy))
			elif r is g and g is b:
				continue
			else:
				_head = (ix,iy)
	return _head,_blocks
def view(timg,linker,end):
	_reli = [end]
	# view able draw
	_paint = drawer.Draw(timg)
	_cur = _pre = end
	_pre_idx = 0
	while True:
		_cur = _pre
		_pre_idx = linker.getpos(_cur)
		_pre = linker.idx2xy(_pre_idx)
		_reli.append(_pre)
		if _pre_idx is linker.HEAD:
			timg.save("res.png")
			_reli.pop()
			return _reli
		_paint.line((_cur[0]*(size+bar)+startn[0], _cur[1]*(size+bar)+startn[1], _pre[0]*(size+bar)+startn[0], _pre[1]*(size+bar)+startn[1]),fill=128)


def mainf():
	im = img.open("screenshot.png").convert("RGB")
	_head,_blocks = buildmap(im)
	l = Linker(W,H)
	l.sethead(_head)
	for blk in _blocks:
		l.setblock(blk)
	l.show()
	end = l.link()
	l.show()
	print(end)
	return view(im,l,end)
_e = "#"
# 5 click 925,658 + next
# next 555,1600
# cmd adb shell input tap x1 y1
count = 2
while True:
	os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
	os.system("adb pull /sdcard/screenshot.png .")
	reli = mainf()
	reli.reverse()
	for x,y in reli:
		os.system('adb shell "input tap %d %d"' %(x*(size+bar)+startn[0], y*(size+bar)+startn[1]))
	time.sleep(1)
	count += 1
	if count is 5:
		os.system('adb shell "input tap 925 658"')
		
	# next
	os.system('adb shell "input tap 555 1600"')
	count = count%5