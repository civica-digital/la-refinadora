from . import app
from flask import jsonify, request, render_template, url_for
from .forms import ValidateForm
from validadora.manager.manager import Manager

REPOSITORIOS = ['i11', 'i12', 'i13', 'i14', 'u21', 'm31', 'm32', 'm33', 'c41', 'c42', 'c43', 'c44', 'c45', 'c46', 'n51', 'n52', 'l01', 'd01']

_M = Manager()
validators = _M.repo.list_validadores()

@app.route('/')
@app.route('/index.htm')
@app.route('/index.html')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = ValidateForm()
    if form.validate_on_submit():
        return redirect('/validate')
    return render_template("index.html", form=form, validators=validators)

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
    print(request.form.values())
    print(validators)
    if 'validation' in request.form.keys() and 'dcat_url' in request.form.keys():
        validation = request.form['validation']
        dcat_url = request.form['dcat_url']
        if not validation in [v.name for v in validators ]:# REPOSITORIOS:
            return jsonify({ "Error": "Validator not found."})
        if dcat_url != "": # TODO: Fix this later
            resp = jsonify({ "Error": "URL not valid."})
        resp = _M.new_work(validation, dcat_url)
    else:
        resp = { "Error": "Missing arguments. "}
    return jsonify(resp)

@app.route('/validate/<task_id>', methods=['GET'])
def get_task(task_id):
    """
	Gets the status of the task validation id.

	Parameters:
		task_id - the task validation id

	Returns:
	The status of the task validation id
    """
    task_status = _M.report_work(task_id)
    # Get response from validator
    return jsonify({ "id_work": task_status })

@app.route('/validators/', methods=['GET'])
def get_validators():
    """
	Gets the list of possible validations.

	Returns:
       The list of possible validations
    """
    return jsonify([v.name for v in _M.repo.list_validadores()])


@app.route('/validator/<validator_id>', methods=['GET'])
def get_validator(validator_id):
    """

	:param validator_id:
	:return:
		Returns the description of a validator.

	Parameters:
		validator_id - the validator id

	Returns:
	The description of the validator
    """
    validator = {}
    # Get response from validator
    return validator