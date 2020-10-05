import requests
import time
import os

API_KEY = os.environ.get('FEC_ENV_TEST_API_KEY','DEMO_KEY')
API_ENVS = {
    'STAGE': 'https://api-stage.open.fec.gov/v1',
    'DEV': 'https://fec-dev-api.app.cloud.gov/v1',
}

QUERIES = {
    '/candidate/P80001571/?sort_nulls_last=true&candidate_status=C&candidate_status=N&office=H&office=P&per_page=1&page=1&sort_hide_null=false&api_key={0}&sort=name&sort_null_only=false'.format(API_KEY),
     '/candidate/P00003335/history/?sort_hide_null=true&page=1&sort=-two_year_period&sort_null_only=false&per_page=1&election_full=false&api_key={0}'.format(API_KEY),
    '/candidates/?sort_nulls_last=false&per_page=100&page=1&sort_hide_null=false&api_key={0}&sort=name&sort_null_only=false'.format(API_KEY),
    '/candidates/search/?sort=name&election_year=1984&per_page=1&incumbent_challenge=I&incumbent_challenge=O&sort_nulls_last=false&sort_null_only=true&sort_hide_null=false&page=1&office=H&api_key={0}'.format(API_KEY),
    '/committee/C00703975/history/2020/?sort_hide_null=false&sort_nulls_last=false&api_key={0}&designation=J&designation=B&sort=-cycle&per_page=1&sort_null_only=true&page=1&election_full=true'.format(API_KEY),
    '/election-dates/?sort=-election_date&per_page=1&sort_nulls_last=false&sort_null_only=false&page=1&sort_hide_null=false&api_key={0}'.format(API_KEY),
    '/filings/?sort=-receipt_date&per_page=1&sort_nulls_last=false&sort_null_only=false&sort_hide_null=false&page=1&api_key={0}&document_type=T&document_type=U&document_type=S'.format(API_KEY),
    '/schedules/schedule_a/by_state/?per_page=1&cycle=2020&hide_null=false&page=1&api_key={0}&sort=-total&sort_null_only=false&sort_nulls_last=false&sort_hide_null=false'.format(API_KEY),
    '/communication_costs/?page=1&sort_null_only=false&per_page=1&api_key={0}&support_oppose_indicator=O&sort_nulls_last=false&sort_hide_null=true'.format(API_KEY)
}


def test_env_consistency():
    time_sleep = 0.5 # upgraded key
    time_start = time.time()
    if API_KEY == 'DEMO_KEY':
        time_sleep = 90 # DEMO_KEY
    for q in QUERIES:
        old = {}
        new = {}
        for e, ev in API_ENVS.items():
            time_elapsed = time.time() - time_start
            time.sleep(time_sleep - time_elapsed)
            response = requests.get(ev + q).json()
            time_start = time.time()
            try:
                new = response['pagination']
            except KeyError:
                time_sleep = 3.6
                while 'pagination' not in response:
                    time.sleep(time_sleep)
                    response = requests.get(ev + q).json()
                new = response['pagination']
            if new['count'] >= 500000: # count > 500000 implies estimate, do not use
                continue
            elif old:
                assert new == old
            else:
                old = new



                
# https://api-stage.open.fec.gov/v1/efile/reports/presidential/?sort_hide_null=false&sort=-receipt_date&sort_null_only=false&page=1&api_key=DEMO_KEY&sort_nulls_last=false&per_page=14

# https://fec-dev-api.app.cloud.gov/v1/efile/reports/presidential/?sort_hide_null=false&sort=-receipt_date&sort_null_only=false&page=1&api_key=DEMO_KEY&sort_nulls_last=false&per_page=14
