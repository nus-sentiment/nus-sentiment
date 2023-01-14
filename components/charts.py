import altair as alt
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud, STOPWORDS  
import matplotlib.pyplot as plt
import random 
from textblob import TextBlob

def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    brightness = random.randint(44,70)
    color = random.choice(['40','226'])
    return "hsl(" + color + ", 97%, " + str(brightness) + "%)"

def wordcloudchart(data: pd.DataFrame):
        all_post_string = data['post'].sum()
        stopwords = set(STOPWORDS)
        stopwords.update(['a', 'b', 'c', 'u', 'C', 'want', 'know', 'take', 'think', 's', 'took', 'one', 'will', 'prof', 'lot', 'much', 'need'])
        fig, ax = plt.subplots(figsize=(15,5))
        wc = WordCloud(stopwords = stopwords, background_color = "white", max_words = 20)
        wc.generate(all_post_string)
        plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3), interpolation='bilinear')
        plt.axis("off")
        plt.show()
        return fig

def bar(counts: dict):
    fig = px.bar(x=list(counts.keys()), y=list(counts.values()), color=list(counts.keys()))
    return fig

def line_and_scatter(data: pd.DataFrame, keyword: str):
    chart = alt.Chart(data, title=f"Sentiment Over Time for {keyword}")

    line = chart.mark_line(tooltip=True).encode(
        x=alt.X("created_at:T", timeUnit="yearmonthdate", title="time"),
        y=alt.Y(
            "mean(sentiment):Q", title="sentiment", scale=alt.Scale(domain=[-1,1])
        ),
        color=alt.Color(value="#FF4B4B")
    )

    scatter = chart.mark_point(size=75, filled=True).encode(
        x=alt.X("created_at:T", timeUnit="yearmonthdate", title="time"),
        y=alt.Y("sentiment:Q", title="sentiment"),
        tooltip=alt.Tooltip(["created_at", "sentiment", "post"]),
        href="url"
    )

    return line + scatter

def wordcloudchart(data: pd.DataFrame):
    all_post_list = data['post'].sum().split()
    pos_word_list=''
    neu_word_list=''
    neg_word_list=''

    for word in all_post_list:               
        testimonial = TextBlob(word+ ' ')
        if testimonial.sentiment.polarity >= 0.5:
            pos_word_list+=(word+ ' ')
        elif testimonial.sentiment.polarity <= -0.5:
            neg_word_list+=(word+ ' ')
        else:
            neu_word_list+=(word + ' ')
        stopwords = set(STOPWORDS)

    stopwords.update(['a', 'b', 'c', 'u', 'C', 'want', 'know', 'take', 'think', 's', 'took', 'one', 'will', 'prof', 'lot', 'much', 'need', 'Thank', 'mod', 't', 'still', 'even', 'really'])
    
    lst_title_words = [[pos_word_list,'Positive Sentiment'], [neu_word_list, 'Neutral Sentiment'], [neg_word_list, 'Negative Sentiment']]
    figures = []
    count = 0
    for i in lst_title_words:
        fig, ax = plt.subplots(figsize=(15,5))
        ax.set_facecolor('black')
        wc = WordCloud(stopwords = stopwords, background_color = "black", max_words = 20)
        wc.generate(i[0])
        plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3), interpolation='bilinear')
        plt.axis("off")
        plt.title(i[1],fontdict = {'fontsize' : 30,
            'color':  'white'})
        plt.rcParams['axes.facecolor']='black'
        plt.rcParams['savefig.facecolor']='black'
        plt.show()
        figures.append(fig)
        count+=1
    return figures


