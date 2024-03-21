import connexion

from config import CONFIG

app = connexion.FlaskApp(__name__)
app.add_api("pharm-api.yml")
app.run(host=CONFIG["server"]["listen_ip"], port=CONFIG["server"]["port"], debug=CONFIG["server"]["debug"])