#to-do: make it interactive with the web page so that it'll be an actual project rather than shit  

from flask import Flask, render_template, request, jsonify
from collections import OrderedDict

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# LRU Cache Implementation
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) == self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def get_cache(self):
        return list(self.cache.items())

# Initialize LRU Cache with capacity 3
lru_cache = LRUCache(3)

# API to get a value
@app.route('/get/<int:key>', methods=['GET'])
def get_value(key):
    result = lru_cache.get(key)
    return jsonify({"key": key, "value": result})

# API to put a key-value pair
@app.route('/put', methods=['POST'])
def put_value():
    data = request.json
    key = data['key']
    value = data['value']
    lru_cache.put(key, value)
    return jsonify({"message": "Key-Value pair added", "cache": lru_cache.get_cache()})

# API to get the current cache state
@app.route('/cache', methods=['GET'])
def get_cache():
    return jsonify({"cache": lru_cache.get_cache()})

if __name__ == '__main__':
    app.run(debug=True)
