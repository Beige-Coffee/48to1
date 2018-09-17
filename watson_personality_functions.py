from hidden import IBM_personality_insights_api
from watson_developer_cloud import PersonalityInsightsV3
import json
import pandas as pd


personality_insights = PersonalityInsightsV3(
    version = '2017-09-21',
    iam_apikey = IBM_personality_insights_api,
    url = 'https://gateway-wdc.watsonplatform.net/personality-insights/api'
)
# To prevent IBM from accessing our data for general service improvements, we
# set the X-Watson-Learning-Opt-Out header parameter to true when we create the service instance
personality_insights.set_default_headers({'x-watson-learning-opt-out': "true"})


def text_to_big5_personality_pd(profile):
    df = pd.DataFrame(profile['personality'])
    df['trait'] = 'Big5'
    df['name'][4] = 'Neuroticism'
    return df[['trait','name', 'percentile']]


def text_to_openness_sub_personality_pd(profile):
    df = pd.DataFrame(profile['personality'])
    df = pd.DataFrame(df[df['name'] == 'Openness']['children'][0])
    df['trait'] = 'Openness'
    return df[['trait','name', 'percentile']]


def text_to_conscientiousness_sub_personality_pd(profile):
    df = pd.DataFrame(profile['personality'])
    df = pd.DataFrame(df[df['name'] == 'Conscientiousness']['children'][1])
    df['trait'] = 'Conscientiousness'
    return df[['trait','name', 'percentile']]


def text_to_extraversion_sub_personality_pd(profile):
    df = pd.DataFrame(profile['personality'])
    df = pd.DataFrame(df[df['name'] == 'Extraversion']['children'][2])
    df['trait'] = 'Extraversion'
    return df[['trait','name', 'percentile']]


def text_to_agreeableness_sub_personality_pd(profile):
    df = pd.DataFrame(profile['personality'])
    df = pd.DataFrame(df[df['name'] == 'Agreeableness']['children'][3])
    df['trait'] = 'Agreeableness'
    return df[['trait','name', 'percentile']]


def text_to_neuroticism_sub_personality_pd(profile):
    df = pd.DataFrame(profile['personality'])
    df = pd.DataFrame(df[df['name'] == 'Emotional range']['children'][4])
    df['trait'] = 'Neuroticism'
    return df[['trait','name', 'percentile']]


def profile_to_needs_df(profile):
    df = pd.DataFrame(profile['needs'])
    df['trait'] = 'Needs'
    return df[['trait','name', 'percentile']]


def profile_to_values_df(profile):
    df = pd.DataFrame(profile['values'])
    df['trait'] = 'Values'
    return df[['trait','name', 'percentile']]


def all_personality_info_to_df(text):
    profile = personality_insights.profile(content = text, content_type='text/plain').get_result()
    frames = [text_to_big5_personality_pd(profile),
              text_to_openness_sub_personality_pd(profile),
              text_to_conscientiousness_sub_personality_pd(profile),
              text_to_extraversion_sub_personality_pd(profile),
              text_to_agreeableness_sub_personality_pd(profile),
              text_to_neuroticism_sub_personality_pd(profile),
              profile_to_needs_df(profile),
              profile_to_values_df(profile)
             ]
    return pd.concat(frames, ignore_index = True)

