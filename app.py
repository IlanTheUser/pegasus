# Import necessary modules
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import inspect
import time
import sys

# Initialize Flask application
app = Flask(__name__)

# Database configuration
# Use environment variable for DATABASE_URL if available, otherwise use default MySQL connection string
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql://user:password@db/myapp')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy event system

# Initialize SQLAlchemy without binding it to app
db = SQLAlchemy()
db.init_app(app)

# Define the database model for user preferences
class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<UserPreference {self.name}>'  # String representation of the object

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')  # Render the main page

# Route to handle saving user preferences
@app.route('/save', methods=['POST'])
def save():
    data = request.json  # Get JSON data from the request
    new_preference = UserPreference(name=data['name'], color=data['color'])
    db.session.add(new_preference)  # Add new preference to the database session
    db.session.commit()  # Commit the changes to the database
    return jsonify({"success": True})  # Return a JSON response indicating success

# Route to display all saved preferences
@app.route('/results')
def results():
    all_data = UserPreference.query.all()  # Fetch all user preferences from the database
    return render_template('results.html', data=all_data)  # Render results page with fetched data

# Function to create database tables
def create_tables():
    max_retries = 5
    retry_count = 0
    while retry_count < max_retries:
        try:
            with app.app_context():  # Ensure we're within the Flask app context
                inspector = inspect(db.engine)
                if not inspector.has_table('user_preference'):
                    db.create_all()  # Create all tables defined in the models
                    print("Tables created.")
                else:
                    print("Tables already exist.")
            break  # Exit the loop if successful
        except Exception as e:
            retry_count += 1
            print(f"Error connecting to the database: {e}")
            print(f"Retrying in 5 seconds... (Attempt {retry_count}/{max_retries})")
            time.sleep(5)  # Wait for 5 seconds before retrying
    
    if retry_count == max_retries:
        print("Failed to connect to the database after multiple attempts. Exiting.")
        sys.exit(1)  # Exit the application if unable to connect to the database

# Main execution block
if __name__ == '__main__':
    create_tables()  # Ensure database tables are created before running the app
    app.run(host='0.0.0.0', debug=True)  # Run the Flask app, accessible from any IP, in debug mode