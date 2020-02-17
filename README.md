React-Tracks application

Setup
The first thing to do is to clone the repository:

- $ git clone https://github.com/Mostafapy/react-tracks.git
- $ cd react-tracks

Create a virtual environment to install dependencies in and activate it:
- $ python3 -m venv env
- $ source env/bin/activate

For Windows Users:
- $ python3 -m venv env
- Note add this command to settings.json file ""terminal.integrated.shellArgs.windows": ["-ExecutionPolicy", "RemoteSigned"]"
- $ env/Scripts/activate

Then install the dependencies:
(env)$ pip install -r requirements.txt

Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by venv.

Once pip has finished downloading the dependencies Then migrate and runserver:
- (env)$ cd app
- (env)$ python manage.py migrate
- (env)$ python manage.py runserver


And navigate to http://127.0.0.1:8000/.

In order to test the purchase flows, fill in the account details in project/gc_app/views.py to match your SANDBOX developer credentials.