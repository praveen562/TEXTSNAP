from flask import Flask, render_template, request, send_file, redirect, url_for
import csv
import datetime
import io
import os

app = Flask(__name__)

# Dummy summarizer and sentiment analyzer
def summarize_text(text):
    if len(text.strip()) > 150:
        return text.strip()[:150] + "..."
    return text.strip()

def detect_sentiment(text):
    text_lower = text.lower()
    if any(word in text_lower for word in ["good", "excellent", "amazing", "love", "best", "comfortable", "great"]):
        return "POSITIVE"
    elif any(word in text_lower for word in ["bad", "poor", "worst", "hate", "terrible", "confusing", "difficult", "faded"]):
        return "NEGATIVE"
    else:
        return "NEUTRAL"

# Save to history
def save_to_history(date, summary, sentiment):
    with open('history.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([date, summary, sentiment])

# Read history
def read_history():
    if not os.path.exists('history.csv'):
        return []
    with open('history.csv', 'r', encoding='utf-8') as file:
        return list(csv.reader(file))

# Home Page Route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Summarizer Page Route
@app.route('/index', methods=['GET', 'POST'])
def index():
    summary = ""
    sentiment = ""
    if request.method == 'POST':
        text = request.form['review']
        summary = summarize_text(text)
        sentiment = detect_sentiment(text)
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_to_history(date, summary, sentiment)
        return render_template('index.html', summary=summary, sentiment=sentiment)

    return render_template('index.html', summary=summary, sentiment=sentiment)

# Download summary as txt
@app.route('/download', methods=['POST'])
def download():
    summary = request.form['summary']
    buffer = io.BytesIO()
    buffer.write(summary.encode('utf-8'))
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="summary.txt", mimetype="text/plain")

# History page
@app.route('/history')
def history():
    history_data = read_history()
    return render_template('history.html', history=history_data)

if __name__ == "__main__":
    app.run(debug=True)
