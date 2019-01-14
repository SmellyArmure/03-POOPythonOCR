import json

#Classe Agent
class Agent:
	def __init__(self, agreeableness):
		self.agreeableness=agreeableness

listAgent = []
listAgreeableness = []

fichAgents = open("agents-100k.json")
Data = json.load(fichAgents)

for element in Data:
	listAgent.append(Agent(element["agreeableness"]))
	#listAgreeableness.append(element["agreeableness"])
	listAgreeableness.append(listAgent[-1].agreeableness)

fichAgents.close()

somme = sum(listAgreeableness)
total = len(listAgreeableness)
moyenne = somme/total

print(somme)
print(total)
print(moyenne)