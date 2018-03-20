# Small Recommendation Engine Demo

App runs on Heroku and is available [here](https://recommendapp-test.herokuapp.com/) (First visit might be slow because Heroku needs to start the app first). 

## Run Locally

Make sure Postgres server is running. Create database and tables by running the following commands
```bash
cd data
sh create_database.sh
sh create_tables.sh
sh copy_data.sh
cd ..
```

Create new virtualenv, activate it and export the environment variables
```bash
python3.6 -m venv env
source env/bin/activate
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://localhost/recommend_app_test"
```
Install dependencies by running 
```bash
pip install -r requirements.txt
```
Finally, run the app
```bash
python app.py
```
and visit [localhost:5000](http://localhost:5000/).

## Possible Improvements

There are many ways the project could be improved if additional time was invested: 
* Add documentation. (I think most of functionality should be clear from checking the code.)
* Add tests. 
* Add a larger more realistic data in addition to the provided toy data.
* Improve and further test recommendation algorithm on a more realistic dataset. 
