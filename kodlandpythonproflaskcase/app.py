from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)

@app.route('/')
def quiz():
    best_score = get_best_score()
    return render_template('quiz.html', best_score=best_score)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        username = request.form['username']
        question1 = request.form['question1']
        question2 = request.form['question2']
        question3 = request.form['question3']
        question4 = request.form['question4']
        question5 = request.form['question5']

        # Sınavı değerlendirme işlevi burada yapılabilir
        score = evaluate_quiz(question1, question2, question3, question4, question5)
        
        # Veritabanına kaydet
        user = User(username=username, score=score)
        db.session.add(user)
        db.session.commit()

        return render_template('result.html', username=username, score=score, best_score=get_best_score())

def evaluate_quiz(question1, question2, question3, question4, question5):
    score = 0
    
    # Soruların doğru cevapları
    correct_answers = {
        'question1': 'Data collection',
        'question2': 'OpenCV',
        'question3': 'NLTK',
        'question4': 'Data collection and cleaning',
        'question5': ['knn', 'k-en yakın komşu']  # Birden fazla doğru cevap için list kullanıldı
    }
    
    # Verilen cevaplar doğru cevaplara uygun mu kontrol ediliyor
    if question1 == correct_answers['question1']:
        score += 1
    if question2 == correct_answers['question2']:
        score += 1
    if question3 == correct_answers['question3']:
        score += 1
    if question4 == correct_answers['question4']:
        score += 1
    # Question 5 için kontrol
    if any(answer.lower() in question5.lower() for answer in correct_answers['question5']):
        score += 1

    return score

def get_best_score():
    best_score = db.session.query(db.func.max(User.score)).scalar()
    return best_score if best_score is not None else 0

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
