# Activate the virtual environment if you have one
# On Windows (cmd)
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Set the FLASK_APP environment variable
# On Windows (cmd)
set FLASK_APP=run.py
# On macOS/Linux
export FLASK_APP=run.py

# Enable development mode (optional, but useful for debugging)
# On Windows (cmd)
set FLASK_ENV=development
# On macOS/Linux
export FLASK_ENV=development

# Run the Flask application
flask run
