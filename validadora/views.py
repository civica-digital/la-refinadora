from flask import jsonify, request, render_template, url_for, Blueprint
from flask.ext.login import current_user, login_required
from validadora.forms import ValidateForm
from validadora.manager.manager import Manager
from uuid import uuid4
import json

REPOSITORIOS = ['i11', 'i12', 'i13', 'i14', 'u21', 'm31', 'm32', 'm33', 'c41', 'c42', 'c43', 'c44', 'c45', 'c46', 'n51', 'n52', 'l01', 'd01']

_M = Manager()
validators = _M.repo.list_validadores()

validations = Blueprint('validations', __name__)

@validations.route('/')
@validations.route('/index.htm')
@validations.route('/index.html')
@validations.route('/index', methods=['GET', 'POST'])
def index():
    form = ValidateForm()
    if form.validate_on_submit():
        return redirect('/validate')
    return render_template("index.html.haml", form=form, validators=validators)

@validations.route('/validate', methods=['POST'])
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

    callback = False
    if 'validation' in request.form.keys() and 'dcat_url' in request.form.keys():
        validation = request.form['validation']
        dcat_url = request.form['dcat_url']
        if not validation in [v.name for v in validators ]:# REPOSITORIOS:
            return jsonify({ "Error": "Validator not found."})
        if dcat_url != "": # TODO: Fix this later
            resp = jsonify({ "Error": "URL not valid."})

        callback = request.form['callback_url']
        if callback:
            callback = request.form['callback_url']
        work = _M.new_work(validation, dcat_url, callback)
        resp = {'id': work.wid }
    else:
        resp = { "Error": "Missing arguments. "}
    return jsonify(resp)

@validations.route('/validate/<task_id>', methods=['GET'])
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

@validations.route('/validators', methods=['GET'])
def get_validators():
    """
	Gets the list of possible validations.

	Returns:
       The list of possible validations
    """
    return jsonify([v.name for v in _M.repo.list_validadores()])


@validations.route('/validator/<validator_id>', methods=['GET'])
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


@validations.route('/users/current')
@login_required
def show_current_user():
    return jsonify({
        'email': current_user.email,
        'authenticated': current_user.authenticated,
        'api_key': current_user.api_key
    }), 200, {'Content-Type': 'application/json; charset=utf-8'}

@validations.route('/users/api_key', methods=['GET','POST'])
@login_required
def get_token():
    return jsonify({'api_key': current_user.api_key})

@validations.route('/users/api_key/new', methods=['GET'])
@login_required
def regenerate_token():
    current_user.api_key = uuid4().hex
    current_user.save()
    return jsonify({'api_key': current_user.api_key})


@validations.route('/echo', methods=['POST'])
def echo():
    print(json.loads(request.data.decode('UTF-8')))
    return 'OK'