#college crapplication

**A project by Matt Ramina and Matt Kumar**

Markov chains for college essays. Uses the wonderful [markovify](https://github.com/jsvine/markovify) by @jsvine.

Available at http://college-crapplication.appspot.com/

Why would you want to install this?

1. git clone
2. get Google App Engine SDK for python [here](https://cloud.google.com/appengine/downloads)
3. `pip install -r requirements.txt --target=lib`
4. create secret.py with one line: `essay_password = 'YOUR_PASSWORD_HERE'`
5. create project, change id in app.yaml, upload to GAE
6. add essays at /add_essay.html
7. view the madness at /