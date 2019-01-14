import json

#Classe Agent
class Agent:
	def __init__(self, agAttributs):
		for nomAtt, valAtt in agAttributs.items():
			setattr(self, nomAtt, valAtt)

listAgents = []
listAgreeableness = []

fichAgents = open("agents-100k.json")
data = json.load(fichAgents)

for element in data:
 	listAgents.append(Agent(element))
 	listAgreeableness.append(listAgents[-1].agreeableness)

monAgent = listAgents[2]

fichAgents.close()

print(str(monAgent.agreeableness))

