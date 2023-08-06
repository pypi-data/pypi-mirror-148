#
#  Copyright (c) 2018-2022 Renesas Inc.
#  Copyright (c) 2018-2022 EPAM Systems Inc.
#
"""aos-keys main module."""

import argparse
import logging
import sys

from aos_keys.actions import (
    UserType,
    new_token_user,
    convert_pkcs12_file_to_pem,
    install_root_ca,
    print_user_info,
    install_user_certificate,
)
from aos_keys.common import DEFAULT_CREDENTIALS_FOLDER, console, AosKeysError

try:
    from importlib.metadata import version  # noqa: WPS433
except ImportError:
    import importlib_metadata as version  # noqa: WPS433

logger = logging.getLogger(__name__)

_COMMAND_INFO = 'info'
_COMMAND_NEW_USER = 'new-user'
_COMMAND_TO_PEM = 'to-pem'
_COMMAND_INSTALL_ROOT_CA = 'install-root'
_COMMAND_INSTALL_CLIENT_CERT = 'install-cert'


def _args_to_cert_path(command_params) -> str:
    """
    Get path to certificate from received command line parameters.

    Args:
        command_params: Parameters received from argparse

    Raises:
            AosKeysError: If not set any parameters.

    Returns:
        parsed full path to certificate
    """
    if command_params.user_type:
        return str(UserType.from_input(command_params.user_type).default_user_certificate_path)
    elif command_params.cert_file_name:
        return command_params.cert_file_name

    raise AosKeysError(
        'User certificate not specified.',
        help_text='Use one of --oem, --sp, --admin, or -c key',
    )


def _parse_args():
    """User arguments parser.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Work with keys. Create new keys, receive certificates, show info',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parser = parser.add_subparsers(title='Commands')
    new_user_command = sub_parser.add_parser(_COMMAND_NEW_USER, help='Create new key and receive certificate')
    new_user_command.set_defaults(which=_COMMAND_NEW_USER)
    new_user_command.add_argument(
        '-o',
        '--output-dir',
        dest='output_dir',
        default=DEFAULT_CREDENTIALS_FOLDER,
        help='Output directory to save certificate.',
    )

    new_user_command.add_argument(
        '-d',
        '--domain',
        dest='register_domain',
        default='aoscloud.io',
        help='Aos Cloud domain to sign user certificate.l',
    )

    new_user_command.add_argument(
        '-t',
        '--token',
        dest='token',
        help='Cloud authorization token.',
    )

    new_user_command.add_argument(
        '-oem',
        '--oem',
        dest='user_type',
        action='store_const',
        const='oem',
        help='Create OEM user key/certificate.',
    )

    new_user_command.add_argument(
        '-s',
        '--sp',
        dest='user_type',
        action='store_const',
        const='sp',
        help='Create Service Provider user key/certificate.',
    )

    new_user_command.add_argument(
        '-a',
        '--admin',
        dest='user_type',
        action='store_const',
        const='admin',
        help='Create ADMIN user key/certificate.',
    )

    new_user_command.add_argument(
        '-e',
        '--ecc',
        action='store_true',
        help='Create ECC key instead of RSA',
    )

    info_command = sub_parser.add_parser(_COMMAND_INFO, help='Show certificate / user information')
    info_command.set_defaults(which=_COMMAND_INFO)
    info_command.add_argument(
        '-c',
        '--certificate',
        dest='cert_file_name',
        help='Certificate file to inspect.',
    )
    info_command.add_argument(
        '-s',
        '--sp',
        dest='user_type',
        action='store_const',
        const='sp',
        help='Show info of default Service Provider user certificate.',
    )
    info_command.add_argument(
        '-o',
        '--oem',
        dest='user_type',
        action='store_const',
        const='oem',
        help='Show info of default OEM user certificate.',
    )

    info_command.add_argument(
        '-a',
        '--admin',
        dest='user_type',
        action='store_const',
        const='admin',
        help='Show info of default ADMIN user certificate.',
    )

    client_cert_command = sub_parser.add_parser(
        _COMMAND_INSTALL_CLIENT_CERT,
        help='Install user certificate to browser store',
    )
    client_cert_command.set_defaults(which=_COMMAND_INSTALL_CLIENT_CERT)
    client_cert_command.add_argument(
        '-c',
        '--certificate',
        dest='cert_file_name',
        help='Certificate file to inspect.',
    )
    client_cert_command.add_argument(
        '-s',
        '--sp',
        dest='user_type',
        action='store_const',
        const='sp',
        help='Show info of default Service Provider user certificate.',
    )
    client_cert_command.add_argument(
        '-o',
        '--oem',
        dest='user_type',
        action='store_const',
        const='oem',
        help='Show info of default OEM user certificate.',
    )

    client_cert_command.add_argument(
        '-a',
        '--admin',
        dest='user_type',
        action='store_const',
        const='admin',
        help='Show info of default ADMIN user certificate.',
    )

    pem_command = sub_parser.add_parser(
        _COMMAND_TO_PEM,
        help='Convert pkcs12 container to PEM key and certificates chain.',
    )
    pem_command.set_defaults(which=_COMMAND_TO_PEM)
    pem_command.add_argument(
        '-c',
        '--certificate',
        dest='cert_file_name',
        required=True,
        help='path to pkcs12 file.',
    )
    pem_command.add_argument(
        '-o',
        '--output-dir',
        dest='output_dir',
        default=DEFAULT_CREDENTIALS_FOLDER,
        help='Output directory to save certificate.',
    )

    ca_command = sub_parser.add_parser(_COMMAND_INSTALL_ROOT_CA, help='Install Aos CA root Certificate.')
    ca_command.set_defaults(which=_COMMAND_INSTALL_ROOT_CA)

    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {version("aos-keys")}')
    return parser.parse_args()


def main():
    """Terminal main entry point."""
    args = _parse_args()

    try:
        if not hasattr(args, 'which'):
            sys.exit(0)
        elif args.which == _COMMAND_INSTALL_ROOT_CA:
            install_root_ca()
        elif args.which == _COMMAND_INFO:
            print_user_info(_args_to_cert_path(args))
        elif args.which == _COMMAND_INSTALL_CLIENT_CERT:
            install_user_certificate(_args_to_cert_path(args))
        elif args.which == _COMMAND_NEW_USER:
            if args.user_type:
                user_type = UserType.from_input(args.user_type)
            else:
                raise AosKeysError('Unknown user type', 'Set one of --sp, --oem or admin param')
            new_token_user(args.register_domain, args.output_dir, args.token, user_type, args.ecc)
        elif args.which == _COMMAND_TO_PEM:
            convert_pkcs12_file_to_pem(args.cert_file_name, args.output_dir)
    except AosKeysError as ake:
        ake.print_message()
        sys.exit(1)
    except Exception as sce:
        console.print('Process failed with error: ')
        console.print(sce)
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
