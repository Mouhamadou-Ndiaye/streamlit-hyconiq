import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import seaborn as sns
import missingno as msno
import plotly.express as px
import altair as alt

from PIL import Image


# Functions

# ---------------------Data Observation-----------------------------------------#


def data_observation(data):
    st.markdown("---")
    df = pd.read_csv(data + '.csv', encoding='utf-8', delimiter=",")
    st.subheader(data + ' data')
    code_1 = data + '''.head(10)'''
    st.code(code_1, language='python')
    st.dataframe(df.head(10))
    st.subheader('Description of the data')
    st.table(df.describe())



def count_rows(rows):
    return len(rows)


def drop_col(hyconiq) :
    hyconiq_drop = hyconiq
    for x in range(1,21) :
        hyconiq_drop = hyconiq_drop.drop(columns = [rf'taggedFullName{x}',rf'taggedUsername{x}'])
    hyconiq_drop = hyconiq_drop.drop(columns = ['playCount','videoDuration','query','caption','profileUrl','query','location','locationId','viewCount','username','postId','postUrl','videoUrl','imgUrl','fullName','likedByViewer'])
    pd.DataFrame((hyconiq_drop))
    return hyconiq_drop

from datetime import datetime


def get_weekday(dt):
    return dt.weekday()


def get_hour(dt):
    return dt.hour


def get_month(dt):
    return dt.month


def get_dom(dt):
    return dt.day


def time_gestion(data):
    data['pubDate'] = data['pubDate'].map(pd.to_datetime)
    data['weekday'] = data['pubDate'].map(get_weekday)
    data['hour'] = data['pubDate'].map(get_hour)
    data['month'] = data['pubDate'].map(get_month)
    data['day'] = data['pubDate'].map(get_dom)
    return data


def typeconvert(study_data):
    study_data['type'] = (study_data['type']).apply(lambda x: str(x))
    study_data['isSidecar'] = (study_data['isSidecar']).apply(lambda x: str(x))
    return study_data

def initializing(study_data):
    hycoviz = study_data.drop(columns=['pubDate', 'timestamp'])
    hycoviz = hycoviz.drop_duplicates()
    return hycoviz


def frequency(study_data, freq, var):
    fig = px.bar(study_data, x=study_data[freq], y=study_data[var], color=study_data['month'], title= var + ' by ' + freq)
    st.plotly_chart(fig)


def frequecy_list(study_data):

    col1, col2 = st.columns(2)

    sf = col1.selectbox(
        "Sélectionner",  # Drop Down Menu Name
        [
            'likeCount',
            'commentCount',
        ]
    )

    sd = col2.selectbox(
        "Sélectionner votre temporalité",  # Drop Down Menu Name
        [
            'hour',
            'day',
            'weekday'
        ]
    )

    frequency(study_data, sd, sf)

def typestudy(study_data, freq, var, type):
    fig = px.bar(study_data, x=study_data[freq], y=study_data[var], color=study_data[type], barmode="group", title= var + ' of ' + type + ' by ' + freq)
    st.plotly_chart(fig)

def type_list(study_data):

    col1, col2, col3 = st.columns(3)

    sf = col1.selectbox(
        "Sélectionner",  # Drop Down Menu Name
        [
            'likeCount',
            'commentCount',
        ]
    )

    se = col2.selectbox(
        "Sélectionner",  # Drop Down Menu Name
        [
            'type',
            'isSidecar',
        ]
    )

    sd = col3.selectbox(
        "Sélectionner votre temporalité",  # Drop Down Menu Name
        [
            'hour',
            'day',
            'weekday'
        ]
    )

    typestudy(study_data, sd, sf,se)

def top10liked (pub_stat) :
    pub_stat_like_top10 = pub_stat.sort_values(by = ['likeCount'], ascending=False).head(20)
    fig = px.pie(pub_stat_like_top10,values = pub_stat_like_top10['likeCount'] , names = pub_stat_like_top10['description'],title='Top Like Post Hyconiq', color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)


def top10Commented (pub_stat) :
    pub_stat_comment_top10 = pub_stat.sort_values(by = ['commentCount'], ascending=False).head(20)
    fig = px.pie(pub_stat_comment_top10,values = pub_stat_comment_top10['commentCount'] , names = pub_stat_comment_top10['description'], title = 'Top Comment post hyconiq', color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

def heatmap(data_drop):
    fig = plt.figure(figsize=(10, 4))
    datag = data_drop.groupby(['weekday', 'hour']).apply(count_rows).unstack()
    heatmap = sns.heatmap(datag, linewidths=.5)
    plt.title('Heatmap by Hour and weekdays', fontsize=15)
    heatmap.set_yticklabels(('Lun Mar Mer Jeu Ven Sam Dim').split(), rotation='horizontal')
    st.pyplot(fig)
# In this function we're going to look at the data and his missing values

# ---------------------Data Processing-----------------------------------------#
# How to manage the columns in my data
# In this function we're going to delete the column we don't use in our dataviz and rename the columns


if __name__ == "__main__":

    with st.sidebar:
        selected = option_menu("HyconiqViz",
                               ["Presentation", "Transforming the Data", "Frequency", "Type Study", "Top 10"
                                   , "n._mouhamadou_", "621565314", "mouhamadou.ndiaye@efrei.net"
                                ],
                               icons=['instagram', 'gear', 'calendar', 'search', 'file-bar-graph', 'instagram', 'telephone', 'envelope'
                                      ], menu_icon="cast", default_index=1)

    st.title("Welcome to my HyconiqViz 🎶")

    if selected == "Presentation":

        from PIL import Image

        hyconiqImage = Image.open('hyco1.jpg')
        hyconiqImage2 = Image.open('hyco2.jpg')


        st.image(hyconiqImage, caption='Logo Hyconiq', width=500)
        st.title("Presentation 🎤")
        st.markdown(
            "Yo tout le monde, ici c'est Mouhamadou Ndiaye, et je vais vous présenter une data visualisation sur les posts Instagram de votre compte Hyconiq."
            " Comme vous pouvez le voir, je suis très intéressé par Hyconiq que je suis depuis maintenant 5 ans !")
        st.image(hyconiqImage2, caption='Apprendre, Inspirer, Divertir. BE A PART OF THE CULTURE.')

        st.markdown('La data visualisation que je vais vous présenter, montre des statistiques sur le nombre de likes ou de comments '
                    ', le comportement de ces derniers à travers les jours et heures, et bien plus encore ... Elle se déroule du mois d août à Octobre 2022.  Bonne visualisation 🔥.')

    if selected == "Transforming the Data":
        from PIL import Image

        st.title("Discovering the data 📚")
        discover = Image.open('discover.jpg')
        st.image(discover)
        st.title('Hyconiq data')
        data_observation('hyconiq')

        st.markdown('---')

        st.title("Transforming the data 📚")
        process = Image.open('process.jpg')
        st.image(process)
        st.subheader('Data Drop')

        st.write(
            'Comme vous pouvez le voir il y a des colonnes qui on des valeurs manquantes et des colonnes répititives. '
            'Je vais donc supprimer ces colonnes afin de procéder à la visualisation')

        hyconiq = pd.read_csv('hyconiq.csv')

        st.subheader('hyconiq data after transform')
        hyconiq = drop_col(hyconiq)
        st.dataframe(hyconiq.head(10))
        st.subheader('Rajout des colonnes jour, mois, heure')
        hyconiq = time_gestion(hyconiq)
        hyconiq  = initializing(hyconiq)
        st.dataframe(hyconiq.head(10))

    if selected == "Frequency":
        hyconiq = pd.read_csv('hyconiq.csv')
        hyconiq = drop_col(hyconiq)
        hyconiq = time_gestion(hyconiq)
        hyconiq = typeconvert(hyconiq)
        hyconiq = initializing(hyconiq)

        st.title('Statistiques de like et de comments par post')

        post = Image.open('post.jpg')
        st.image(post)

        frequecy_list(hyconiq)

    if selected == "Type Study":
        hyconiq = pd.read_csv('hyconiq.csv')
        hyconiq = drop_col(hyconiq)
        hyconiq = time_gestion(hyconiq)
        hyconiq = typeconvert(hyconiq)
        hyconiq = initializing(hyconiq)

        st.title('Statistiques de like et de comments par type de post')
        media = Image.open('media.jpg')
        st.image(media)

        type_list(hyconiq)

    if selected == "Top 10":
        hyconiq = pd.read_csv('hyconiq.csv')
        hyconiq = drop_col(hyconiq)
        hyconiq = time_gestion(hyconiq)
        hyconiq = typeconvert(hyconiq)
        hyconiq = initializing(hyconiq)

        st.title('Top 10')
        top = Image.open('top.jpg')
        st.image(top)

        st.title('Top 10 Liked post')
        top10liked(hyconiq)

        st.title('Top 10 Commented post')
        top10Commented(hyconiq)

        st.title('Bonus Correlation')
        heatmap(hyconiq)






