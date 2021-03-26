import json
from pprint import pprint

filename = 'movies.json'
with open(filename) as f:
    print(len(json.loads(f.read())))
