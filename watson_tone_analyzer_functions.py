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


def label_score(score):
    if score < .5:
        return 'Zero'
    elif .5 <= score <= .75:
        return 'Mid'
    else:
        return 'High'


def add_color(level, tone):
    if tone == 'Analytical':
        if level == 'Zero':
            return '#21252900'
        elif level == 'Mid':
            return '#afd5fd'
        else:
            return '#6eaff1'
    if tone == 'Joy':
        if level == 'Zero':
            return '#21252900'
        elif level == 'Mid':
            return '#fffd9d'
        else:
            return '#f7f338'
    if tone == 'Sadness':
        if level == 'Zero':
            return '#21252900'
        elif level == 'Mid':
            return '#eaebec'
        else:
            return '#cacaca'
    if tone == 'Anger':
            if level == 'Zero':
                return '#21252900'
            elif level == 'Mid':
                return '#f3c9c9'
            else:
                return '#e28d8d'
    if tone == 'Tentative':
            if level == 'Zero':
                return '#21252900'
            elif level == 'Mid':
                return '#e5cdf1'
            else:
                return '#cc97e6'
    if tone == 'Confident':
            if level == 'Zero':
                return '#21252900'
            elif level == 'Mid':
                return '#bcf5c9'
            else:
                return '#44e268'
    if tone == 'Fear':
            if level == 'Zero':
                return '#21252900'
            elif level == 'Mid':
                return '#f3dee7'
            else:
                return '#f1a6c6'


def find_sentence_tone(tone_analysis, tone):
    for d in tone_analysis['sentences_tone']:
        if len(d['tones']) == 0:
            sentence = d['text']
            yield {
                   'sentence' : sentence,
                   'score' : 0,
                   'level' : 'Zero',
                   'color' : add_color('Zero', tone)
                    }
        else:
            tones = []
            for sent in d['tones']:
                tones.append(sent['tone_name'])
            if tone not in tones:
                sentence = d['text']
                yield {
                       'sentence' : sentence,
                       'score' : 0,
                       'level' : 'Zero',
                       'color' : add_color('Zero', tone)
                        }
            else:
                for sent in d['tones']:
                    if sent['tone_name'] != tone:
                        continue
                    else:
                        sentence = d['text']
                        score = sent['score']
                        level = label_score(sent['score'])
                        color = add_color(label_score(sent['score']), tone)
                        yield {
                            'sentence' : sentence,
                            'score' : score,
                            'level' : level,
                            'color' : color
                               }

def tone_to_doc_analysis(tone_analysis):
    df = text_analysis_to_pd(tone_analysis)
    return df[['tone_name','score']]

def find_doc_tones(tone_analysis):
    tones = []
    for d in tone_analysis['sentences_tone']:
        if len(d['tones']) > 0:
            for sent in d['tones']:
                if sent['tone_name'] not in tones:
                    tone = sent['tone_name']
                    tones.append(tone)
                    yield {
                        'tone_name' : tone
                           }
                else:
                    continue
        else:
            continue

def doc_tone_finder(tone_analysis):
    return pd.DataFrame(list(find_doc_tones(tone_analysis)))