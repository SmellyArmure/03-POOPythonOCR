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

	# constructeur des objets de classe Zone
	def __init__(self, pt1, pt2):
		self.coin1 = pt1
		self.coin2 = pt2
		self.inhabitants = [] # crée le tableau qui contiendra les habitants

	# affecte à une zone l'agent passé en paramètre
	def affectInhab(self, agent):
		self.inhabitants.append(agent) #met l'agent dans une liste correpondant à la zone

	# vérifie si la position donnée est bien dans l'objet de classe Zone concerné
	def contains(self, posit):
		return posit.longitude >= min(self.coin1.longitude, self.coin2.longitude) and \
		posit.longitude <= max(self.coin1.longitude, self.coin2.longitude) and \
		posit.latitude >= min(self.coin1.latitude, self.coin2.latitude) and \
		posit.latitude <= max(self.coin1.latitude, self.coin2.latitude)

	# initialise la liste de toutes les zones 
	@classmethod
	def init_zones(cls):
		for lati in range(cls.MIN_LAT_DEG, cls.MAX_LAT_DEG, cls.HEIGHT_DEG):
			for longi in range (cls.MIN_LONG_DEG, cls.MAX_LONG_DEG, cls.WIDTH_DEG):
				cls.ZONES.append(Zone(Position(longi, lati), Position(longi+cls.WIDTH_DEG, lati+cls.HEIGHT_DEG)))

	# assigne les habitants à leur zone (renvoie la zone concernée)
	@classmethod
	def ZoneInhab(cls,position):
		#utilise la position de l'agent donnée (degrés) et calcule le compteur de chaque boucle
		index_long = int((position.longitude - cls.MIN_LONG_DEG) // cls.WIDTH_DEG)
		index_lat = int((position.latitude - cls.MIN_LAT_DEG) // cls.HEIGHT_DEG)
		#calcule l'index dans la liste Zone.ZONES[]
		index = int((index_lat * ((cls.MAX_LONG_DEG - cls.MIN_LONG_DEG) // cls.WIDTH_DEG)) + index_long)
		theZone = cls.ZONES[index]
		assert theZone.contains(position) # vérifie que la position est bien dans la zone trouvée
		return theZone # renvoie la zone
##############################################################""
#Initialisation des variables
listAgents = []
##############################################################""
#Fonction main
def main():
	Zone.init_zones() #initialise les zones (attribut de classe : liste ZONES)
	#boucle sur les agents
	ind = 0
	for dico in json.load(open("agents-100k.json")): #boucle sur les éléments (dictionnaires) qui constitueront les agents
		ind += 1
		pos = Position(dico.pop("longitude"),dico.pop("latitude")) #récupère la position de l'agent
		agent = Agent(pos,**dico) # crée l'agent selon sa position et les attributs du dictionnaire
		listAgents.append(agent) # ajoute l'agent crée à la liste
		zone = Zone.ZoneInhab(agent.position) 
		zone.affectInhab(agent) # affecte l'agent dans sa zone
	rep = int(input("numéro d'agent ? "))
	print("l'agent n°" + str(rep) + " est situé à la position (" + str(listAgents[rep].position.longitude) \
		+ "," + str(listAgents[rep].position.latitude) + ").")
	repZone = Zone.ZoneInhab(listAgents[rep].position)
	lat_c1 = repZone.coin1.latitude
	lat_c2 = repZone.coin2.latitude
	long_c1 = repZone.coin1.longitude
	long_c2 = repZone.coin2.longitude
	print("Il est contenu dans la zone délimitée par (" + str(long_c1) + "," + str(lat_c1) + ") et (" + str(long_c2) + "," + str(lat_c2) + ").")

main()

	

