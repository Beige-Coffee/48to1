from hidden import IBM_tone_analyzer_api
from watson_developer_cloud import ToneAnalyzerV3
import json
import pandas as pd


tone_analyzer = ToneAnalyzerV3(
    version = '2017-09-21',
    iam_apikey = IBM_tone_analyzer_api,
    url = 'https://gateway-wdc.watsonplatform.net/tone-analyzer/api'
)

# To prevent IBM from accessing our data for general service improvements, we
# set the X-Watson-Learning-Opt-Out header parameter to true when we create the service instance
tone_analyzer.set_default_headers({'x-watson-learning-opt-out': "true"})

def text_analysis_to_pd(tone_analysis):
    return pd.DataFrame.from_dict(tone_analysis['document_tone']['tones'])

def get_score(tones):
    output = ''
    for idx, score in enumerate(tones, 1):
        output += f"Score {idx}: {score['score']} "
    return output

def get_tone(tones):
    output = ''
    for idx, score in enumerate(tones, 1):
        output += f"Tone {idx}: {score['tone_name']} "
    return output

def text_to_doc_analysis(text):
    tone_analysis = tone_analyzer.tone(
    {'text': text},
    'application/json').get_result()
    return text_analysis_to_pd(tone_analysis)


def text_to_sentence_analysis(text):
    tone_analysis = tone_analyzer.tone(
    {'text': text},
    'application/json').get_result()
    df = pd.DataFrame.from_dict(tone_analysis['sentences_tone'])
    df['score'] = df['tones'].apply(get_score)
    df['tone'] = df['tones'].apply(get_tone)
    return df[['text', 'score', 'tone']]