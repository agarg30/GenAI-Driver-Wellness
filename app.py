import os
import certifi
from flask import Flask, request, render_template, jsonify

from google.cloud import firestore
from wellness_message import WellnessMessage

# Set up Firestore credentials
os.environ['GRPC_DEFAULT_SSL_ROOTS_FILE_PATH'] = certifi.where()


app = Flask(__name__)
db = firestore.Client()
wellness_message = WellnessMessage()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Collect driver data from form or JSON
        data = request.get_json() if request.is_json else request.form
        driver_name = data.get('driver_name', '')
        trip_hours = data.get('trip_hours', '')
        fatigue_level = data.get('fatigue_level', '')
        wellness_note = data.get('wellness_note', '')
        on_medication = data.get('on_medication', '')
        medication_type = data.get('medication_type', '')
        medication_schedule = data.get('medication_schedule', '')
        driver_readiness = data.get('driver_readiness', '')
        emergency_contact = data.get('emergency_contact', '')
        # Save to Firestore
        doc_data = {
            'driver_name': driver_name,
            'trip_hours': trip_hours,
            'fatigue_level': fatigue_level,
            'wellness_note': wellness_note,
            'on_medication': on_medication,
            'medication_type': medication_type,
            'medication_schedule': medication_schedule,
            'driver_readiness': driver_readiness,
            'emergency_contact': emergency_contact,
            'createdAt': firestore.SERVER_TIMESTAMP
        }
        db.collection('DriverData').add(doc_data)
        # Generate AI wellness message
        ai_message = wellness_message.get_message(doc_data)
        return render_template('index.html', message='Data saved to Firestore', wellness_message=ai_message)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
