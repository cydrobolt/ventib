from views import *
from flask import Flask

app = Flask('Ventib')

def add_routes(rule_endpoint_tuples):
    for rule, endpoint in rule_endpoint_tuples:
        app.add_url_rule(rule, endpoint, methods=["GET", "POST"])

add_routes([
    ('/', core.index)
])
