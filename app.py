from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('rsvp.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            invitation_id TEXT PRIMARY KEY,
            can_attend BOOLEAN,
            guests_count INTEGER,
            submission_date TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

@app.route('/respond/<invitation_id>', methods=['GET', 'POST'])
def respond(invitation_id):
    if request.method == 'POST':
        can_attend = request.form.get('can_attend') == 'yes'
        guests_count = int(request.form.get('guests_count', 0))
        submission_date = datetime.now()

        conn = sqlite3.connect('rsvp.db')
        c = conn.cursor()
        
        # Check if response already exists
        c.execute('SELECT * FROM responses WHERE invitation_id = ?', (invitation_id,))
        existing = c.fetchone()
        
        if existing:
            # Update existing response
            c.execute('''
                UPDATE responses 
                SET can_attend = ?, guests_count = ?, submission_date = ?
                WHERE invitation_id = ?
            ''', (can_attend, guests_count, submission_date, invitation_id))
        else:
            # Insert new response
            c.execute('''
                INSERT INTO responses (invitation_id, can_attend, guests_count, submission_date)
                VALUES (?, ?, ?, ?)
            ''', (invitation_id, can_attend, guests_count, submission_date))
        
        conn.commit()
        conn.close()
        
        return render_template('thank_you.html')
    
    return render_template('rsvp_form.html', invitation_id=invitation_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(debug=True)