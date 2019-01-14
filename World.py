import json

#Classe Agent
class Agent:
	def __init__(self, **agAttributs):
		for nomAtt, valAtt in agAttributs.items():
			setattr(self, nomAtt, valAtt)

listAgents = []
listAgreeableness = []

def main():
	for dico in json.load(open("agents-100k.json")):
 		listAgents.append(Agent(**dico))
 		listAgreeableness.append(listAgents[-1].agreeableness)

main()

monAgent = listAgents[2]
print(str(monAgent.agreeableness))

