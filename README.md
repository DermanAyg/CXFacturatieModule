# CXFacturatieModule
Documentation on setting up and running a localized version of the FacturatieModule application.

Prerequisite:

````
1. Clone repo
1. Open repo
2. $ cd client
3. $ npm install
````

## Client

### End2End testing

````
1. open repo
2. cd client
3. npm install
4. npx cypress open
````

### Starting and/or building

````
a. npm run start
b. npm run startandbuild
c. npm run build
````


## Server

### Virtual env

````
1. $ cd server\env\scripts
2. $ activate
3. (env) $ cd ../../
4. (env) $ pip install -r requirements.txt
5. check if you have correct packages: pip list
````

### Testing
 ###### # Note: ENV must be running whilst performing the following.

````
(env) $ pytest
````


### Starting
###### # Note: Database must be populated with data, visit the FastAPI swagger docs and populate database.

````
(env) $ uvicorn main:app --reload
````
