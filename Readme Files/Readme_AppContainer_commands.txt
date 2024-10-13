# Update the repositories
sudo apt update -y

# Install python packages
sudo apt install python3 python3-pip python3-venv -y

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Now we need to put the files of the project inside the home directory using MobaXterm

# Install the packages for our application
pip install -r requirements.txt

# Run the application (Need to be in the same directory)
python app.py
