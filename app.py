from flask import Flask, request, render_template, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        print(f"Trying to download from URL: {url}")
        
        output_path = "downloaded_video.mp4"
        # Run yt-dlp to download the video
        subprocess.run(['yt-dlp', '-o', output_path, url], check=True)

        print(f"File downloaded to: {output_path}")

        return send_file(output_path, as_attachment=True)
    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred: {str(e)}. Please make sure the URL is correct."

if __name__ == '__main__':
    app.run(debug=True)
