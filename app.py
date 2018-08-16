from flask import Flask, render_template, url_for
from data import Articles


import requests
import json
app = Flask(__name__)

Articles = Articles()

@app.route("/articles")
def articles():
	return render_template('articles.html', articles = Articles)


@app.route("/")
def noPoke():
	print("sdf")
	print(url_for('getEvo', pokemon='squirtle'))
	return render_template('noPoke.html')

@app.route("/<pokemon>")	
def getEvo(pokemon):

	# get sprite of given pokemon
	response = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon + "/")
	data = response.json()
	poke_URL = data["sprites"]["front_default"]

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


	# get a list of the next evolutions
	evo_list = []
	evo_urls = []
	# Step 3 - get next evolution

	#check if final/no evolution
	if (len(evoChain["evolves_to"]) == 0):
		print(name + " is already at max evolution")
		return render_template('evo.html', poke = pokemon.capitalize(), poke_URL = poke_URL)

	#else, get all the evos and sprite links
	while(len(evoChain["evolves_to"]) != 0): #we know we start with atleast one
		evo_list.append(evoChain["evolves_to"][0]["species"]["name"]) #evo name
		#get sprite url
		response = requests.get("https://pokeapi.co/api/v2/pokemon/" + evo_list[-1])
		data = response.json()
		evo_urls.append(data["sprites"]["front_default"])
		print(name + " evolves into " + evo_list[-1] + " with link " + evo_urls[-1])
		evoChain = evoChain["evolves_to"][0]

	#evo = evoChain["evolves_to"][0]["species"]["name"]
	#print(name + " evolves into " + evo)
	evo = evo_list[0]

	# Step 4 - get sprite of next evolution
	response = requests.get("https://pokeapi.co/api/v2/pokemon/" + evo)
	data = response.json()
	evo_URL = data["sprites"]["front_default"]
	print(evo_URL)
	#return evo
	return render_template('evo.html', poke = name.capitalize(), evo = evo.capitalize(), 
		poke_URL = poke_URL, evo_URL = evo_URL, evo_list = evo_list)

if __name__ == '__main__':
	app.run(debug=True)