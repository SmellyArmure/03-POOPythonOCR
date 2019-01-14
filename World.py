import json
import math

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
		self._long_rad = self.longitude*math.pi/180
		return self._lat_rad
	
	@property
	def lat_rad(self):
		self._lat_rad = self.latitude*math.pi/180
		return self._lat_rad

#Initialisation des variables
listAgents = []

#Fonction main
def main():
	for dico in json.load(open("agents-100k.json")):
 		pos = Position(dico.pop("longitude"),dico.pop("latitude"))
 		listAgents.append(Agent(pos,**dico))
 		
main()

monAgent = listAgents[2]
print(monAgent.position.latitude)
print(monAgent.position.lat_rad)
