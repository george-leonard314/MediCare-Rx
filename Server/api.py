import connexion
import sys
sys.path.append('/home/g/Programming Asignment/MediCare-Rx')
from config import CONFIG

app = connexion.FlaskApp(__name__)
app.add_api("api.yml")    
app.run(host=CONFIG["server"]["listen_ip"], port=CONFIG["server"]["port"], debug=CONFIG["server"]["debug"])