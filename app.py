import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from io import BytesIO

app = Flask(__name__)

# Configuration for SQLAlchemy and Flask session
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medications.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # For sessions

# Initialize the database
db = SQLAlchemy(app)

# Import the models
from models import Medication, User

# Ensure that the tables are created at startup
with app.app_context():
    db.create_all()

# Home route (requires login)
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            return 'Username already exists'
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# API to add a new medication
@app.route('/add_medication', methods=['POST'])
def add_medication():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = request.get_json()
    new_med = Medication(
        medName=data['medName'],
        dosage=data['dosage'],
        time=data['time'],
        interval=data['interval'],
        notes=data['notes']
    )
    db.session.add(new_med)
    db.session.commit()
    return jsonify({'success': True})

# API to get all medications
@app.route('/get_medications', methods=['GET'])
def get_medications():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    medications = Medication.query.all()
    meds = [
        {
            'id': med.id,
            'medName': med.medName,
            'dosage': med.dosage,
            'time': med.time,
            'interval': med.interval,
            'notes': med.notes
        } for med in medications
    ]
    return jsonify({'medications': meds})

# API to delete a medication
@app.route('/delete_medication/<int:id>', methods=['DELETE'])
def delete_medication(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    med = Medication.query.get(id)
    if med:
        db.session.delete(med)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Medication not found'})

@app.route('/edit_medication/<int:id>', methods=['GET', 'POST'])
def edit_medication(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    med = Medication.query.get(id)
    
    if request.method == 'POST':
        # Update the medication with the new data from the form
        med.medName = request.form['medName']
        med.dosage = request.form['dosage']
        med.time = request.form['time']
        med.interval = request.form['interval']
        med.notes = request.form['notes']
        
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_medication.html', med=med)

# Route to export medications to an Excel file
@app.route('/export_medications', methods=['GET'])
def export_medications():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    medications = Medication.query.all()

    # Convert the data to a pandas DataFrame
    meds = [
        {
            'Medication Name': med.medName,
            'Dosage': med.dosage,
            'Time': med.time,
            'Interval (Hours)': med.interval,
            'Notes': med.notes
        } for med in medications
    ]
    
    df = pd.DataFrame(meds)

    # Create a BytesIO object to hold the Excel file
    output = BytesIO()

    # Write the DataFrame to an Excel file
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Medications')
    
    # Set the position of the file pointer to the beginning
    output.seek(0)

    # Send the file as a response with a download prompt
    return send_file(output, as_attachment=True, download_name='medications.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    app.run(debug=True)
