from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'secret123'

# Load dataset
df = pd.read_csv('data/students.csv')

# Dummy credentials
USERNAME = 'admin'
PASSWORD = 'admin123'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    subjects = list(df.columns[2:])
    avg_scores = df[subjects].mean().tolist()
    students = df['Name'].tolist()
    math_scores = df['Math'].tolist()
    return render_template('dashboard.html', subjects=subjects, avg_scores=avg_scores, students=students, math_scores=math_scores)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
