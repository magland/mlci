import subprocess
import json
import pandas as pd
import os

def get_projects():
    projects0=[
        dict(ptype='node',name='ephys-viz',github_user='flatironinstitute',conda_channel='flatiron'),
        dict(ptype='node',name='kbclient',github_user='magland'),
        dict(ptype='node',name='kbucket',conda=True,github_user='flatironinstitute',npm_name='@magland/kbucket',conda_channel='flatiron'),
        dict(ptype='node',name='lariclient',github_user='magland'),
        dict(ptype='node',name='mlclient',github_user='magland'),
        dict(ptype='node',name='mountainlab',github_name='mountainlab-js',github_user='flatironinstitute',conda_channel='flatiron'),
        dict(ptype='node',name='epoxy',github_name='mountainlab-js',github_user='flatironinstitute',npm_name='@magland/epoxy'),
        dict(ptype='python',name='ml_ephys',github_user='magland',conda_channel='flatiron'),
        dict(ptype='python',name='ml_ms4alg',github_user='magland',conda_channel='flatiron'),
        dict(ptype='python',name='ml_pyms',github_user=None,conda_channel='flatiron',pypi_name=None),
        dict(ptype='python',name='ml_ms3',github_user=None,conda_channel='flatiron',pypi_name=None),
        dict(ptype='python',name='mountainlab_pytools',github_user='magland',conda_channel='flatiron'),
        dict(ptype='python',name='mlprocessors',github_user='flatironinstitute',conda_channel='flatiron'),
        dict(ptype='python',name='spikeforestwidgets',github_user='magland',conda_channel='flatiron'),
        dict(ptype='other',name='mldevel',github_user='magland'),
        dict(ptype='other',name='mountainsort_examples',github_user='flatironinstitute')
    ]
    projects=[]
    for P0 in projects0:
        P=dict(
            name=P0['name']
        )
        if P0['github_user']:
            if 'github_name' not in P0:
                P0['github_name']=P0['name']
            P['local']=dict(
                name=P0['github_name']
            )
            if P0['github_name']:
                P['github']=dict(
                    name=P0['github_name'],
                    user=P0['github_user'],
                )
        if P0['ptype'] == 'node':
            if 'npm_name' not in P0:
                P0['npm_name']=P0['name']
            if P0['npm_name']:
                P['npm']=dict(
                    name=P0['npm_name']
                )
        elif P0['ptype'] == 'python':
            if 'pypi_name' not in P0:
                P0['pypi_name']=P0['name']
            if P0['pypi_name']:
                P['pypi']=dict(
                    name=P0['pypi_name']
                )
        if 'conda_channel' in P0:
            if 'conda_name' not in P0:
                P0['conda_name']=P0['name']
            if P0['conda_name']:
                P['conda']=dict(
                    name=P0['conda_name'],
                    channel=P0['conda_channel']
                )
        projects.append(P)
            
    '''
    projects=[
        dict(
            name='epoxy',
            local=dict(name='epoxy'),
            github=dict(name='epoxy',user='magland'),
            npm=dict(name='@magland/epoxy')
        ),
        dict(
            name='mountainlab',
            local=dict(name='mountainlab-js'),
            github=dict(name='mountainlab-js',user='flatironinstitute'),
            conda=dict(name='mountainlab',channel='flatiron'),
            npm=dict(name='mountainlab')
        ),
        dict(
            name='kbucket',
            local=dict(name='kbucket'),
            github=dict(name='kbucket',user='flatironinstitute'),
            conda=dict(name='kbucket',channel='flatiron'),
            npm=dict(name='@magland/kbucket')
        ),
        dict(
            name='mountainlab_pytools',
            local=dict(name='mountainlab_pytools'),
            github=dict(name='mountainlab_pytools',user='magland'),
            conda=dict(name='mountainlab_pytools',channel='flatiron'),
            pypi=dict(name='mountainlab_pytools')
        )
    ]
    for name in ['ml_ephys','ml_ms4alg','ml_spyking_circus']:
        projects.append(dict(
            name=name,
            local=dict(name=name),
            github=dict(name=name,user='magland'),
            conda=dict(name=name,channel='flatiron'),
            pypi=dict(name=name)
        ))
    '''
    return projects

def find_latest_conda_package(package_name,*,channel=None):
    opts=[]
    if channel:
        opts.append('-c {}'.format(channel))
    cmd='conda search --json {} {}'.format(' '.join(opts),package_name)
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stderr:
        print(result.stderr)
    if not result.stdout:
        print('Not found on conda: '+cmd)
        return None
    obj=json.loads(result.stdout.decode())
    if package_name in obj:
        return obj[package_name][-1]
    else:
        return None
    
# need to pip install yolk3k
def find_latest_pypi_package(package_name):
    opts=[]
    cmd='yolk -V {} {}'.format(' '.join(opts),package_name)
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stderr:
        print(result.stderr)
    if not result.stdout:
        print('Not found on pypi: '+cmd)
        return None
    lines=result.stdout.decode().split('\n')
    lines=list(filter(None, lines)) # remove empty lines
    line=lines[-1]
    version=line.split()[1]
    return dict(
        version=version
    )

# need to install yarn
def find_latest_npm_package(package_name):
    cmd='yarn info {} --json version'.format(package_name)
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stderr:
        print(result.stderr)
    if not result.stdout:
        print('Not found on npm: '+cmd)
        return None
    obj=json.loads(result.stdout.decode())
    return dict(
        version=obj['data']
    )

from .get_setup_py_data import get_setup_py_data
def get_git_status(dirname):
    cmd='git status -s'
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dirname)
    if result.stderr:
        print(result.stderr)
    if not result.stdout.decode():
        return ''
    return result.stdout.decode()

def find_local_project(package_name,*,git_repo_dirname):
    basedir=git_repo_dirname
    dirname=basedir+'/'+package_name
    package_json_fname=dirname+'/package.json'
    setup_py_fname=dirname+'/setup.py'
    ret={}
    ret['status']=get_git_status(dirname)
    ret['modifications']='{}'.format(len(ret['status'].split('\n'))-1)
    if ret['modifications']=='0':
        ret['modifications']=''
    if os.path.exists(package_json_fname):
        with open(package_json_fname) as f:
            obj=json.load(f)
        ret['version']=obj['version']
    elif os.path.exists(setup_py_fname):
        obj=get_setup_py_data(dirname)
        if obj:
            ret['version']=obj['version']
        else:
            return 'problem'
    else:
        return None
    return ret

def get_local_info(projects,*,git_repo_dirname):
    for P in projects:
        print(P['name'])
        if 'local' in P:
            project=find_local_project(P['local']['name'],git_repo_dirname=git_repo_dirname)
            if project:
                P['local_version']=project['version']
                P['local_status']=project['status']
                P['local_modifications']=project['modifications']
            else:
                P['local_version']='not found'
    print('done.')
    
def get_remote_info(projects):
    for P in projects:
        print(P['name'])
        if 'conda' in P:
            package=find_latest_conda_package(P['conda']['name'],channel=P['conda']['channel'])
            if package:
                P['conda_version']=package['version']
            else:
                P['conda_version']='not found'
        if 'pypi' in P:
            package=find_latest_pypi_package(P['pypi']['name'])
            if package:
                P['pypi_version']=package['version']
            else:
                P['pypi_version']='not found'
        if 'npm' in P:
            package=find_latest_npm_package(P['npm']['name'])
            if package:
                P['npm_version']=package['version']
            else:
                P['npm_version']='not found'
    print('done.')
    
def get_data_frame(projects,*,local,remote,local_changes):
    columns=['name']
    if local:
        columns.append('local_version')
        if local_changes:
            columns.append('local_modifications')
    if remote:
        columns.extend(('conda_version','pypi_version','npm_version'))
    DF1=pd.DataFrame(projects,columns=columns)
    DF1.set_index('name')
    DF1 = DF1.replace(float('nan'), '', regex=True)
    return DF1

def generate_status_table(*,local=True,remote=False,local_changes=True,git_repo_dirname):
    projects=get_projects()
    if local:
        get_local_info(projects,git_repo_dirname=git_repo_dirname)
    if remote:
        get_remote_info(projects)
    DF=get_data_frame(projects,local=local,remote=remote,local_changes=local_changes)
    return DF

def run_command(cmd,cwd=None):
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd=cwd)
    if result.stdout:
        print(result.stdout.decode())
    if result.stderr:
        print(result.stderr.decode())

def update_git_repos(git_repo_dirname):
    projects=get_projects()
    if not os.path.exists(git_repo_dirname):
        os.mkdir(git_repo_dirname)
    for P in projects:
        print(P['name'])
        if 'github' in P:
            gh=P['github']
            url='https://github.com/{}/{}'.format(gh['user'],gh['name'])
            repo_dirname=git_repo_dirname+'/'+gh['name']
            if not os.path.exists(repo_dirname):
                cmd='git clone {} {}'.format(url,repo_dirname)
                run_command(cmd)
            cmd='git pull'
            run_command(cmd,cwd=repo_dirname)