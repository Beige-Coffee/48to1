import sys
sys.path.append('..')
from collections import Counter
from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
import numpy as np
import pandas as pd
from watson_personality_functions import all_personality_info_to_df, personality_insights
from watson_tone_analyzer_functions import text_to_sentence_analysis, find_sentence_tone, doc_tone_finder, tone_analyzer

app = Flask(__name__,
            static_url_path='') 

@app.route('/', methods=['GET'])
def welcome_page():
    return render_template('index.html')

@app.route('/contact', methods=['GET'])
def contact_page():
    return render_template('contact.html')

@app.route('/research', methods=['GET'])
def load_research():
    return render_template('research.html')

@app.route('/example', methods=['GET'])
def load_example():
    tone_analysis_example = pickle.load(open("tone_analysis.p", "rb"))
    data = pd.DataFrame(list(find_sentence_tone(tone_analysis_example, 'Analytical')))
    doc = doc_tone_finder(tone_analysis_example)
    personailty_df = pickle.load( open( "personality.pkl", "rb" ) )
    with pd.option_context('display.max_colwidth', -1):
        personality_table =  personailty_df.to_html(classes='table table-striped table-hover', index=False, escape=False)
        return render_template('example.html', data=data, doc=doc)

@app.route('/example/<tone_name>', methods=['GET'])
def load_example_tone(tone_name):
    tone_analysis_example = pickle.load(open("tone_analysis.p", "rb"))
    data = pd.DataFrame(list(find_sentence_tone(tone_analysis_example, tone_name)))
    doc = doc_tone_finder(tone_analysis_example)
    personailty_df = pickle.load( open( "personality.pkl", "rb" ) )
    with pd.option_context('display.max_colwidth', -1):
        personality_table =  personailty_df.to_html(classes='table table-striped table-hover', index=False, escape=False)
        return render_template('example.html', data=data, doc=doc)

@app.route('/analyze/<tone_name>', methods=['GET'])
def load_tone(tone_name):
    data = pd.DataFrame(list(find_sentence_tone(tone_analysis, tone_name)))
    doc = doc_tone_finder(tone_analysis)
    return render_template('analyze_text_tone.html', data=data, doc=doc)

@app.route('/analyze', methods=['GET', 'POST'])
def load_analyze():
    if request.method == 'POST':
        text = request.form['text']
        if len(text.split()) > 1:
            global tone_analysis
            tone_analyzer.set_default_headers({'x-watson-learning-opt-out': "true"})
            tone_analysis = tone_analyzer.tone(
            {'text': text},
            'application/json').get_result()
            if "sentences_tone" in tone_analysis.keys():
                data = pd.DataFrame(list(find_sentence_tone(tone_analysis, 'Analytical')))
                doc = doc_tone_finder(tone_analysis)
                return render_template('analyze_text_tone.html', data=data, doc=doc)
    return render_template('analyze_no_text.html')

def style_table(raw_table):
    old_html = '<table border="1" class="dataframe'
    new_html = '<table border="1px solid white" class="dataframe sortable' 
    table = raw_table.replace(old_html, new_html)
    return table

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=False)


