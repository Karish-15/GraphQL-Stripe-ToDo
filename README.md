# dendrite-task

# Using Docker 
Run using `docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin -v ./realm_data:/opt/keycloak/data/import quay.io/keycloak/keycloak:22.0.4 start-dev --import-realm`

Easily import the realm from `./realm_data/realm.json` and create users from keycloak panel. 

# Run Flask app

While in the root directory of the repo, run the flask app using `python -m app`
