# CXFacturatieModule
Documentation on setting up and running a localized version of the FacturatieModule application.

Prerequisite:

````
1. Clone repo
1. Open repo
2. $ cd client
3. $ npm install

4. create auth0 dashboard & application (if not existent)
5. get the domain uri i.e:  dev-icv5ncp4ozs141pe.eu.auth0.com
6. get the clientId i.e:    3iW54zkwBpaEl3eDECbnyjLIPLVRUH1p
7. add these to the main.ts file under domain and clientId

(once server and client has been started)
1. create user in auth0
2. create profile for user with same email
(the application checks for the auth0 email and mirrors this with the profile)
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
