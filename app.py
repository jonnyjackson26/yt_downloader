from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_choice = request.form['format']
    try:
        print(f"Trying to download from URL: {url}")
        ydl_opts = {}

        if format_choice == "mp4":
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
            }
        elif format_choice == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': '%(title)s.%(ext)s',
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            # Get the final filename for the MP3
            file_path = ydl.prepare_filename(info_dict)
            if format_choice == "mp3":
                file_path = file_path.replace('.webm', '.mp3')  # Update the path to point to the MP3

        print(f"File downloaded to: {file_path}")

        # Use send_file to send the downloaded MP3 file
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        print(f"Error: {e}")  # Log the error to the console
        return f"An error occurred: {str(e)}. Please make sure the URL is correct."


if __name__ == '__main__':
    app.run(debug=True)
