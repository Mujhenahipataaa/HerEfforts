import os
from flask import Flask, render_template, jsonify
import instaloader

app = Flask(__name__)
L = instaloader.Instaloader()

# --- CONFIGURATION ---
TARGET_USERNAME = "artist_virtichhajed"  # Account to track followers
TARGET_SHORTCODE = "DYPDeabsNXv"          # Reel to track views

# Fetch sensitive session data from environment variables
BURNER_USERNAME = os.environ.get("BURNER_USERNAME", "quinch102")
SESSION_ID = os.environ.get("SESSION_ID") 

if SESSION_ID:
    try:
        print("Setting up authenticated session from environment variables...")
        L.context._session.cookies.set("sessionid", SESSION_ID, domain=".instagram.com")
        L.context.username = BURNER_USERNAME
        
        # Render has a read/write local directory, but it's ephemeral.
        # We save it here just to satisfy instaloader's context flow.
        L.save_session_to_file(filename=BURNER_USERNAME)
        print("Session loaded successfully!")
    except Exception as e:
        print(f"Failed to apply session cookie: {e}")
else:
    print("WARNING: No SESSION_ID environment variable found. Requests might be unauthenticated.")
# ---------------------

# --- HTML ROUTES ---

@app.route('/')
@app.route('/followers')
def followers_page():
    return render_template('followers.html', username=TARGET_USERNAME)

@app.route('/views')
def views_page():
    return render_template('views.html', shortcode=TARGET_SHORTCODE)


# --- LIVE API DATA ENDPOINTS ---

@app.route('/api/followers')
def get_followers():
    try:
        profile = instaloader.Profile.from_username(L.context, TARGET_USERNAME)
        return jsonify({"followers": profile.followers})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/plays')
def get_plays():
    try:
        post = instaloader.Post.from_shortcode(L.context, TARGET_SHORTCODE)
        # Fallback to standard video_view_count if play count is missing
        plays = post._node.get('video_play_count', post._node.get('video_view_count', 0))
        return jsonify({"plays": plays})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Render requires binding to 0.0.0.0 and using the dynamic PORT variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
