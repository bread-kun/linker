class Linker():
	"""for a minigame linker to link all null box by one line
	:param map size by width and height
	"""
	NULL,BLOCK,HEAD = -3,-2,-1
	def __init__(self, width, height):
		self.__set_map__(width,height)
	def reset(self, width=None, height=None):
		if width and height:
			del self.map
			return self.__set_map__(width,height)
		self.__set_map__(self.width,self.height)

	def __set_map__(self, width, height):
		self.WIDTH,self.HEIGHT = width,height
		self.map = [Linker.NULL for i in range(width*height)]

	def setpos(self, pos, value):
		# xy or idx
		if type(pos) is tuple:
			self.map[pos[0]+pos[1]*self.WIDTH] = value
			return value
		if type(pos) is int:
			self.map[pos] = value
			return value
	def getpos(self,pos):
		# idx
		if type(pos) is int:
			return self.map[pos]
		# xy
		if type(pos) is tuple:
			return self.map[pos[0]+pos[1]*self.WIDTH]
	def setblock(self,*xys):
		for xy in xys:
			self.setpos(xy, Linker.BLOCK)
	def sethead(self, headxy):
		# xy
		self.head = headxy
		self.setpos(headxy,Linker.HEAD)

	def idx2xy(self, idx):
		return idx%self.WIDTH,idx//self.WIDTH
	def xy2idx(self, xy):
		return xy[0]+xy[1]*self.WIDTH

	"""main func
	"""
	def link(self):
		# (idx, [path_idx_1,path_idx_2,path_idx_3]), while tuple[1] len is 0 ,then recall
		def __guess(idx,_path):
			guess_stack.append((idx,_path))
			return [guess_stack[-1][1].pop()]

		# return idx and [path] which len is 1
		def __recall(current_idx):
			if len(guess_stack) > 0:
				_cur = current_idx
				while _cur != guess_stack[-1][0]:
					_next = self.getpos(_cur)
					self.setpos(_cur, Linker.NULL)
					_cur = _next
				if len(guess_stack[-1][1]) is 0:
					guess_stack.pop()
					__recall(_cur)
				return self.idx2xy(_cur),[guess_stack[-1][1].pop()]
			print("none of guess_stack")

		_current = self.head
		guess_stack = []
		_path = self._get_path(_current)
		while True:
			while len(_path) is 1:
				self.setpos(_path[0], self.xy2idx(_current))
				_current = self.idx2xy(_path[0])
				_path = self._get_path(_current)
			if self.isover():
				break
			if len(_path) is 0:
				_current,_path = __recall(self.xy2idx(_current))
				continue
			_path = __guess(self.xy2idx(_current),_path)

	def _get_path(self,xy):
		def __find__(xy):
			# [idx]
			_path = []
			_x,_y = xy
			# up
			if _y > 0 and self.getpos((_x,_y-1)) is Linker.NULL:
				_path.append(self.xy2idx((_x,_y-1)))
			# down
			if _y < self.HEIGHT-1 and self.getpos((_x,_y+1)) is Linker.NULL:
				_path.append(self.xy2idx((_x,_y+1)))
			# left
			if _x > 0 and self.getpos((_x-1,_y)) is Linker.NULL:
				_path.append(self.xy2idx((_x-1,_y)))
			# right
			if _x < self.WIDTH-1 and self.getpos((_x+1,_y)) is Linker.NULL:
				_path.append(self.xy2idx((_x+1,_y)))
			return _path
		_cpath = __find__(xy)
		if len(_cpath) > 1:
			for _cpath_idx in _cpath:
				_deep_path = __find__(self.idx2xy(_cpath_idx))
				if len(_deep_path) is 1:
					return [_cpath_idx]
		return _cpath

	def show(self):
		for y in range(self.HEIGHT):
			for x in range(self.WIDTH):
				_v = self.getpos((x,y))
				if _v is Linker.NULL:
					print("  *",end="")
					continue
				if _v is Linker.BLOCK:
					print("   ",end="")
					continue
				print("%3d" %_v, end="")
			print()

	def isover(self):
		for x in self.map:
			if x is Linker.NULL:
				return False
		return True
if __name__ == '__main__':
	l = Linker(6,5)
	l.sethead((5,1))
	l.setblock((2,0),(3,0),(2,2),(1,4),(4,3))
	l.link()
	l.show()

# start 20,350 -> 1060 1220