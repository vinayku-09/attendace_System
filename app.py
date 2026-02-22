from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
import os
import face_recognition
import pandas as pd
import numpy as np
import cv2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy user database for demonstration purposes
users = {
    "user@example.com": "password123"
}

# Ensure upload directory exists
os.makedirs('uploads', exist_ok=True)

# Load student images and create encodings
def load_student_images(path='students_images'):
    student_encodings = []
    student_names = []
    for image_name in os.listdir(path):
        img_path = os.path.join(path, image_name)
        try:
            img = face_recognition.load_image_file(img_path)
            img_encoding = face_recognition.face_encodings(img)[0]
            student_encodings.append(img_encoding)
            student_names.append(os.path.splitext(image_name)[0])
        except (IndexError, FileNotFoundError):
            print(f"Error loading {img_path}")
    return student_encodings, student_names

# Load the attendance sheet
def load_attendance_sheet(path='attendance.csv'):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Roll No', 'Name'])

# Save the updated attendance sheet
def save_attendance_sheet(attendance_df, path='attendance.csv'):
    attendance_df.to_csv(path, index=False)
    print("Attendance sheet updated.")

# Mark attendance in the DataFrame
def mark_attendance_in_sheet(name, attendance_df, date):
    if name in attendance_df['Name'].values:
        if date not in attendance_df.columns:
            attendance_df[date] = 'A'  # Initialize column for the date with 'A' for absent
        attendance_df.loc[attendance_df['Name'] == name, date] = 'P'  # Mark as present
        print(f"Marked {name} as present on {date}.")
    else:
        print(f"{name} not found in the attendance sheet.")
    
    # Print the attendance_df for debugging
    print("Updated Attendance DataFrame:")
    print(attendance_df)

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        users[email] = password  # Storing the user in the dummy database

        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('signup/index.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and users[email] == password:
            return redirect(url_for('ams_panel'))
        else:
            flash('Invalid login credentials, please try again.')
            return redirect(url_for('login'))

    return render_template('login/index.html')

# AMS Panel Route
@app.route('/ams_panel')
def ams_panel():
    return render_template('ams_panel/index.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/index.html')

# Capture Attendance Route
@app.route('/capture_attendance')
def capture_attendance():
    return render_template('capture_attendance/index.html')

# Process Attendance Route (handles form submission for attendance)
@app.route('/process_attendance', methods=['POST'])
def process_attendance():
    if 'classImage' not in request.files:
        return "No image uploaded!", 400

    date = request.form['date']
    uploaded_file = request.files['classImage']

    # Save the uploaded image temporarily
    img_path = os.path.join('uploads', uploaded_file.filename)
    uploaded_file.save(img_path)

    # Load student encodings
    student_encodings, student_names = load_student_images()

    # Load and process the uploaded image
    img = face_recognition.load_image_file(img_path)
    rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect all faces in the image
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    matched_students = []
    attendance_df = load_attendance_sheet()

    # Compare faces and mark attendance
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(student_encodings, face_encoding)
        face_distances = face_recognition.face_distance(student_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = student_names[best_match_index]
            mark_attendance_in_sheet(name, attendance_df, date)
            matched_students.append(name)
        else:
            matched_students.append("Unknown")

    # Save the updated attendance sheet
    save_attendance_sheet(attendance_df)

    # Count the number of 'P' entries for the given date
    num_present = attendance_df[date].value_counts().get('P', 0)

    # Create a new row for "Total Present"
    new_row = {col: None for col in attendance_df.columns}  # Initialize new row with None for all columns
    new_row['Name'] = 'Total Present'
    new_row[date] = num_present  # Assuming 'date' is the date column you want to update

    # Convert the new row to a DataFrame
    new_row_df = pd.DataFrame([new_row])

    # Use pd.concat to append the new row
    attendance_df = pd.concat([attendance_df, new_row_df], ignore_index=True)

    # Save the sheet again with the updated 'Total Present' row
    save_attendance_sheet(attendance_df)

    return jsonify({
        'matched_students': matched_students,
        'num_present': int(num_present)  # Ensure it's a standard Python int for JSON serialization
    })

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
