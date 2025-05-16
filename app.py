from flask import Flask, render_template, request
from scraper import scrape_instagram_data
from sentiment_utils import analyze_sentiment, calculate_engagement

app = Flask(__name__)

sentiment_post_map = {
    'Very Positive': [],
    'Positive': [],
    'Neutral': [],
    'Negative': [],
    'Very Negative': []
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    username = request.form['username']
    data = scrape_instagram_data(username)

    zipped_data = []

    followers_raw = data['followers']

    for i, caption in enumerate(data['captions']):
        hashtags = data['hashtags'][i]
        sentiment = analyze_sentiment(caption, hashtags)

        post_link = data['post_links'][i]
        image = data['images'][i]
        likes = data['likes'][i]
        comments = data['comments'][i]

        engagement_rate = calculate_engagement(followers_raw, likes, comments)

        sentiment_post_map[sentiment].append((caption, post_link))

        zipped_data.append({
            'link': post_link,
            'caption': caption,
            'hashtags': hashtags,
            'sentiment': sentiment,
            'image': image,
            'likes': likes,
            'comments': comments,
            'engagement_rate': engagement_rate
        })

    result = {
        'username': username,
        'posts': data['posts'],
        'followers': data['followers'],
        'following': data['following'],
    }

    return render_template('results.html', result=result, zipped=zipped_data)

@app.route('/filter/<mood>')
def filter_by_mood(mood):
    posts = sentiment_post_map.get(mood, [])
    return render_template('filter.html', mood=mood, posts=posts)

if __name__ == '__main__':
    app.run(debug=True)