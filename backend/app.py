from flask import Flask, request, render_template, redirect, url_for
from models import db, Transcript

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transcripts.db'
db.init_app(app)


with app.app_context():
  db.create_all()

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/webhook', methods=['POST'])
def webhook():
  data = request.json
  call_id = data.get('call_id')
  transcript = data.get('concatenated_transcript')

  if call_id and transcript:
    new_transcript = Transcript(username="Andy", transcript=transcript)
    db.session.add(new_transcript)
    db.session.commit()
    return {"message": "Transcript saved successfully"}, 200
  else:
    return {"message": "Invalid data"}, 400

@app.route('/transcripts', methods=['GET', 'POST'])
def transcripts():
  if request.method == 'POST':
    username = request.form['username']
    user_transcripts = Transcript.query.filter_by(username=username).all()
    return render_template('transcripts.html', transcripts=user_transcripts, username=username)
  
  return render_template('transcripts.html', transcripts=[], username='')

if __name__ == '__main__':
  app.run(debug=True)
  # db.create_all()
