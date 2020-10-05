import os
import sys
import argparse
import github3 as gh
from datetime import datetime, timezone


GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME', '')

if GITHUB_TOKEN and GITHUB_USERNAME:
    gh = gh.login(GITHUB_USERNAME, password=GITHUB_TOKEN)
    print('Login successful! Retrieving your issues\n')
else:
    sys.exit('Login failed! Verify that credentials are stored as environmental variables on your local system.')

utc_dt = datetime.now(timezone.utc)  # UTC time
today = utc_dt.astimezone()  # local time

REPOSITORIES = ['openFEC', 'fec-cms', 'fec-eregs', 'fecnet', 'fec-pattern-library', 'fec-accounts']

parser = argparse.ArgumentParser()
parser.add_argument(
    'milestone', metavar='milestone', type=str,
    help='A program to see the last time you commented on your open issue in a given sprint',
)
args = parser.parse_args()
for repo in REPOSITORIES:
    results = gh.issues_on('fecgov', repo, assignee=GITHUB_USERNAME, state='open')
    for result in results:
        report_string = ''
        commented = False
        if result.milestone and args.milestone in result.milestone.title:
            issue_url = result.html_url
            comments = result.comments(sort='desc')
            last_commented = result.created_at
            for comment in comments:
                if (str(comment.user) == GITHUB_USERNAME and
                    comment.updated_at >= last_commented):
                    last_commented = comment.updated_at
                    days_ago = today - last_commented
                    report_string = str(comment.user) + ' last commented ' +\
                        str(days_ago.days) + ' days ago on issue:\n' + str(issue_url) + '\n'
                    commented = True
            if not commented and '/pull/' not in issue_url:
                report_string = GITHUB_USERNAME + ' has not commented on issue:\n' + str(issue_url) + '\n'
        if report_string:
            print(report_string)
