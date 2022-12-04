# cli.py
"""This module provided the cli interface for the tool"""

import argparse
import sys

from . import __version__
import urllib.parse
from .singleshoot import Gun


def main():
    args = parse_cmd_line_arguments()

    if args.mode and args.mode != "canary":
        if not args.command:
            print('the argument -c/--command is required to generate RCE payloads')
            exit()
        else:
            if int(args.encode) > -1:
                _command = urllib.parse.quote(args.command)
            else:
                _command = args.command
    
    if args.mode and args.mode == "canary":
        if not args.canary:
            print('the argument -cn/--canary is required to generate canary payloads')
            exit()
    
    gun = Gun(args.target, args.target_list, _command,
    args.encode, args.protocol, args.canary, args.mode, args.verbose, args.filter)

    gun.reload()


def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
        prog="single-shot",
        description="Generate possible RCE payloads to use in with blind SSRF scenarios",
        epilog="After all, we are all alike"
    )

    parser.version = f"single-shot v{__version__}"
    parser.add_argument("-v", "--version", action="version")

    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument("-t", "--target", 
        metavar="TARGET", nargs="?", help="Set the target internal domain name or IP address")
    
    group1.add_argument("-l", "--target-list", 
        metavar="TARGET_FILE", nargs="?", help="Set the target list containing internal domain names or IP addresses")

    parser.add_argument("-c", "--command", 
        metavar="COMMAND", nargs="?", default="", help="Set the command to be executed")

    parser.add_argument("-e", "--encode", 
        metavar="ENCODE_LEVEL", nargs="?", default="1", help="Set the payload's URLencode level,ex:\n-e 0 will not encode the payload\n-e 2 will double URLencode the output")
    
    parser.add_argument("-p", "--protocol", 
        metavar="PROTOCOL", nargs="?", default="http://", help="Set the internal address protocol.\ndefault is http://")

    parser.add_argument("-cn", "--canary", 
        metavar="CANARY_ADDRESS", nargs="?", help="Set canary address to confirm internal services")
    
    parser.add_argument("-m", "--mode", 
        metavar="MODE", nargs="?", default="canary", help="There are currently three supported modes:\ncanary (deafult mode: generate canary payloads)\nrce (generate payloads that can lead to RCE)\nall (generates RCE and Canary payloads)")

    parser.add_argument("-f", "--filter", 
        metavar="FILTER", nargs="*", default=["shellshock"], help="Filter category, framework or a specific payload from the results\ndefault: exclude Shellshock payloads")

    parser.add_argument("-V", "--verbose", 
        default=False, help="Show name of the exploited service and vulnerability for each payload", action="store_true")

        
    return parser.parse_args()

class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)