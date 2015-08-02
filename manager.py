'''
Python script for uploading/downloading scripts for use with the game Screeps.

http://support.screeps.com/hc/en-us/articles/203022612-Commiting-scripts-using-direct-API-access

Usage:

    #
    # general help/usage
    #

    python3 manager.py --help

    #
    # retrieve all scripts from the game and store them
    # in the folder "some_folder"
    #

    python3 manager.py from_game some_folder

    #
    # send all *.js files to the game
    #

    python3 manager.py to_game some_folder

WARNING: Use at your own risk! Make backups of all your game content!

'''

import sys
import os
import argparse
import json

import requests
from requests.auth import HTTPBasicAuth

SCREEPS_ENDPOINT = 'https://screeps.com/api/user/code'

USER_ENV = 'SCREEPS_USER'
PASSWORD_ENV = 'SCREEPS_PASSWORD'

TO_SCREEPS = 'to_game'
FROM_SCREEPS = 'from_game'


def get_user_from_env():

    user = os.environ.get('SCREEPS_USER')

    if not user:
        print('You must provide a username, i.e. export '
              '{}=<your email address>'.
              format(USER_ENV))
        sys.exit()

    return user


def get_password_from_env():

    password = os.environ.get('SCREEPS_PASSWORD')

    if not password:
        print('You must provide a password, i.e. export {}=<your password>'.
              format(PASSWORD_ENV))
        sys.exit()

    return password


def get_data(user, password):

    print('Retrieving data...')

    response = requests.get(SCREEPS_ENDPOINT,
                            auth=HTTPBasicAuth(user, password))

    response.raise_for_status()

    data = response.json()

    if data['ok'] != 1:
        raise Exception()

    return data


def send_data(user, password, modules):

    auth = HTTPBasicAuth(user, password)
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    data = {'modules': modules}

    resp = requests.post(SCREEPS_ENDPOINT,
                         data=json.dumps(data),
                         headers=headers,
                         auth=auth)

    resp.raise_for_status()


def check_for_collisions(target_folder, modules):

    for module in modules:

        target = os.path.join(target_folder, '{}.js'.format(module))

        if os.path.exists(target):

            print('File {} exists.'.format(target))
            print('Specify --force to overwrite. Aborting...')
            sys.exit()


def main():

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('operation',
                        choices=(TO_SCREEPS, FROM_SCREEPS),
                        help='')
    parser.add_argument('destination', help='')
    parser.add_argument('--user', help='')
    parser.add_argument('--password', help='')
    parser.add_argument('--force', action='store_const', const=True,
                        help='force overwrite of files in an existing folder')
    parser.add_argument('--merge', action='store_const', const=True,
                        help='merge scripts into a single main.js module')

    args = parser.parse_args()

    user = args.user if args.user else get_user_from_env()
    password = args.password if args.password else get_password_from_env()

    target_folder = os.path.abspath(args.destination)

    if args.operation == FROM_SCREEPS:

        data = get_data(user, password)

        # does the folder exist?
        if not os.path.isdir(target_folder):

            # no - create it
            print('Creating new folder "{}"...'.format(target_folder))

            os.makedirs(target_folder)

        else:

            # yes - check for collisions (unless --force was specified)
            if not args.force:

                print('Checking for collisions...')

                check_for_collisions(target_folder, data['modules'])

                print('Ok, no collisions.')

        # for each module, create a corresponding filename and put it in
        # the target folder

        for module in data['modules']:

            target = os.path.join(target_folder, '{}.js'.format(module))

            with open(target, 'w') as fout:
                fout.write(data['modules'][module])

    else:

        modules = {}

        for root, folders, files in os.walk(target_folder):

            folders[:] = []

            for target_file in files:

                name, ext = os.path.splitext(target_file)

                if ext != '.js':
                    continue

                with open(os.path.join(root, target_file), 'r') as fin:
                    modules[name] = fin.read()

        if args.merge:

            merge_modules(modules)

        # upload modules
        send_data(user, password, modules)


def generate_header(filename):

    return '''
// {border}
// {name}
// {border}
'''.format(border='-' * 25, name=filename)


def merge_modules(modules):

    keys = [x for x in modules.keys()]

    keys.sort()

    merged = ''

    for key in keys:

        merged = merged + generate_header(key) + modules[key]

        del(modules[key])

    modules['main.js'] = merged

if __name__ == '__main__':

    main()
