#!/usr/bin/env python

import os
from mlstatus import update_git_repos
from mlstatus import generate_status_table
import datetime
import time

if not os.path.exists('output'):
    os.mkdir('output')

git_repo_dirname='git_repos'

while True:
    update_git_repos(git_repo_dirname=git_repo_dirname)

    timestamp=str(datetime.datetime.now()).split('.')[0]
    DF=generate_status_table(local=True,remote=True,local_changes=False,git_repo_dirname=git_repo_dirname)

    print(DF.to_string(index=False))
    with open('output/status.txt','w') as f:
        txt='Updated: {}\n\n'.format(timestamp)
        txt+=DF.to_string(index=False)
        f.write(txt)
    with open('output/status.html','w') as f:
        html='<p>Updated: {}</p>\n'.format(timestamp)
        html+=DF.to_html(index=False)
        f.write(html)
    
    time.sleep(60)