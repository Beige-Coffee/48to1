from collections import Counter
from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
import numpy as np
import pandas as pd
import urllib.parse

app = Flask(__name__,
            static_url_path='') 


@app.route('/', methods=['GET'])
def welcome_page():
    return render_template('index.html')

@app.route('/get_started', methods=['GET'])
def load_get_started():
    return render_template('get_started.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


