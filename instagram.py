from flask import Flask, render_template, jsonify
import instaloader

app = Flask(__name__)
L = instaloader.Instaloader()

# Change this to the Reel you want to track
TARGET_SHORTCODE = "DYPDeabsNXv"

@app.route('/')
def index():
    return render_template('index.html', shortcode=TARGET_SHORTCODE)

@app.route('/api/data')
def get_data():
    try:
        # Load the post data
        post = instaloader.Post.from_shortcode(L.context, TARGET_SHORTCODE)
        # Pull only the UI Play Count
        plays = post._node.get('video_play_count', 0)
        return jsonify({"plays": plays})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)