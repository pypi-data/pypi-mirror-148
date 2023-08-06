import sys
import argparse
import keyring
import logging
from keyring.errors import NoKeyringError
from keyrings.cryptfile.cryptfile import CryptFileKeyring

"""
This code uses keyring library to safety store username and password for
any services in the configured keyring. The current code implements
single command line able to add/remove/check entries from the keyring.

On linux ubuntu, the default keyring is gnome app name `seahorse`, but kwallet
is also
   pros:
     - unique and secure password storage solution
     - single interface to store credential
     - multiple backends and alternatives are possible (see doc
        at https://keyring.readthedocs.io/en/latest).
   cons:
     - library API exposes only basic authentication username/password.
       Usage of OAuth2.0/Certificates/ssh key requires some alternatives.
     - The keyring used in backend (ubuntu) is the gnome GUI that requires
       advanced configuration to be used without gui (see Linux headless notes
       here after)

The analysis only identified this library to store passwords.


Linux headless notes
--------------------
When Linux system is run without GUI, the keyring can still be used with dbus.

```shell
dbus-run-session -- sh
echo 'somecredstorepass' | gnome-keyring-daemon --unlock
```
(Source: https://keyring.readthedocs.io/en/latest/
    #using-keyring-on-headless-linux-systems)
"""
logger = logging.getLogger('drb-keyring')
init = False


def _log_kr_info(verbose: bool):
    if not verbose:
        return
    try:
        kr = keyring.get_keyring()
        logger.info(f'Using keyring backend {type(kr)}.')
    except Exception:
        logger.info(f'Keyring not prperly set.')


def _init_keyring_backed(verbose: bool):
    global init
    if init:
        _log_kr_info(verbose)
        return
    try:
        keyring.get_keyring()
        raise NoKeyringError()
    except NoKeyringError:
        kr = CryptFileKeyring()
        kr.keyring_key = 'a25Za/.?$'  # Warn: Same as PlaintextKeyring
        keyring.set_keyring(kr)
    _log_kr_info(verbose)
    init = True


def kr_add(service, username, password, verbose=False):
    _init_keyring_backed(verbose)
    if verbose:
        logger.info(f"Add keyring {service}/{username}.")
    keyring.set_password(service_name=service,
                         username=username,
                         password=password)
    return 0


def kr_remove(service, username, verbose=False):
    _init_keyring_backed(verbose)
    if kr_check(service, username, verbose) == 0:
        if verbose:
            logger.info(f"Remove keyring {service}/{username}.")
        keyring.delete_password(service, username)
        return 0
    else:
        return 1


def kr_get(service, username=None, verbose=False):
    _init_keyring_backed(verbose)
    if username is None:
        username = keyring.get_credential(service, None)
    return username, keyring.get_password(service, username)


def kr_check(service, username, verbose=False):
    _init_keyring_backed(verbose)
    credential = keyring.get_credential(service, username)
    if credential:
        if verbose:
            logger.info(f"Found {service}/{username}.")
        return 0
    else:
        if verbose:
            logger.info(f"Service {service}/{username} not found.")
        return 1


def add(args):
    return kr_add(args.service, args.username, args.password, args.verbose)


def remove(args):
    return kr_remove(args.service, args.username, args.verbose)


def check(args):
    return kr_check(args.service, args.username, args.verbose)


def get(args):
    return kr_get(args.service, args.username, args.verbose)


def main(argv) -> int:
    parser = argparse.ArgumentParser(description='Manage keyring commands.')

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    groups = parser.add_subparsers(help='commands')
    add_group = groups.add_parser('add', help="Add new keyring entry")
    add_group.add_argument('--service', metavar='SERVICE', type=str,
                           help='Service name')
    add_group.add_argument('--username', metavar='USERNAME', type=str,
                           help='Service connection username')
    add_group.add_argument('--password', metavar='PASSWORD', type=str,
                           help='Service connection password')
    add_group.set_defaults(func=add)

    remove_group = groups.add_parser('del', help="Remove keyring entry")
    remove_group.add_argument('del', action='store_true')
    remove_group.add_argument('--service', metavar='SERVICE', type=str,
                              help='Service name')
    remove_group.add_argument('--username', metavar='USERNAME', type=str,
                              help='Service connection username')
    remove_group.set_defaults(func=remove)

    check_group = groups.add_parser('check', help="check keyring status")
    check_group.add_argument('check', action='store_true')
    check_group.add_argument('--service', metavar='SERVICE', type=str,
                             help='Service name')
    check_group.add_argument('--username', metavar='USERNAME', type=str,
                             help='Service connection username')
    check_group.set_defaults(func=check)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
