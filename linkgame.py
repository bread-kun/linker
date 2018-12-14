from linker import Linker
from PIL import Image as img, ImageDraw as drawer
import os
import time
from logger import *

W,H = 6,7
size = 108
_startn = (172,368)
startn = (_startn[0]+size//2,_startn[1]+size//2)
endn = (907,1227)
bar = 17
@clocker
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
# see a path on res img
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
			# timg.save("res.png")
			_reli.pop()
			return _reli
		_paint.line((_cur[0]*(size+bar)+startn[0], _cur[1]*(size+bar)+startn[1], _pre[0]*(size+bar)+startn[0], _pre[1]*(size+bar)+startn[1]),fill=128)
import io
@clocker
def buildscript(reslist):
	script_file = "mksc.mk"
	i = 1
	with io.open(script_file,"wt",1024,"utf-8") as writer:
		writer.writelines("count= 36\nspeed= 0.2\nstart data >>\nUserWait(5)\n")
		writer.flush()
		while i < len(reslist):
			writer.writelines("Drag({x1}, {y1}, {x2}, {y2}, 150)\n".format(x1=reslist[i-1][0]*(size+bar)+startn[0],y1=reslist[i-1][1]*(size+bar)+startn[1],x2=reslist[i][0]*(size+bar)+startn[0],y2=reslist[i][1]*(size+bar)+startn[1]))
			i += 1
		writer.flush()
	return script_file

def mainf():
	im = img.open("screenshot.png").convert("RGB")
	_head,_blocks = buildmap(im)
	l = Linker(W,H)
	l.sethead(_head)
	for blk in _blocks:
		l.setblock(blk)
	end = l.link()
	l.show()
	print(end)
	return view(im,l,end)
@clocker
def getscreenshot():
	os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
	os.system("adb pull /sdcard/screenshot.png .")
@clocker
def sendlink(reli):
	_sc = buildscript(reli)
	os.system("adb push %s sdcard" %_sc)
	os.system('adb shell "monkey -f /sdcard/%s 1"' %_sc)
	pass
_e = "#"
# 5 click 925,658 + next
# next 555,1600
mcount = int(input("count level:"))
@clocker
def loop(count):
	count = count%5
	getscreenshot()
	reli = mainf()
	reli.reverse()
	# simplify, tap to swip, rali list to conner list
	i = 0
	while True:
		if i+2 >= len(reli):
			break
		# leave conner node
		if (reli[i][0] == reli[i+1][0] and reli[i+1][0] == reli[i+2][0]) or (reli[i][1] == reli[i+1][1] and reli[i+1][1] == reli[i+2][1]):
			reli.pop(i+1)
			continue
		i += 1
	sendlink(reli)
	if count is 0:
		time.sleep(1)
		os.system('adb shell "input tap 923 662"')
		# os.system('cls')
	count += 1
		
	# next
	os.system('adb shell "input tap 555 1600"')
	time.sleep(0.1)
	return count

while True:
	mcount = loop(mcount)