import json
import csv
from wk_client.constants import EXAMPLE_DOC_REQUIREMENTS

from flask import Blueprint, request, g
from werkzeug.exceptions import BadRequest

from wk_client import auth, endpoints, models
from wk_client.auth_utils import create_user, create_user_data
from wk_client.logic import UserAccount
from wk_client.request_utils import time_now
from wk_client.settings import BANK_ACCOUNT
from wk_client.utils import get_date

bp = Blueprint('routes', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    return "Hello, World!"


@bp.route('/get_info', methods=('GET',))
def get_info():
    return json.dumps(endpoints.get_product_data())


@bp.route('/register', methods=('POST',))
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        try:
            username = data['username']
            password = data['password']
            account = data['bank_account']
        except KeyError:
            raise BadRequest()
        
        user = create_user(username, password, account)
        return json.dumps(user.username)


@bp.route('/test_login', methods=('GET', 'POST'))
@auth.login_required
def test_login():
    return json.dumps('Hello {}'.format(auth.username()))

#request log

@bp.route('/get_decision', methods=('GET', 'POST'))
@auth.login_required
def get_decision():
    if request.method == 'GET':
        return json.dumps(endpoints.get_decision(g.user, None))
    elif request.method == 'POST':
        data = request.get_json()
        if(data):
            dob = data['basic_questions']['date_of_birth']
            creditScore = data['credit_report']['score']
            #creditLimit = data['credit_report']['credit_limit']
            #creditUtilisation = data['credit_report']['credit_utilisation']
            #numberOfAccounts = data['credit_report']['number of accounts']
            #ageOfOldestAccount = data['credit_report']['age_of_oldest_account']
            #creditSearchesLast12m = data['credit_report']['credit_searches_last_12m']
            missedPayments = data['credit_report']['missed_payments_last_12m']
            username = g.user.username
            new_stuff = create_user_data(username, dob, creditScore, missedPayments)
        return json.dumps(endpoints.get_decision(g.user, data))


@bp.route('/request_funding', methods=('POST',))
@auth.login_required
def request_funding():
    """
    Request funding - Check that approval in question is still the active one. Balance is 0? (flexibiltiy?
    Returns:

    """
    data = request.get_json()
    amount = data['amount']
    approval_id = data['approval_reference']
    dt = time_now()
    user_account = UserAccount(g.user.id)
    funding, error = endpoints.request_funding(
        user_account,
        approval_id=approval_id,
        amount=amount,
        dt=dt
    )
    if error:
        raise BadRequest(error)
    else:
        schedule = {
            k.isoformat(): v for k, v in user_account.repayment_schedule_for_loan(funding).items()
        }

        return json.dumps({
            'funding_reference': funding.id,
            'repayment_account': BANK_ACCOUNT,
            'repayment_schedule': schedule
        })


@bp.route('/get_schedule', methods=('GET',))
@auth.login_required
def get_schedule():
    user_account = UserAccount(g.user.id)
    as_of = get_date(time_now())
    balance = user_account.balance(as_of)
    schedule = user_account.repayment_schedule_for_date(as_of)
    return json.dumps({
        'balance': balance,
        'schedule': {k.isoformat(): v for k, v in schedule.items()}
    })
