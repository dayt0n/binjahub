#!/usr/bin/env python3
"""Main code for the oracle API."""
import argparse
import getpass
import uvicorn
from dotenv import load_dotenv
from binjahub.auth import setup_ldap_auth


def parse_arguments() -> argparse.Namespace:
    """Parse arguments from cmdline to initialize
    optional settings such as host, port, debug mode, and autoreload.
    """
    load_dotenv()
    parser = argparse.ArgumentParser(description="Oracle API Configuration")
    parser.add_argument("-H", "--host", type=str, default="127.0.0.1", help="Host address")
    parser.add_argument("-p", "--port", type=int, default=5555, help="Port number")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-r", "--reload", action="store_true", help="Enable autoreload")
    parser.add_argument("-s", "--server", default=None, help="LDAP server URL")
    parser.add_argument("-b", "--base-dn", default=None, help="LDAP base DN to search for users")
    parser.add_argument("-u", "--bind-user", default=None, help="LDAP Bind username")
    parser.add_argument("-P", "--bind-password", default=None, help="LDAP Bind password")
    return parser.parse_args()


def main() -> int:
    """Main function to run the uvicorn web server and the API."""
    args = parse_arguments()
    password = args.bind_password
    if args.bind_user and not password:
        password = getpass.getpass(f"Enter password for {args.bind_user}: ")

    setup_ldap_auth(url=args.server, base=args.base_dn, user=args.bind_user, password=password)

    uvicorn.run(
        "binjahub.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        debug=args.debug,
    )

    return 0


if __name__ == "__main__":
    main()
