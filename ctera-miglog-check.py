#!/usr/bin/python3
#v1.0.0 - Parse migration errors for  migration jobs

import click
import logging
from getpass import getpass
import hashlib
import csv
import os
from datetime import datetime
from cterasdk import Gateway, config, CTERAException

# ignore TLS error warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@click.command(help="Check for migration log errors")
@click.option("-a", "--address", required=True, help="Edge filer FQDN")
@click.option("-u", "--admin", required=True, help="Edge filer admin user")
@click.option("-j", "--job", required=True, help="Migration job number")
@click.option("--debug", is_flag=True, help="debug")
def miglogcheck(address,admin,job,debug):

    config.Logging.get().setLevel(logging.INFO)
    if debug:
        config.Logging.get().setLevel(logging.DEBUG)

    session = start_session(address,admin)
    
    try:
        errormessages = checkjob(session,job)
    except CTERAException as error:
        print(error)
    teardown(session)
    
    parseerrors(errormessages,address.split('.')[0])

def start_session(address,admin):
    config.http['ssl'] = 'Trust'

    password = 'Password1!'
    #password = getpass('Enter Password (%s): ' % admin)
    try:
        session = Gateway(address, https=True)
        session.login(admin, password)
    except CTERAException as error:
        print(error)
        quit()
    return session


def checkjob(session,job):
    get_list = ['status','config']

    info = session.get_multi('', get_list)

    session.telnet.enable(hashlib.sha1(
        (info.status.device.MacAddress + '-' + info.status.device.runningFirmware).encode('utf-8')).hexdigest()[:8])
    try:
        path = '/var/volumes/vol1/.ctera/migrationlogs/jobs/'+job+'/'
        print(path)
        errormessages = session.shell.run_command(f'grep sender {path}migration.log | grep rsync | grep -v vanished')
    except CTERAException as error:
        print(error)
        quit()
    session.telnet.disable()
    return errormessages

def parseerrors(errormessages,address):
    #Create Output File
    create_dir('output')
    
    filers_path = os.path.join('output', datetime.now().strftime(address + '-%Y_%m_%d-%H-%M') + '.csv')
    with open(filers_path, 'w', newline='\n', encoding='utf-8') as outputcsv:
        writer = csv.DictWriter(outputcsv, fieldnames=["Path","Error"])
        writer.writeheader()
        
        for message in errormessages.split('\n'):
            errors = {'Path':message.split('"')[1],'Error':message.split(': ')[-1]}
            writer.writerow(errors)
            
    print(f'\n\tLog File: {filers_path}\n')

def create_dir(output):
    output = os.path.expandvars(output)
    if not os.path.exists(output):
        os.makedirs(output)
    if not os.path.isdir(output):
        raise click.BadParameter('"%s" is not a folder' % os.path.basename(output), param=output, param_hint='-o')


def teardown(session):
    session.logout()

if __name__ == '__main__':
    miglogcheck()