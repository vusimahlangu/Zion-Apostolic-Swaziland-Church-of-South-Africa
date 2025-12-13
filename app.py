from flask import Flask, jsonify, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
DB_PATH = 'zion_church.db'
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            id_number TEXT UNIQUE NOT NULL,
            province TEXT NOT NULL,
            membership_number TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Branches table
    c.execute('''
        CREATE TABLE IF NOT EXISTS branches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            province TEXT NOT NULL,
            city TEXT NOT NULL,
            address TEXT,
            contact_phone TEXT
        )
    ''')
    # Insert 9 provinces
    provinces = [
        ('Eastern Cape', 'Gqeberha', '123 Faith St', '041 123 4567'),
        ('Free State', 'Bloemfontein', '456 Hope Rd', '051 234 5678'),
        ('Gauteng', 'Johannesburg', '789 Grace Ave', '011 345 6789'),
        ('KwaZulu-Natal', 'Durban', '321 Peace St', '031 456 7890'),
        ('Limpopo', 'Polokwane', '654 Love Rd', '015 567 8901'),
        ('Mpumalanga', 'Mbombela', '987 Unity Ave', '013 678 9012'),
        ('North West', 'Mahikeng', '147 Faith Rd', '018 789 0123'),
        ('Northern Cape', 'Kimberley', '258 Hope St', '053 890 1234'),
        ('Western Cape', 'Cape Town', '369 Grace Rd', '021 901 2345')
    ]
    for province in provinces:
        c.execute('INSERT OR IGNORE INTO branches (province, city, address, contact_phone) VALUES (?, ?, ?, ?)', province)
    conn.commit()
    conn.close()
    print("✅ Database initialized with 9 provinces")
init_db()
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'church': 'Zion Apostolic Swaziland Church of South Africa',
        'npo': '2023/757388/08',
        'motto': 'Building Faith, Unity, and the Future of Our Youth',
        'contact': '072 276 7670 (Youth President)',
        'timestamp': datetime.now().isoformat()
    })
@app.route('/api/church/info')
def church_info():
    return jsonify({
        'name': 'Zion Apostolic Swaziland Church of South Africa',
        'npo': '2023/757388/08',
        'motto': 'Building Faith, Unity, and the Future of Our Youth',
        'contact': '072 276 7670',
        'email': 'youth@zionchurch.org.za',
        'founded': 1985,
        'provinces': 9
    })
@app.route('/api/branches')
def get_branches():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT province, city, contact_phone FROM branches')
    branches = [{'province': row[0], 'city': row[1], 'phone': row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify({'branches': branches})
if __name__ == '__main__':
    print("=" * 70)
    print("ZION APOSTOLIC SWAZILAND CHURCH OF SOUTH AFRICA")
    print("=" * 70)
    print("NPO Registration: 2023/757388/08")
    print("Youth President: Mr. S. Shongwe - 072 276 7670")
    print("Motto: Building Faith, Unity, and the Future of Our Youth")
    print("=" * 70)
    print("🌐 Website: http://localhost:5000")
    print("📊 API Health: http://localhost:5000/api/health")
    print("🏛️  Branches: http://localhost:5000/api/branches")
    print("=" * 70)
    app.run(debug=True, port=5000, host='0.0.0.0')
