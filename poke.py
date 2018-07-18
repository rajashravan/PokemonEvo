import requests
import json
#import pokebase as pb

#chesto = pb.NamedAPIResource('berry', 'chesto')
#print(chesto.name)

#parameters = {"lat": 40.71, "lon" : -74}

#response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)

#print(response.content)

#print(type(data))

#print(response.headers)

#find the evo path of bulbusaur

#pm = pb.evolution_chain(1)
#print(pm.baby_trigger_item)



# Returns 
def getEvo(pokemon):
	# Step 1 - get Species of pokemon
	response = requests.get("https://pokeapi.co/api/v2/pokemon-species/" + pokemon + "/")

	# turn into JSON
	data = response.json()

	# Step 2 - get evolution chain
	name = data["name"]
	evolution_chain_url = data["evolution_chain"]["url"]
	response = requests.get(evolution_chain_url)
	data = response.json()
	evoChain = data["chain"]

	# Get to current pokemon
	while (evoChain["species"]["name"] != name):
		#print(len(evoChain["evolves_to"]))
		#print(evoChain["evolves_to"][0])
		# get next chain link
		evoChain = evoChain["evolves_to"][0]


	# Step 3 - get next evolution
	if (len(evoChain["evolves_to"]) == 0):
		print(name + " is already at max evolution")
		return 
	evo = evoChain["evolves_to"][0]["species"]["name"]
	print(name + " evolves into " + evo)
	return evo


pm_name = raw_input("Please enter your Pokemon's name or ID: ")
getEvo(pm_name)






