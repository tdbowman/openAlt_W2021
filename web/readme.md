
You will need these Python modules:
* pip install Flask
* pip install Flask-MySQLdb
* pip install virtualenv

You will need to create a virtual environment. I believe you only need do this once.  
This should be done inside `crossrefEventData/web/`  
`py -m venv env`   
It will create a folder called env.

If you have all the other modules installed, you can run:  
`python app.py` - always do this from the terminal. In my experience it is buggy under Vscode.

Now go to http://127.0.0.1:5000/