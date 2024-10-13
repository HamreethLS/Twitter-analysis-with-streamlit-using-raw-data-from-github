import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(layout='wide',page_title='Twitter Analysis Dashboard')
# Load the data
url = "https://raw.githubusercontent.com/skathirmani/datasets/refs/heads/main/narendramodi_tweets.csv"
data = pd.read_csv(url)

# Convert created_at column to datetime and extract year and month
data['created_at'] = pd.to_datetime(data['created_at'])
data['year'] = data['created_at'].dt.year
data['month'] = data['created_at'].dt.month


# Create the header
st.title("Narendra Modi - Twitter Analysis")
st.write("Created by Hamreeth L S")

# Create the sidebar
st.sidebar.header("Filters")
year_filter = st.sidebar.selectbox("Select Year", data['year'].unique())
source_filter = st.sidebar.selectbox("Select Source", data['source'].unique())

# Filter the data based on the selected year and source
filtered_data = data[(data['year'] == year_filter) & (data['source'] == source_filter)]


# First row: Three metrics
st.metric("No. of Tweets", len(filtered_data))
st.metric("Average Retweets", filtered_data['retweets_count'].mean().astype(int))
st.metric("Average Likes", filtered_data['favorite_count'].mean().astype(int))

# Second row: Line chart
st.write("Month-wise Total Number of Tweets")
monthly_tweets = filtered_data.groupby('month')['id'].count().reset_index()
monthly_tweets['month'] = monthly_tweets['month'].apply(lambda x: pd.to_datetime(x, format='%m').strftime('%B'))

fig1 = px.line(monthly_tweets, x='month', y='id', markers=True)
fig1.update_layout(
    title='Month-wise Total Number of Tweets',
    xaxis_title='Month',
    yaxis_title='Number of Tweets',
    xaxis=dict(tickmode='array', tickvals=list(range(1, 13)), ticktext=monthly_tweets['month']),
    template='plotly_white'
)
st.plotly_chart(fig1, key="line_chart")

# Third row: Two columns
col1, col2 = st.columns(2)

# Month-wise total number of hashtags
st.write("Month-wise Total Number of Hashtags")
fig2 = px.bar(filtered_data.groupby('month')['hashtags_count'].sum().reset_index(), x='month', y='hashtags_count')
fig2.update_layout(
    title='Month-wise Total Number of Hashtags',
    xaxis_title='Month',
    yaxis_title='Number of Hashtags',
    xaxis=dict(tickmode='array', tickvals=list(range(1, 13)), ticktext=pd.date_range(start='2022-01-01', periods=12, freq='M').strftime('%B')),
    template='plotly_white'
)
st.plotly_chart(fig2, key="bar_chart1")

# Top 10 tweets based on number of likes
st.write("Top 10 Tweets by Likes")
top_tweets = filtered_data.nlargest(10, 'favorite_count')
st.write(top_tweets[['text', 'favorite_count']].rename(columns={'text': 'Tweet', 'favorite_count': 'Likes'}))

# Optional: Hashtag analysis tab
st.write("---")
st.write("Hashtag Analysis")
# Extract hashtags from the 'text' column
def extract_hashtags(text):
    hashtags = re.findall(r'#\w+', text)
    return hashtags

filtered_data['hashtags'] = filtered_data['text'].apply(extract_hashtags)
# Top 10 hashtags
top_hashtags = filtered_data['hashtags'].explode().value_counts().nlargest(10)
st.write(top_hashtags)

# Bar chart of top 10 hashtags
fig3 = px.bar(x=top_hashtags.index, y=top_hashtags.values)
fig3.update_layout(xaxis_title='Hashtag', yaxis_title='Count')
st.plotly_chart(fig3, key="bar_chart2")