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