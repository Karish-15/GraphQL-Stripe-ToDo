from flask import request, jsonify, g, redirect, render_template, session
from flask_oidc import OpenIDConnect
from oauth2client.client import OAuth2Credentials
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, ObjectType

from api import app, db, queries
from api.queries import resolve_all_todos
from api.mutations import create_todo_resolver, delete_todo_resolver, update_todo_resolver
from api.models import ToDo, UserPro
from api.graphql_queries import graphql_url, query_allToDo, mutation_createToDo, mutation_deleteToDo, mutation_updateToDo

import json, requests, stripe

app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_USER_INFO_ENABLED': True,
    'OIDC_OPENID_REALM': 'test',
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
})

oidc = OpenIDConnect(app)

query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field("listTodos", resolve_all_todos)
mutation.set_field("createToDo", create_todo_resolver)
mutation.set_field("deleteToDo", delete_todo_resolver)
mutation.set_field("updateToDo", update_todo_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)

@app.route('/')
def homepage():
    if oidc.user_loggedin:
        resp = requests.post(url=graphql_url, json={"query": query_allToDo, "user_id": session['oidc_auth_profile'].get('sub')}, headers={"Authorization": "Bearer " + oidc.get_access_token()})
        ls = resp.json()['data']['listTodos']['todos'] if resp.status_code == 200 else []
        pro_license = True if UserPro.query.filter_by(id=session['oidc_auth_profile'].get('sub')).first() else False
        return render_template('user_logged_in_home.html', user=session['oidc_auth_profile'].get('preferred_username'), todo_list = ls, pro_license = pro_license)

    return render_template('homepage.html', description = "A to-do app")

@app.route('/private')
@oidc.require_login
def hello_me():
    return redirect('/')

@app.route('/logout')
@oidc.require_login
def logout():
    refresh_token = oidc.get_refresh_token()
    oidc.logout()
    if refresh_token is not None:
        keycloak_openid.logout(refresh_token)
    oidc.logout()
    g.oidc_id_token = None
    return redirect(
        "http://localhost:5000" + '/protocol/openid-connect/logout?redirect_uri=' + "localhost:5000/")

@app.route("/graphql", methods=["POST"])
@oidc.accept_token(scopes='openid')
def graphql_server():
    data = request.get_json()
    user_id = data.get('user_id')
    success, result = graphql_sync(
        schema,
        data,
        context_value={'request': request, 'user_id': user_id},
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

@app.route('/create_todo', methods=['POST', 'GET'])
@oidc.require_login
def create_todo():
    error = ""
    if request.method == 'POST':

        title=request.form['title']
        description=request.form['description']
        author_id=str(session['oidc_auth_profile'].get('sub'))
        image_url = request.form['image_url'] if request.form.get('image_url') else "Not Available"

        query_create = mutation_createToDo(title, description, image_url)

        resp = requests.post(url=graphql_url, json={"query": query_create, 'user_id': author_id}, headers={"Authorization": "Bearer " + oidc.get_access_token()})

        if resp.status_code == 200:
            return redirect('/')

        error = "Invalid details, try again"

    user_id = session['oidc_auth_profile'].get('sub')
    user_data = UserPro.query.filter_by(id=user_id).first()

    if(user_data):
        return render_template('create_todo_pro.html', eroor=error)

    return render_template('create_todo_nonpro.html', error=error)

@app.route('/delete_todo/<todo_id>', methods=['GET'])
@oidc.require_login
def delete(todo_id):
    query_delete = mutation_deleteToDo(todo_id)

    resp = requests.post(url=graphql_url, json={"query": query_delete, "todo_id": todo_id, "user_id": session['oidc_auth_profile'].get('sub')}, headers={"Authorization": "Bearer " + oidc.get_access_token()})
    print(resp.json())
    return redirect('/')

@app.route('/update_todo/<todo_id>', methods=['POST', 'GET'])
@oidc.require_login
def update(todo_id):
    error = ""
    if request.method == 'POST':
        title=request.form['title']
        description=request.form['description']
        image_url = request.form['image_url'] if request.form.get('image_url') else "Not Available"

        query_update = mutation_updateToDo(todo_id, title, description, image_url)

        resp = requests.post(url=graphql_url, json={"query": query_update, "todo_id": todo_id, "user_id": session['oidc_auth_profile'].get('sub')}, headers={"Authorization": "Bearer " + oidc.get_access_token()})
        if resp.status_code == 200:
            return redirect('/')

        error = "Invalid details, try again"

    todo = ToDo.query.filter_by(id=todo_id).first() if ToDo.query.filter_by(id=todo_id).first() else None

    if session['oidc_auth_profile'].get('sub') != todo.author_id:
        return redirect('/')
    if todo is None:
        return redirect('/')

    pro_license = True if UserPro.query.filter_by(id=session['oidc_auth_profile'].get('sub')).first() else False
    return render_template('update_todo.html', error=error, todo = todo, pro_license = pro_license)

@app.route('/create-checkout-session', methods=['POST'])
@oidc.require_login
def create_checkout_session():
    user_id = session['oidc_auth_profile'].get('sub')

    # User already has pro license
    if UserPro.query.filter_by(id=user_id).first():
        return redirect('/')

    YOUR_DOMAIN = 'http://localhost:5000'
    stripe.api_key = 'sk_test_51O0rdqSAx2prmQegmfQK9gsyHU0ki4XCNbbXEQXZ7pp01VFnhQlSRhnZ0UGZAhLlp49DMOIKfsjJPcRCsnbqXT4q00HMa64fF4'

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': "price_1O0roRSAx2prmQegG4Y5QE4V",
            'quantity': 1,
        }],
        client_reference_id=session['oidc_auth_profile'].get('sub'),
        mode='payment',
        success_url=YOUR_DOMAIN + "/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=YOUR_DOMAIN + '/cancel',
        
    )

    return redirect(checkout_session.url, code=303)

@app.route('/success')
def success():
    session_stripe = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    user_id = session_stripe['client_reference_id']

    user = UserPro(id=user_id, pro_license=True)
    db.session.add(user)
    db.session.commit()
    return redirect('/')
    

@app.route('/cancel')
@oidc.require_login
def cancel():
    return redirect('/')

@app.route('/get_pro')
@oidc.require_login
def get_pro():
    return render_template('checkout.html')




if __name__ == '__main__':
    # db.create_all()
    app.run()

