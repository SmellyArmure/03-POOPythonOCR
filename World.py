class Agent:
	def __init__(self, agreeableness):
		self.agreeableness=agreeableness

first_agent = Agent(1.5)

print("l'agréabilité de l'agent est : " + str(first_agent.agreeableness))