# USAGE
# Start the server:
# 	python run_front_server.py
# Submit a request via Python:
#	python simple_request.py
import os

import dill
import pandas as pd

# import the necessary packages

dill._dill._reverse_typemap['ClassType'] = type
#import cloudpickle
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
	# load the pre-trained model
	global model
	with open(model_path, 'rb') as f:
		model = dill.load(f)
	print(model)

modelpath = "/app/app/models/logreg_pipeline.dill"
#modelpath = "C:/Users/admin/Desktop/ML/logreg_pipeline.dill"
load_model(modelpath)

@app.route("/", methods=["GET"])
def general():
	return """Welcome to prediction process. Please use 'http://<address>/predict' to POST"""

@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}
	dt = strftime("[%Y-%b-%d %H:%M:%S]")
	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":

		ph, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity = "", "", "", "", "", "", "", "", ""

		request_json = flask.request.get_json()
		if request_json["ph"]:
			ph = request_json['ph']

		if request_json["Hardness"]:
			Hardness = request_json['Hardness']

		if request_json["Solids"]:
			Solids = request_json['Solids']

		if request_json["Chloramines"]:
			Chloramines = request_json['Chloramines']

		if request_json["Sulfate"]:
			Sulfate = request_json['Sulfate']

		if request_json["Conductivity"]:
			Conductivity = request_json['Conductivity']

		if request_json["Organic_carbon"]:
			Organic_carbon = request_json['Organic_carbon']

		if request_json["Trihalomethanes"]:
			Trihalomethanes = request_json['Trihalomethanes']

		if request_json["Turbidity"]:
			Turbidity = request_json['Turbidity']

		logger.info(f'{dt} Data: ph={ph}, Hardness={Hardness}, Solids={Solids}, Chloramines={Chloramines}, Sulfate={Sulfate}, Conductivity={Conductivity}, Organic_carbon={Organic_carbon}, Trihalomethanes={Trihalomethanes}, Turbidity={Turbidity}')

		try:
			preds = model.predict_proba(pd.DataFrame({"ph": [ph],
												  "Hardness": [Hardness],
												  "Solids": [Solids],
												  "Chloramines": [Chloramines],
												  "Sulfate": [Sulfate],
												  "Conductivity": [Conductivity],
												  "Organic_carbon": [Organic_carbon],
												  "Trihalomethanes": [Trihalomethanes],
												  "Turbidity": [Turbidity]}))
		except AttributeError as e:
			logger.warning(f'{dt} Exception: {str(e)}')
			data['predictions'] = str(e)
			data['success'] = False
			return flask.jsonify(data)

		data["predictions"] = preds[:, 1][0]
		# indicate that the request was a success
		data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading the model and Flask starting server..."
		"please wait until server has fully started"))
	port = int(os.environ.get('PORT', 8180))
	app.run(host='127.0.0.1', debug=True, port=port)
