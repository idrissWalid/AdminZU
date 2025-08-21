from flask import Flask, render_template, request, redirect, url_for, session
from flask import send_from_directory
from flask import jsonify
from flask import make_response

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Stockage votes en mémoire
votes = {"Candidat1": 0, "Candidat2": 0}

# --- Route user vote page ---
@app.route('/')
def index():
    return "API de vote en ligne. Utilisez les routes /vote/<candidate> pour voter.", 200

# --- Route pour voter ---
@app.route('/vote/<candidate>', methods=['POST'])
def vote(candidate):
    if candidate in votes:
        votes[candidate] += 1
    return '', 204

# --- Admin login page ---
@app.route('/admin', methods=['GET'])
def admin_login_page():
    return render_template('admin_login.html')

# --- Admin login POST ---
@app.route('/admin_login', methods=['POST'])
def admin_login():
    pwd = request.form.get('password')
    if pwd == 'Lifeisabitch13':
        session['admin'] = True
        return redirect('/dashboard')
    else:
        return 'Mot de passe incorrect', 403

# --- Dashboard ---
@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/admin')

    total = votes["Candidat1"] + votes["Candidat2"]
    percent_c1 = round((votes["Candidat1"] / total * 100), 2) if total else 0
    percent_c2 = round((votes["Candidat2"] / total * 100), 2) if total else 0

    return render_template(
        'admin_dashboard.html',
        total_votes=total,
        votes_c1=votes["Candidat1"],
        votes_c2=votes["Candidat2"],
        percent_c1=percent_c1,
        percent_c2=percent_c2
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
