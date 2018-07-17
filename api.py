import requests
import json
import pokebase as pb

#chesto = pb.NamedAPIResource('berry', 'chesto')
#print(chesto.name)

#parameters = {"lat": 40.71, "lon" : -74}

#response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)

#print(response.content)

#print(type(data))

#print(response.headers)

#find the evo path of bulbusaur

pm = pb.evolution_chain(1)
#print(pm.baby_trigger_item)

pm_name = "bulbasaur"


# Step 1 - get Species of pokemon 
response = requests.get("https://pokeapi.co/api/v2/pokemon-species/" + pm_name + "/")

# turn into JSON
data = response.json()

# Step 2 - get evolution chain
evolution_chain_url = data["evolution_chain"]["url"]
response = requests.get(evolution_chain_url)
data = response.json()

# Step 3 - get next evolution

print(data["chain"]["evolves_to"][0]["species"]["name"])






