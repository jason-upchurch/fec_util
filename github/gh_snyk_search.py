import os
import re
import sys
import github3 as gh
from datetime import datetime


GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME', '')

if GITHUB_TOKEN and GITHUB_USERNAME:
    gh = gh.login(GITHUB_USERNAME, password=GITHUB_TOKEN)
    print('Login successful! Retrieving snyk issues\n')
else:
    sys.exit('Login failed! Verify that credentials are stored as environmental variables on your local system.')

today = datetime.today().date()
results = gh.search_issues(
    "snyk in:title is:open type:issue user:fecgov -repo:fecgov/fecfile-online -repo:fecgov/fecfile-ImageGenerator"
)
for result in results:
    if re.match(r'[\(\[]snyk.*due.*', result.issue.title.lower()):
        due_date = re.search("([0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4})", result.issue.title)
        if due_date:
            due_date = due_date[0]
            try:
                due_date = datetime.strptime(due_date, '%m/%d/%Y').date()
            except:
                due_date = datetime.strptime(due_date, '%m/%d/%y').date()
            days_to_resolve = due_date - today
        else:
            days_to_resolve = '*** undetermined ***'
    
        print('ISSUE: ', result.issue.html_url)
        print('VULNERABILITY: ', result.issue.title)
        print('CURRENT MILESTONE: ', result.issue.milestone)
        print('DAYS TO RESOLVE: ', days_to_resolve.days, '\n')



    
