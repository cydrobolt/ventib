from web.views import *
from . import config
from flask import Flask

app = Flask('web')
app.secret_key = config.password

def add_routes(rule_endpoint_tuples):
    for rule, endpoint in rule_endpoint_tuples:
        print(rule, endpoint)
        app.add_url_rule(rule, view_func=endpoint, methods=["GET", "POST"])

add_routes([
    ('/', core.index),
    ('/register_login/', user.register_login),
    ('/register/', user.register),
    ('/login/', user.login),
    ('/user/', user.user),
    ('/420/blazeit/', user.new_text)
])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
