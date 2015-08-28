from app import app
from flask import jsonify, request, render_template, url_for
from .forms import ValidateForm
# from repositorio import repositorios
from validators import url
from validator import validate_catalog

REPOSITORIOS = ['i11', 'i12', 'i13', 'i14', 'u21', 'm31', 'm32', 'm33', 'c41', 'c42', 'c43', 'c44', 'c45', 'c46', 'n51', 'n52', 'l01', 'd01']

@app.route('/')
@app.route('/index.htm')
@app.route('/index.html')
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = ValidateForm()
	if form.validate_on_submit():
		return redirect('/validate')
	return render_template("index.html", form=form)

@app.route('/validate', methods=['POST'])
def validate():
	"""
	Validates a data catalog.

	Parameters:
		validation - validator key
		dcat_url - URL of the DCAT object

	Returns:
	The id of the validation task id
    """
    resp = {}
	if 'validation' in request.args and 'dcat_url' in request.args:
		validation = request.form['validation']
		dcat_url = request.form['dcat_url']
		if not validation in REPOSITORIOS:
			resp = { "Error": "Validator not found."}
		if url(dcat_url) == False:
			resp = { "Error": "URL not valid."}
		resp = validate_catalog(validation, dcat_url)
	else:
		resp = { "Error": "Missing arguments. "}
	return jsonify(resp)

@app.route('/validate/<int:task_id>', methods=['GET'])
def get_task(task_id):
	"""
	Gets the status of the task validation id.

	Parameters:
		task_id - the task validation id

	Returns:
	The status of the task validation id
    """
    task_status = {}
	# Get response from validator
	return task_status

@app.route('/validators/', methods=['GET'])
def get_validators(task_id):
	"""
	Gets the list of possible validations.

	Returns:
	The list of possible validations
    """
    validators = {}
	# Get response from validator
	return validators

@app.route('/validator/<validator_id>', methods=['GET'])
def get_validator(validator_id):
	"""
	Returns the description of a validator.

	Parameters:
		validator_id - the validator id

	Returns:
	The description of the validator
    """
    validator = {}
	# Get response from validator
	return validator