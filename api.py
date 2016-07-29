#!flask/bin/python

from flask import Flask, request, send_from_directory, jsonify, make_response, abort
import os
import pokemonify_name as pn

app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/js/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.realpath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static', 'js'), filename)

@app.route('/get_names', methods=['GET'])
def get_names():
  uname = request.args.get('uname')
  out_vals = pn.getInputAndSuggest(uname, False)
  print(out_vals)
  # pokemons_names_list = pn.get_pokemons_names()
  return make_response(jsonify(out_vals))

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
  app.run(debug=True)