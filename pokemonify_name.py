import jellyfish
from bs4 import BeautifulSoup
import sqlite3
import os.path
# from fuzzywuzzy import fuzz
from operator import itemgetter, attrgetter, methodcaller


def get_pokemons_names():
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

  return pokemons_names_list

def get_all_substrings(input_string, minv, maxv):
  length = len(input_string)
  alist = []
  for j in range(minv, maxv + 1):
    for i in range(length):
      if len(input_string[i:i + j + 1]) >= minv:
        alist.append(input_string[i:i + j + 1])
  return set(alist)

def getDiff(s1, s2):
  return jellyfish.jaro_winkler(s2, s1)
  # return fuzz.ratio(s1, s2)/100

def getInputAndSuggest(uname, print_output = True):
  pokemons_names_list = get_pokemons_names()
  uname = uname.lower()
  uphonic = jellyfish.nysiis(uname)
  best_rep = {}
  for pokemon_name in pokemons_names_list:
    # if not pokemon_name.startswith("cascoon"):
    if len(pokemon_name) < len(uname) + 2:
      continue
    psubs = get_all_substrings(pokemon_name, 2, len(uname))
    similar_subs = []
    best_sub_rep = {}
    for psub in psubs:
      psub_phone = jellyfish.nysiis(psub)
      # print()
      name_diff = getDiff(psub, uname)
      phone_diff = getDiff(psub_phone, uphonic)
      best_sub_rep[name_diff + phone_diff] = [psub, pokemon_name, name_diff, phone_diff]
      # print("psub : ", psub, " psub phone : ", psub_phone, " uname : ", uname, " uphonic : ", uphonic)
      # print("jerro wicker distance names : ", name_diff)
      # print("jerro wicker distance phone : ", phone_diff)
    list_keys = list(best_sub_rep.keys())
    list_keys = sorted(list_keys, reverse=True)[:2]
    for key in list_keys:
      if key > 1.35:
        if key in best_rep:
          best_rep[key].append(best_sub_rep[key])
        else:
          best_rep[key] = [best_sub_rep[key]]

  list_keys = list(best_rep.keys())
  list_keys = sorted(list_keys, reverse=True)[:3]
  best_rep = dict((k, v) for k, v in best_rep.items() if k in list_keys)
  output_res = []
  for list_key in list_keys:
    for rep in best_rep[list_key]:
      output_res.append({'updated_name': rep[1].replace(rep[0], uname),
        'pokemon_name': rep[1], 'similarity': rep[3]})

  output_res = sorted(output_res, key=itemgetter('similarity'), reverse = True)
  if print_output:
    print("Our best suggestions results ::: ")
    for res in output_res:
      print("Nikname : ", res['updated_name'], " Based on pokemon : ",
        res['pokemon_name'], "  rep : ", res)
    print()
  return output_res

# while(1):
#   uname = input("Enter username : ")
#   getInputAndSuggest()