import json
import math
import random

#Classe Agent
class Agent:
	def __init__(self, position, **agAttributs):
		for nomAtt, valAtt in agAttributs.items():
			setattr(self, nomAtt, valAtt)
			self.position = position

#Classe Position
class Position:
	def __init__(self, longi, lati):
		self.longitude = longi
		self.latitude = lati

	@property
	def long_rad(self):
		return self.longitude*math.pi/180
	
	@property
	def lat_rad(self):
		return self.latitude*math.pi/180

#Classe Zone
class Zone:

	ZONES=[]
	MIN_LAT_DEG = -90
	MAX_LAT_DEG = 90
	MIN_LONG_DEG = -180
	MAX_LONG_DEG = 180
	WIDTH_DEG = 1
	HEIGHT_DEG = 1

	def __init__(self, coin1, coin2):
		self.coin1 = coin1
		self.coin2 = coin2

	@classmethod
	def init_zones(cls):
		for lati in range(cls.MIN_LAT_DEG, cls.MAX_LAT_DEG, cls.HEIGHT_DEG):
			for longi in range (cls.MIN_LONG_DEG, cls.MAX_LONG_DEG, cls.WIDTH_DEG):
				cls.ZONES.append(Zone(Position(longi, lati), Position(longi+cls.WIDTH_DEG, lati+cls.HEIGHT_DEG)))

#Initialisation des variables
listAgents = []

##############################################################""
#Fonction main
def main():
	Zone.init_zones() #initialise les zones (attribut de classe : liste ZONES)
	for dico in json.load(open("agents-100k.json")):
		pos = Position(dico.pop("longitude"),dico.pop("latitude"))
		listAgents.append(Agent(pos,**dico))
	
main()
print(Zone.ZONES[50].coin1.lat_rad)
	

