from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
import subprocess
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with env var in production
DATABASE = os.path.join(os.path.dirname(__file__), 'queries.db')

# Case types for Faridabad District Court (sample)
CASE_TYPES = [
    'CIVIL', 'CRIMINAL', 'FAMILY', 'MISC', 'EXECUTION'
]

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_type TEXT,
        case_number TEXT,
        filing_year TEXT,
        raw_response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        case_type = request.form['case_type']
        case_number = request.form['case_number']
        filing_year = request.form['filing_year']
        # Call Playwright scraper
        case_data = None
        error = None
        try:
            result = subprocess.run([
                'python', 'scraper.py', case_type, case_number, filing_year
            ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
            if result.returncode != 0:
                error = 'Scraper error: ' + result.stderr
            else:
                output = result.stdout
                try:
                    data = json.loads(output)
                    case_data = data
                except Exception:
                    error = 'Could not parse case data.'
        except Exception as e:
            error = f'Error running scraper: {e}'
        # Log query and response
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        raw_html = case_data.get('raw_html', '') if case_data else ''
        c.execute('INSERT INTO queries (case_type, case_number, filing_year, raw_response) VALUES (?, ?, ?, ?)',
                  (case_type, case_number, filing_year, raw_html))
        conn.commit()
        conn.close()
        # Redirect to case details page
        return redirect(url_for('case_details', case_type=case_type, case_number=case_number, filing_year=filing_year))
    return render_template('index.html', case_types=CASE_TYPES)
@app.route('/case_details')
def case_details():
    case_type = request.args.get('case_type')
    case_number = request.args.get('case_number')
    filing_year = request.args.get('filing_year')
    # Call Playwright scraper again to get details (or cache in production)
    case_data = None
    error = None
    try:
        result = subprocess.run([
            'python', 'scraper.py', case_type, case_number, filing_year
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        if result.returncode != 0:
            error = 'Scraper error: ' + result.stderr
        else:
            output = result.stdout
            try:
                data = json.loads(output)
                case_data = data
            except Exception:
                error = 'Could not parse case data.'
    except Exception as e:
        error = f'Error running scraper: {e}'
    if case_data:
        return render_template('case_details.html', **case_data)
    else:
        return render_template('case_details.html', error=error)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
