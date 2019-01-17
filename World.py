import json
import math
import random
import matplotlib.pyplot as plt

##############################################################""
# Diverses fonctions générales

def rad_in_km(angle_rad): # convertit un angle en radians en kms
		return angle_rad*Zone.R_EARTH

def trie_xy(xy_tuple): # met les deux tableaux dans l'ordre des x croissants
	x_val = xy_tuple[0]
	y_val = xy_tuple[1]
	assert len(x_val) == len(y_val) # s'assure que les deux tableaux sont de même longueur
	coord = [(x_val[i],y_val[i]) for i in range(0,len(x_val))] # crée un tableau de tuples coordonnées
	coord.sort() # trie (écrase) le tableau selon les valeurs de x
	new_x = [c[0] for c in coord] # reconstitue une liste triée des x
	assert all(new_x[i] <= new_x[i+1] for i in range(len(new_x)-1)) # vérifie que new_x est bien dans l'ordre croissant
	new_y = [c[1] for c in coord] # reconstitue une liste des y triée selon les x
	return (new_x, new_y) # retourne un tuple qui contient les deux nouveaux tableaux
  # on serait pas obligés de passer par un tuple pour renvoyer les infos... à vérifier

##############################################################""
# Les Classes

# Classe Agent
class Agent:
	def __init__(self, position, **agAttributs):
		for nomAtt, valAtt in agAttributs.items():
			setattr(self, nomAtt, valAtt)
			self.position = position

# Classe Position
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

# Classe Zone
class Zone:

	ZONES=[]
	R_EARTH = 6371
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

	@property
	def area(self): # calcule l'aire en km d'une zone à partir des longitudes et latitudes en radians
		return abs(rad_in_km(self.coin1.long_rad-self.coin2.long_rad) *\
			rad_in_km(self.coin1.long_rad-self.coin2.long_rad))

	@property
	def popul(self): # retourne le nombre d'habitants d'une zone
		return len(self.inhabitants)

	@property
	def pop_dens(self): # retourne la densité de population
		return self.popul / self.area
	
	@property
	def mean_agr(self): # calcule et retourne l'agréabilité moyenne d'une zone
		if self.popul == 0:
			return 0
		else:
			return sum([agent.agreeableness for agent in self.inhabitants])/self.popul #List Comprehension
			# [ <1> <2> ] : crée un tableau en exécutant l'opération <1> dans la boucle <2>.
			# somme tous les éléments du tableau, et divise par le nbe d'habitants
	
	@property
	def mean_age(self): # calcule et retourne l'âge moyen dans une zone
		if self.popul == 0:
			return 0
		else:
			return sum([agent.age for agent in self.inhabitants])/self.popul #List Comprehension

	@property
	def mean_inc(self): # calcule et retourne l'âge moyen dans une zone
		if self.popul == 0:
			return 0
		else:
			return sum([agent.income for agent in self.inhabitants])/self.popul #List Comprehension

	@classmethod
	def _init_zones(cls): # initialise la liste de toutes les zones 
		for lati in range(cls.MIN_LAT_DEG, cls.MAX_LAT_DEG, cls.HEIGHT_DEG):
			for longi in range (cls.MIN_LONG_DEG, cls.MAX_LONG_DEG, cls.WIDTH_DEG):
				cls.ZONES.append(Zone(Position(longi, lati), Position(longi+cls.WIDTH_DEG, lati+cls.HEIGHT_DEG)))

	# assigne les habitants à leur zone (renvoie la zone concernée)
	@classmethod
	def zoneInhab(cls,position):
		if not cls.ZONES: # au cas où la liste des zones n'existerait pas encore (ZONES serait égal à [])
			cls._init_zones() #initialise les zones (attribut de classe : liste ZONES)
		#utilise la position de l'agent donnée (degrés) et calcule le compteur de chaque boucle
		index_long = int((position.longitude - cls.MIN_LONG_DEG) // cls.WIDTH_DEG)
		index_lat = int((position.latitude - cls.MIN_LAT_DEG) // cls.HEIGHT_DEG)
		#calcule l'index dans la liste Zone.ZONES[]
		index = int((index_lat * ((cls.MAX_LONG_DEG - cls.MIN_LONG_DEG) // cls.WIDTH_DEG)) + index_long)
		theZone = cls.ZONES[index]
		assert theZone.contains(position) # vérifie que la position est bien dans la zone trouvée
		return theZone # renvoie la zone

	# affecte à une zone l'agent passé en paramètre
	def affectInhab(self, agent):
		self.inhabitants.append(agent) #met l'agent dans une liste correpondant à la zone

	# vérifie si la position donnée est bien dans l'objet de classe Zone concerné
	def contains(self, posit):
		return posit.longitude >= min(self.coin1.longitude, self.coin2.longitude) and \
		posit.longitude <= max(self.coin1.longitude, self.coin2.longitude) and \
		posit.latitude >= min(self.coin1.latitude, self.coin2.latitude) and \
		posit.latitude <= max(self.coin1.latitude, self.coin2.latitude)

# Classes Graphes
class BaseGraph:
	
	def __init__(self): # sert seulement à réunir les choses qui seront requises pour l'affichage
		self.title = ("TITRE")
		self.x_lab = ("AXE X")
		self.y_lab = ("AXE Y")
		self.sh_grid = True
	
	def xy_val(self, zones): # fonction qui est là juste pour spécifier que les classes filles devraient toutes comporter cette fonction
		raise NotImplementedError 

	def show(self, zones):
		sorted_xy = trie_xy(self.xy_val(zones))
		plt.plot(sorted_xy[0], sorted_xy[1], '-')
		#plt.plot(self.xy_val(zones)[0], self.xy_val(zones)[1], '.') # données non triées
		plt.xlabel(self.x_lab)
		plt.ylabel(self.y_lab)
		plt.title(self.title)
		plt.grid(self.sh_grid)
		plt.show()

class AgreeaGraph(BaseGraph):
	
	def __init__(self):
		super().__init__() # exécute quand même l'initialisation de la classe mère (attributs non overridés)
		self.title = "-- EST-ON PLUS GENTILS A LA CAMPAGNE ? --"
		self.x_lab = "Densité de population (hab/km carré)"
		self.y_lab = "Agréabilité moyenne des habitants (-2 à +2)"
		# seul self.sh_grid reste à la valeur par défaut True
	
	def xy_val(self, zones): # agréabilité moyenne en fonction de la densité de population
		x_val = [z.pop_dens for z in zones] # toutes les densités de population (liste dans l'ordre des zones)
		y_val = [z.mean_agr for z in zones] # agréabilité moyenne
		return (x_val, y_val)

class IncGraph(BaseGraph):
	
	def __init__(self):
		super().__init__() # exécute quand même l'initialisation de la classe mère (attributs non overridés)
		self.title = "-- EST-ON PLUS RICHE EN VIEILLISSANT ? --"
		self.x_lab = "Age moyen sur les zones"
		self.y_lab = "Revenu moyen sur les zones"
		# seul self.sh_grid reste à la valeur par défaut True

	def xy_val(self, zones): # revenu moyen en fonction de l'âge
		x_val = [z.mean_age for z in zones] # toutes les densités de population (liste dans l'ordre des zones)
		y_val = [z.mean_inc for z in zones] # agréabilité moyenne
		return (x_val, y_val)

##############################################################""
#Initialisation des variables
listAgents = []
##############################################################""
#Fonction main
def main():
	#boucle sur les agents
	for dico in json.load(open("agents-100k.json")): #boucle sur les éléments (dictionnaires) qui constitueront les agents
		pos = Position(dico.pop("longitude"),dico.pop("latitude")) #récupère la position de l'agent
		agent = Agent(pos,**dico) # crée l'agent selon sa position et les attributs du dictionnaire
		listAgents.append(agent) # ajoute l'agent crée à la liste
		zone = Zone.zoneInhab(agent.position) # trouve la zone correspondant à la position de l'agent
		zone.affectInhab(agent) # affecte l'agent dans sa zone
	mon_graphe_1 = AgreeaGraph()
	mon_graphe_1.show(Zone.ZONES)
	mon_graphe_2 = IncGraph()
	mon_graphe_2.show(Zone.ZONES)

main()

	

