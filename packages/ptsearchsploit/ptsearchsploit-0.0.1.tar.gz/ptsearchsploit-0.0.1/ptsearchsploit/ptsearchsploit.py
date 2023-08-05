#!/usr/bin/python3
"""
    Copyright (c) 2020 HACKER Consulting s.r.o.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__version__ = "0.0.1"

import argparse
import json
import subprocess
import sys

import ptlibs.ptmisclib as ptmisclib
import ptlibs.ptjsonlib as ptjsonlib


class ptsearchsploit:
    def __init__(self, args):
        self.SEARCHSPLOIT_LOCATION = "/usr/bin/searchsploit" if not args.path else args.path
        self.use_json = args.json
        self.ptjsonlib = ptjsonlib.ptjsonlib(self.use_json)
        self.json_no = self.ptjsonlib.add_json("ptsearchsploit")
        self.search_query = args.search

    def run(self):
        self.run_searchsploit()
        ptmisclib.ptprint_(ptmisclib.out_if(self.ptjsonlib.get_all_json(), "", self.use_json))

    def run_searchsploit(self):
        try:
            if self.use_json:
                process = subprocess.run([self.SEARCHSPLOIT_LOCATION, self.search_query, "--json"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=False)
                self.ptjsonlib.add_data(self.json_no, {"searchsploit": json.loads(process.stdout)})
            else:
                process = subprocess.run([self.SEARCHSPLOIT_LOCATION, self.search_query], shell=False)
            self.ptjsonlib.set_status(self.json_no, "ok")
        except IOError:
            ptmisclib.end_error(f"Searchsploit not found, expected location: ({ptmisclib.get_colored_text(self.SEARCHSPLOIT_LOCATION, 'INFO')})", self.json_no, self.ptjsonlib, self.use_json)
        except Exception as e:
            ptmisclib.end_error(f"{e}", self.json_no, self.ptjsonlib, self.use_json)


def get_help():
    return [
        {"description": ["ptsearchsploit - Searchsploit wrapper"]},
        {"usage": ["ptsearchsploit <options>"]},
        {"usage_example": [
            "ptsearchsploit -s 'Apache 2.14.18'",
            "ptsearchsploit -s wordpress"
        ]},
        {"options": [
            ["-s",  "--search",                 "<string>",         "String to search for"],
            ["-p",  "--path",                   "<path>",           "Set path to searchsploit (default: '/usr/bin/searchsploit')"],
            ["-j",  "--json",                   "",                 "Output in JSON format"],
            ["-v",  "--version",                "",                 "Show script version and exit"],
            ["-h",  "--help",                   "",                 "Show this help message and exit"]
        ]
        }]


def parse_args():
    parser = argparse.ArgumentParser(add_help=False, usage="ptsearchsploit <options>")
    parser.add_argument("-s", "--search", type=str, required="True")
    parser.add_argument("-p", "--path", type=str)
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("-v", "--version", action="version", version=f"{SCRIPTNAME} {__version__}")

    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        ptmisclib.help_print(get_help(), SCRIPTNAME, __version__)
        sys.exit(0)

    args = parser.parse_args()
    ptmisclib.print_banner(SCRIPTNAME, __version__, args.json)
    return args


def main():
    global SCRIPTNAME
    SCRIPTNAME = "ptsearchsploit"
    args = parse_args()
    script = ptsearchsploit(args)
    script.run()


if __name__ == "__main__":
    main()
