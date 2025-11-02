<<<<<<< HEAD
from flask import Flask, render_template, request, flash
import joblib
import re
import nltk
from nltk.corpus import stopwords

# Ensure stopwords are downloaded
=======
from flask import Flask,render_template,redirect,request,url_for,session,flash
import joblib,re,nltk
from nltk.corpus import stopwords

>>>>>>> dba0054f8ed87c8c0697cbd5783feead707b120d
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
<<<<<<< HEAD

# ✅ Clean text (must match the preprocessing used during training)
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)  # remove URLs
    text = re.sub(r'\@w+|\#', '', text)  # remove mentions, hashtags
    text = re.sub(r'[^a-z\s]', '', text)  # keep only letters and spaces
    text = ' '.join([word for word in text.split() if word not in stop_words])  # remove stopwords
    return text.strip()

# Initialize Flask app
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
=======
    
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

app=Flask(__name__)

model=joblib.load('Multi_nominal_model_spam.pkl')
vectorized=joblib.load('Vectorizer.pkl')

app.secret_key='my_secret'

@app.route('/',methods=['POST','GET'])
def index():
    prediction=None
    if request.method == 'POST':
        Messages=request.form.get('Messages')
        
        if not Messages or not Messages.strip():
            flash('Please enter message','warning')
            return render_template('index.html',prediction=None)
        
        cleaned=clean_text(Messages)
        msg_vectorize=vectorized.transform([cleaned])
        pred=model.predict(msg_vectorize)[0]
        
        prediction='Spam' if pred == 1 else 'Non-Spam'
        print("Original:", Messages)
        print("Cleaned:", cleaned)
        print("Prediction:", prediction)
        
    return render_template('index.html',prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> dba0054f8ed87c8c0697cbd5783feead707b120d
