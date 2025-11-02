
from flask import Flask, render_template, request, flash
import joblib
import re
import nltk
from nltk.corpus import stopwords


from flask import Flask,render_template,redirect,request,url_for,session,flash
import joblib,re,nltk
from nltk.corpus import stopwords

try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE) 
    text = re.sub(r'\@w+|\#', '', text)  
    text = re.sub(r'[^a-z\s]', '', text)  
    text = ' '.join([word for word in text.split() if word not in stop_words])  
    return text.strip()

app = Flask(__name__)
app.secret_key = 'emotion_secret_key'


model = joblib.load('model.pkl')
vectorizer = joblib.load('tfidf_vectorize.pkl')


emotion_labels = {
    0: 'sadness',
    1: 'anger',
    2: 'love',
    3: 'surprise',
    4: 'fear',
    5: 'joy',
}

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    text_input = ""

    if request.method == 'POST':
        text_input = request.form.get('Text')

        if not text_input or not text_input.strip():
            flash('⚠️ Please enter a message to analyze.', 'warning')
            return render_template('index.html', prediction=None, text_input=text_input)


        cleaned = clean_text(text_input)
        vectorized = vectorizer.transform([cleaned])


        pred = model.predict(vectorized)[0]
        prediction = emotion_labels.get(pred, "Unknown")

        print("\n====================")
        print("Original:", text_input)
        print("Cleaned:", cleaned)
        print("Prediction:", prediction)
        print("====================\n")

    return render_template('index.html', prediction=prediction, text_input=text_input)

if __name__ == '__main__':
    app.run(debug=True)
5783feead707b120d
