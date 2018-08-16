from flask import Flask, render_template, url_for
from data import Articles
import requests
import json
app = Flask(__name__)

Articles = Articles()

#Pokemon Object to make sending data to front end easier
class Pokemon:
	def __init__(self):
		self.weight = 0
		self.stats = {} # dictionary for stats
		self.moves = [] # list for moves


@app.route("/articles")
def articles():
	return render_template('articles.html', articles = Articles)


@app.route("/")
def noPoke():
	return render_template('noPoke.html')

@app.route("/<pokemon>")	
def getEvo(pokemon):

	#attributes dict to store 

	# get sprite of given pokemon
	response = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon + "/")
	data = response.json()
	poke_URL = data["sprites"]["front_default"]

	#build pokemon object
	poke = Pokemon()
	poke.weight = data["weight"]

	#build stats dict
	stats = data["stats"]
	for stat in stats:
		#Speed
		if (stat["stat"]["name"] == "speed"):
			poke.stats["speed"] = stat["base_stat"]
		#SpDef
		if (stat["stat"]["name"] == "special-defense"):
			poke.stats["special-defense"] = stat["base_stat"]
		#SpAttack
		if (stat["stat"]["name"] == "special-attack"):
			poke.stats["special-attack"] = stat["base_stat"]
		#Defense
		if (stat["stat"]["name"] == "defense"):
			poke.stats["defense"] = stat["base_stat"]
		#Attack
		if (stat["stat"]["name"] == "attack"):
			poke.stats["attack"] = stat["base_stat"]
		#HP
		if (stat["stat"]["name"] == "hp"):
			poke.stats["hp"] = stat["base_stat"]

	#build moves list
	moves = data["moves"]
	for move in moves:
		poke.moves.append(move["move"]["name"])


	# Step 1 - get Species of pokemon
	response = requests.get("https://pokeapi.co/api/v2/pokemon-species/" + pokemon + "/")

	# turn into JSON
	data = response.json()

	#stats list


	#flavor text
	flavor_text_entries = data["flavor_text_entries"]
	flavor_text = None

	#get english flavor text
	for entry in flavor_text_entries:
		lang = entry["language"]["name"]
		if (lang == "en"):
			flavor_text = entry["flavor_text"]
			break

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


	# get a list of the next evolutions, stored as dict (name and url)
	evo_list = []

	#check if final/no evolution
	'''
	deprecated - code has been updated to be more robust and only have one endpoint
	if (len(evoChain["evolves_to"]) == 0):
		print(name + " is already at max evolution")
		return render_template('evo.html', poke = pokemon.capitalize(), 
			poke_URL = poke_URL, flavor_text = flavor_text)
	'''

	#else, get all the evos and sprite links
	while(len(evoChain["evolves_to"]) != 0): #we know we start with atleast one
		evo_name = evoChain["evolves_to"][0]["species"]["name"] #evo name
		#get sprite url
		response = requests.get("https://pokeapi.co/api/v2/pokemon/" + evo_name)
		data = response.json()
		evo_url = data["sprites"]["front_default"]
		#make dict
		evo_entry = {}
		evo_entry["name"] = evo_name.capitalize()
		evo_entry["url"] = evo_url.capitalize()
		evo_list.append(evo_entry)
		print(name + " evolves into " + evo_name + " with link " + evo_url)
		evoChain = evoChain["evolves_to"][0]

	#evo = evoChain["evolves_to"][0]["species"]["name"]
	#print(name + " evolves into " + evo)

	'''
	# Step 4 - get sprite of next evolution
	response = requests.get("https://pokeapi.co/api/v2/pokemon/" + evo)
	data = response.json()
	evo_URL = data["sprites"]["front_default"]
	print(evo_URL)
	'''
	#return evo
	return render_template('evo.html', poke = poke, name = name.capitalize(), 
		flavor_text = flavor_text, poke_URL = poke_URL, evo_list = evo_list)

if __name__ == '__main__':
	app.run(debug=True)


