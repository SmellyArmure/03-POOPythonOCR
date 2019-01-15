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
	WIDTH_DEG = 10
	HEIGHT_DEG = 10

	def __init__(self, coin1, coin2):
		self.coin1 = coin1
		self.coin2 = coin2

	@classmethod
	def init_zones(cls):
		for lati in range(cls.MIN_LAT_DEG, cls.MAX_LAT_DEG, cls.HEIGHT_DEG):
			for longi in range (cls.MIN_LONG_DEG, cls.MAX_LONG_DEG, cls.WIDTH_DEG):
				cls.ZONES.append(Zone(Position(longi, lati), Position(longi+cls.WIDTH_DEG, lati+cls.HEIGHT_DEG)))

##############################################################""
#Fonction permettant d'assigner les habitants à leur zone
def indexZoneInhab(agent):
	#récupère la position de l'agent (degrés) et calcule le compteur de chaque boucle
	index_long = int((agent.position.longitude - Zone.MIN_LONG_DEG) // Zone.WIDTH_DEG)
	index_lat = int((agent.position.latitude - Zone.MIN_LAT_DEG) // Zone.HEIGHT_DEG)
	#calcule l'index dans la liste Zone.ZONES[]
	index = int((index_lat * ((Zone.MAX_LONG_DEG - Zone.MIN_LONG_DEG) // Zone.WIDTH_DEG)) + index_long)
	return (index, (index_long, index_lat))

##############################################################""
#Initialisation des variables
listAgents = []
##############################################################""
#Fonction main
def main():
	Zone.init_zones() #initialise les zones (attribut de classe : liste ZONES)
	for dico in json.load(open("agents-100k.json")): #boucle sur les éléments (dictionnaires) qui constitueront les agents
		pos = Position(dico.pop("longitude"),dico.pop("latitude")) #récupère la position des agents
		listAgents.append(Agent(pos,**dico)) #passe en attribut la position des agents, crée les attributs selon le dictionnaire
	ind = int(input("indice d'un agent ?"))
	ind_zone = indexZoneInhab(listAgents[int(ind)])[0]
	print("les coord de l'agent n°" + str(ind) + " sont :\n (" + str(listAgents[ind].position.longitude) + "," + str(listAgents[ind].position.latitude) + ").")
	print("la zone n°" + str(ind_zone) + " est définie par les points de coordonnées :\n(" + str(Zone.ZONES[ind_zone].coin1.longitude) + "," + str(Zone.ZONES[ind_zone].coin1.latitude) + ") et ("+ str(Zone.ZONES[ind_zone].coin2.longitude) + "," + str(Zone.ZONES[ind_zone].coin2.latitude) + ").")
	print("(Remarque : les indices long et lat sont " + str(indexZoneInhab(listAgents[int(ind)])[1]) + ".)")

main()

	

