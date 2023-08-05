#!/usr/bin/python3
"""
    Cookie Analyser

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
import re
import sys

import cloudscraper

import ptlibs.ptjsonlib as ptjsonlib
import ptlibs.ptmisclib as ptmisclib


class ptcookie:
    def __init__(self, args):
        self.use_json = args.json
        self.ptjsonlib = ptjsonlib.ptjsonlib(self.use_json)
        self.use_json_no = self.ptjsonlib.add_json("ptcookie")
        self.proxy = {"https": args.proxy, "http": args.proxy}
        args.cookie = None
        self.headers = ptmisclib.get_request_headers(args)
        self.search_query = args.search_for

    def run(self):
        response = self.get_response()
        self.process_response(response)
        ptmisclib.ptprint_(ptmisclib.out_if(self.ptjsonlib.get_all_json(), "", self.use_json))

    def get_response(self):
        try:
            scraper = cloudscraper.create_scraper(delay=10)
            response = scraper.get(f"https://cookiepedia.co.uk/cookies/{self.search_query}", proxies=self.proxy, headers=self.headers)
            return response
        except Exception as e:
            ptmisclib.end_error("Cannot connect to cookiepedia", self.use_json_no, self.ptjsonlib, self.use_json)

    def process_response(self, response):
        try:
            ptmisclib.ptprint_(ptmisclib.out_ifnot(f"Cookie info ({self.search_query}):", "INFO", self.use_json))
            cookie_info = re.search(r"(<h2>About this cookie:<\/h2>)[\s]*(<p>[\S\s]+\<\/p>)[\s]*(<p>[\S\s]+<\/strong><\/p>)", response.text)
            cookie_info = [cookie_info[2]] + [cookie_info[3]] # Select only relevant information
            parsed_info = [(re.sub(r"(<\s*[\w\/]+\s*([\w=\"\'\/\\:\s;-]*)*\s*>)|(\n)", "", i)) for i in cookie_info]
            ptmisclib.ptprint_(ptmisclib.out_ifnot(ptmisclib.get_colored_text('\n'.join(parsed_info), "TEXT"), "", self.use_json))
            self.ptjsonlib.set_status(self.use_json_no, "ok")
            self.ptjsonlib.add_data(self.use_json_no, {"cookie": self.search_query, "cookie_info": ' '.join(parsed_info)})
        except Exception as e:
            ptmisclib.end_error(f"Search returned no matches - {e}", self.use_json_no, self.ptjsonlib, self.use_json)


def get_help():
    return [
        {"description": ["Cookie Analyser"]},
        {"usage": ["ptcookie <options>"]},
        {"usage_example": [
            "ptcookie -s ASP.NET_SessionId",
            "ptcookie -s PHPSESSID"
        ]},
        {"options": [
            ["-s",  "--search-for",             "<cookie>",         "Search for cookie"],
            ["-p",  "--proxy",                  "<proxy>",          "Set proxy (e.g. http://127.0.0.1:8080)"],
            ["-ua", "--user-agent",             "<ua>",             "Set User-Agent header"],
            ["-H",  "--headers",                "<header:value>",   "Set custom header(s)"],
            ["-j",  "--json",                   "",                 "Output in JSON format"],
            ["-v",  "--version",                "",                 "Show script version and exit"],
            ["-h",  "--help",                   "",                 "Show this help message and exit"]
        ]
        }]


def parse_args():
    parser = argparse.ArgumentParser(add_help=False, usage="ptcookie <options>")
    parser.add_argument("-s", "--search-for", type=str, required="True")
    parser.add_argument("-p", "--proxy", type=str)
    parser.add_argument("-ua", "--user-agent", type=str, default="Penterep Tools")
    parser.add_argument("-H", "--headers", type=ptmisclib.pairs)
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
    SCRIPTNAME = "ptcookie"
    args = parse_args()
    script = ptcookie(args)
    script.run()


if __name__ == "__main__":
    main()
