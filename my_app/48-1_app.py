import sys
sys.path.append('..')
from collections import Counter
from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
import numpy as np
import pandas as pd
from watson_personality_functions import all_personality_info_to_df
from watson_tone_analyzer_functions import text_to_sentence_analysis

app = Flask(__name__,
            static_url_path='') 


@app.route('/', methods=['GET'])
def welcome_page():
    return render_template('index.html')

@app.route('/research', methods=['GET'])
def load_research():
    return render_template('research.html')

@app.route('/analyze_d3', methods=['GET'])
def load_d3():
    data = pickle.load( open( "/Users/austin/Documents/Knowledge/48:1/my_app/analytical.pkl", "rb" ) )
    doc = pickle.load( open( "/Users/austin/Documents/Knowledge/48:1/my_app/doc.pkl", "rb" ) )
    return render_template('analyze_text_tone.html', data=data, doc=doc)

@app.route('/analyze', methods=['GET', 'POST'])
def load_analyze():
    if request.method == 'POST':
        text = request.form['text']
        if len(text.split()) > 100:
            tone = text_to_sentence_analysis(text)
            personality = all_personality_info_to_df(text)
            with pd.option_context('display.max_colwidth', -1):
                raw_tone_table = tone.to_html(classes='table table-striped table-hover', index=False, escape=False)
                raw_personality_table = personality.to_html(classes='table table-striped table-hover', index=False, escape=False)
            tone_table = style_table(raw_tone_table)
            personality_table = style_table(raw_personality_table)
            return render_template('analyze.html', tone_table=tone_table, personality_table=personality_table)
    return render_template('analyze_no_text.html')

def style_table(raw_table):
    old_html = '<table border="1" class="dataframe'
    new_html = '<table border="1px solid white" class="dataframe sortable' 
    table = raw_table.replace(old_html, new_html)
    return table

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)


