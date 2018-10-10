#!/usr/bin/env python

#import dep_check
#dep_check.check_dependency()

import re
import sys
import shutil
import os
import textwrap
import argparse
import emailOsint
import domainOsint
import ipOsint
import usernameOsint
from tld import get_tld
from netaddr import IPAddress,AddrFormatError

desc = """
____/ /____ _ / /_ ____ _ _____ ____   / /____   (_)/ /_
/ __  // __ `// __// __ `// ___// __ \ / // __ \ / // __/
/ /_/ // /_/ // /_ / /_/ /(__  )/ /_/ // // /_/ // // /_
\__,_/ \__,_/ \__/ \__,_//____// .___//_/ \____//_/ \__/
                            /_/

        Open Source Assistant for #OSINT
            www.datasploit.info

"""
epilog = """              Connect at Social Media: @datasploit
            """

def run(config_file_path, single_input, file_input, output, active, quiet, parser):
    global desc
    
    # check and ensure the config file is present otherwise create one. required for all further operations
    ds_dir=os.path.dirname(os.path.realpath(__file__))
    config_sample_path= os.path.join(ds_dir,"config_sample.py")
    print os.path.exists(config_file_path)
    if not os.path.exists(config_file_path):
        print "[+] Looks like a new setup, setting up the config file."
        shutil.copyfile(config_sample_path,config_file_path)
        print "[+] A config file is added please follow guide at https://datasploit.github.io/datasploit/apiGeneration/ to fill API Keys for better results"
        # We can think about quiting at this point.
    # parse arguments in case they are provided.
    
    # if no target is provided print help and quit.
    if not (single_input or file_input):
        print "\nSingle target or file input required to run\n"
        parser.print_help()
        sys.exit()
    # Banner print
    print textwrap.dedent(desc)

    if single_input:
        try:
            auto_select_target(single_input, output)
        except KeyboardInterrupt:
            print "\nCtrl+C called Quiting"
    if file_input:
        try:
            if os.path.isfile(file_input):
                print "File Input: %s" % file_input
                with open(file_input, 'r') as f:
                    for target in f:
                        auto_select_target(target.rstrip(), output)
                print "\nDone processing %s" % file_input
            else:
                print "%s is not a readable file" % file_input
                print "Exiting..."
        except KeyboardInterrupt:
            print "\nCtrl+C called Quiting"


def auto_select_target(target, output=None):
    """Auto selection logic"""
    print "Target: %s" % target
    try:
        inp=IPAddress(target)
        if inp.is_private() or inp.is_loopback():
            print "Internal IP Detected : Skipping"
            sys.exit()
        else:
            print "Looks like an IP, running ipOsint...\n"
            ipOsint.run(target, output)
    except SystemExit:
        print "exiting"
    except AddrFormatError:
        if re.match('[^@]+@[^@]+\.[^@]+', target):
            print "Looks like an EMAIL, running emailOsint...\n"
            emailOsint.run(target, output)
        elif get_tld(target, fix_protocol=True,fail_silently=True) is not None:
            print "Looks like a DOMAIN, running domainOsint...\n"
            domainOsint.run(target, output)
        else:
            print "Nothing Matched assuming username, running usernameOsint...\n"
            usernameOsint.run(target, output)
    except:
        print "Unknown Error Occured"

def main():
    global desc, epilog

    # Set all parser arguments here.
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(desc),
        epilog=epilog)

    parser.add_argument(
        "-i", "--input", help="Provide Input", dest='single_target')
    parser.add_argument(
        "-f", "--file", help="Provide Input", dest='file_target')
    parser.add_argument("-a", "--active", help="Run Active Scan attacks",
                        dest='active', action="store_false")
    parser.add_argument("-q", "--quiet", help="Run scans in automated manner accepting default answers",
                        dest='quiet', action="store_false")
    parser.add_argument(
        "-o", "--output", help="Provide Destination Directory", dest='output', default=None)
    parser.add_argument("-c", "--config_file", help="Provide configuration file",
                        dest='config_file_path', default="config.py")
    args = parser.parse_args()

    config_file_path = args.config_file_path
    active = args.active
    quiet = args.quiet
    single_input = args.single_target
    file_input = args.file_target
    output = args.output

    run(config_file_path, single_input, file_input, output, active, quiet, parser)


if __name__ == "__main__":
    main()
