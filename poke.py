import requests
import json
from flask import Flask 


# Returns the name (string) of the evolution of the given pokemon
# Side effect: Prints evolution statement
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

	# Step 4 - get sprite of next evolution
	response = requests.get("https://pokeapi.co/api/v2/pokemon/" + evo)
	data = response.json()
	spriteURL = data["sprites"]["front_default"]
	print(spriteURL)
	return evo


pm_name = input("Please enter your Pokemon's name or ID: ")
getEvo(pm_name)





	



