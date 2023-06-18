import pygame as pg
from pygame.locals import *
from math import ceil


pg.init()
pg.display.set_caption('Line drawer')


# Constants:
displayWidth = 1920
displayHeight = 1080

lineLength = 10
lineWidth = int(lineLength/4)


# Colors:
white = (255,255,255)
black = (0,0,0)
grey = (128,128,128)
lightGrey = (211,211,211)
darkGrey = (105,105,105)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

yellow = (255,255,0)
pink = (255,0,255)
turquoise = (0,255,255)


# Calculated Constants
boardWidth = ceil(displayWidth / lineLength)
boardHeight = ceil(displayHeight / lineLength)

inactiveColor = white # The color of an inactive line
activeColor = black # The color of an active line
isHeatMap = True # True: The pattern will be shown on grey gradient. False: The pattern will be shown black on white.

startingPos = (int(boardWidth / 2), int(boardHeight / 2)) # Where the patternMaker will start.
startingOrientation = 0 # Which way the patternMaker will start out facing. 0 = up, 1 = right, 2 = down, 3 = left

clock = pg.time.Clock()
screen = pg.display.set_mode((displayWidth, displayHeight), RESIZABLE)


class Line:

	def __init__(self, pos1, pos2, heat=inactiveColor):
		self.pos1 = pos1
		self.pos2 = pos2
		self.isActive = False
		self.heat = list(heat)

	def activate(self):
		new_color = []
		for i in self.heat:
			if i >= 25:
				new_i = i - 25
			else:
				new_i = 0
			new_color.append(new_i)
		self.heat = new_color
		self.isActive = True
		self.draw()

	def draw(self):
		if isHeatMap:
			color = self.heat
		elif self.isActive:
			color = activeColor
		else:
			color = inactiveColor
		screen_pos1 = (self.pos1[0] * lineLength, self.pos1[1] * lineLength)
		screen_pos2 = (self.pos2[0] * lineLength, self.pos2[1] * lineLength)
		pg.draw.line(screen, color, screen_pos1, screen_pos2, lineWidth)


class Entity:

	def __init__(self, position, orientation):
		self.position = position
		self.orientation = orientation
		self.flagged = False
		self.iterations = 0

	def turnC(self):
		if self.orientation == 3:
			self.orientation = 0
		else:
			self.orientation += 1

	def turnCC(self):
		if self.orientation == 0:
			self.orientation = 3
		else:
			self.orientation -=1

	def moveForward(self):
		key = ((0, -1), (1, 0), (0, 1), (-1, 0))
		oldPosition = self.position
		change = key[self.orientation]
		self.position = (oldPosition[0] + change[0], oldPosition[1] + change[1])

		for line in lineList:
			if sorted((oldPosition, self.position)) == sorted((line.pos1, line.pos2)):
				if line.isActive:
					self.flagged = True
				else:
					self.flagged = False
				line.activate()

	def advance(self):
		if self.flagged:
			self.moveForward()
		else:
			self.turnC()
			self.moveForward()
		self.iterations += 1


def generateLines(width, height):
	# This function generates a rectangle of lines
	lines = []
	for y in range(height):
		for x in range(width):
			lines.append(Line((x,y), (x + 1, y)))
		for x in range(width + 1):# The '+1' is for the extra line at the end.
			lines.append(Line((x, y), (x, y + 1)))
	for x in range(width):
		lines.append(Line((x, height), (x + 1, height)))
	return lines


def main():
	global isHeatMap
	screen.fill(white)

	for i in lineList:
			i.draw()

	position = startingPos
	orientation = startingOrientation 

	locked = True
	runAutomatically = False
	while locked:

		if runAutomatically:
			patternMaker.advance()

		for event in pg.event.get():
			if event.type == pg.QUIT:
				locked = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					locked = False
				if event.key == pg.K_RETURN:
					patternMaker.advance()
				if event.key == pg.K_SPACE:
					runAutomatically = not runAutomatically
				if event.key == pg.K_TAB:
					isHeatMap = not isHeatMap
					for i in lineList:
						i.draw()

		pg.display.update()
		clock.tick(60)

	pg.quit()

patternMaker = Entity(startingPos, startingOrientation)
lineList = generateLines(boardWidth, boardHeight)
main()