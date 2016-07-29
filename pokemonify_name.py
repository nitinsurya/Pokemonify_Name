import jellyfish
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import os.path


pokemons_names_list = []
dir_path = os.path.dirname(os.path.realpath(__file__))
if os.path.isfile(dir_path + "/" + 'pokemons.db'):
  conn = sqlite3.connect('pokemons.db')
  c = conn.cursor()

  for row in c.execute('''select name from pokemons'''):
    pokemons_names_list.append(row[0])
else:
  conn = sqlite3.connect('pokemons.db')
  c = conn.cursor()

  c.execute('''CREATE TABLE pokemons (pid text, name text, CONSTRAINT id_unique UNIQUE (pid))''')

  page = open("pokemonify_name.html").read()
  parsed_html = BeautifulSoup(page, 'html.parser')
  pokemons_list = []

  for tr_one in parsed_html.tbody.find_all("tr"):
    pid = tr_one.find_all("td")[0].get_text().strip()
    pname = tr_one.find_all("td")[1].get_text().lower().strip().splitlines()[0].replace("\'", "\\'")
    try:
      c.execute("INSERT INTO pokemons VALUES (\"" + pid + "\", \"" + pname + "\")")
    except:
      continue
    pokemons_names_list.append(pname)

  conn.commit()
  conn.close()

def get_all_substrings(input_string, minv, maxv):
  length = len(input_string)
  alist = []
  for j in range(minv, maxv + 1):
    for i in range(length):
      if len(input_string[i:i + j + 1]) >= minv:
        alist.append(input_string[i:i + j + 1])
  return set(alist)

while(1):
  uname = input("Enter username : ")
  uphonic = jellyfish.nysiis(uname)
  best_rep = {}
  for pokemon_name in pokemons_names_list:
    # if not pokemon_name.startswith("bulb"):
    if len(pokemon_name) < len(uname) + 2:
      continue
    psubs = get_all_substrings(pokemon_name, 3, len(uname))
    similar_subs = []
    best_sub_rep = {}
    for psub in psubs:
      psub_phone = jellyfish.nysiis(psub)
      # print()
      name_diff = jellyfish.jaro_winkler(psub, uname)
      phone_diff = jellyfish.jaro_winkler(psub_phone, uphonic)
      best_sub_rep[name_diff + phone_diff] = [psub, pokemon_name, name_diff, phone_diff]
      # print("psub : ", psub, " psub phone : ", psub_phone, " uname : ", uname, " uphonic : ", uphonic)
      # print("jerro wicker distance names : ", name_diff)
      # print("jerro wicker distance phone : ", phone_diff)
    list_keys = list(best_sub_rep.keys())
    list_keys = sorted(list_keys, reverse=True)[:2]
    for key in list_keys:
      if key > 1.3:
        if key in best_rep:
          best_rep[key].append(best_sub_rep[key])
        else:
          best_rep[key] = [best_sub_rep[key]]

  list_keys = list(best_rep.keys())
  list_keys = sorted(list_keys, reverse=True)[:3]
  best_rep = dict((k, v) for k, v in best_rep.items() if k in list_keys)
  print("Our best suggestions results ::: ")
  for list_key in list_keys:
    for rep in best_rep[list_key]:
      print("Nikname : ", rep[1].replace(rep[0], uname), " Based on pokemon : ", rep[1], "  rep : ", rep)
  print()