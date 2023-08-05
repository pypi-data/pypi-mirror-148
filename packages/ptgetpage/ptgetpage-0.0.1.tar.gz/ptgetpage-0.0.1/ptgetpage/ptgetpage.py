#!/usr/bin/python3
"""
    ptgetpage

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
import sys

import ptlibs.ptjsonlib as ptjsonlib
import ptlibs.ptmisclib as ptmisclib

import requests

class ptgetpage:
    def __init__(self, args):
        self.use_json = args.json
        self.ptjsonlib = ptjsonlib.ptjsonlib(self.use_json)
        self.json_no = self.ptjsonlib.add_json(SCRIPTNAME)
        self.headers = ptmisclib.get_request_headers(args)
        self.proxies = {"http": args.proxy, "https": args.proxy}
        self.redirects = args.redirects

        self.url = args.url
        self.ptjsonlib.add_data(self.json_no, {"url": self.url})

    def run(self):
        r = self.get_page()
        if r and not self.use_json:
            self.print_page(r)
        self.ptjsonlib.set_status(self.json_no, "ok")
        ptmisclib.ptprint_(ptmisclib.out_if(self.ptjsonlib.get_all_json(), condition=self.use_json))

    def get_page(self):
        try:
            data = {"status_code": "null", "page_content": "null", "page_headers": []}
            r = requests.get(self.url, allow_redirects=self.redirects, headers=self.headers, proxies=self.proxies, verify=False)
            if "text/html" in r.headers["content-type"]:
                for header, value in r.headers.items():
                    data["page_headers"].append({"header": header, "value": value})
                r.encoding = r.apparent_encoding
                if "charset=windows-1250" in r.text:
                    r.encoding = "windows-1250"
                data.update({"status_code": r.status_code, "encoding": r.encoding, "page_content": r.text})
                self.ptjsonlib.add_data(self.json_no, data)
                return r
            else:
                ptmisclib.end_error("Page not supported", self.json_no, self.ptjsonlib, self.use_json)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
            ptmisclib.end_error("Invalid scheme", self.json_no, self.ptjsonlib, self.use_json)
        except Exception as e:
            ptmisclib.end_error(f"Server not reachable - {e}", self.json_no, self.ptjsonlib, self.use_json)


    def print_page(self, response):
        ptmisclib.ptprint_(ptmisclib.out_ifnot(f"{'='*64}\n{' '*28}{ptmisclib.get_colored_text('HEADERS', 'TITLE')}\n{'='*64}", "", self.use_json))
        for header, value in response.headers.items():
            ptmisclib.ptprint_(ptmisclib.out_ifnot(f"{header}: {value}", "", self.use_json))
        ptmisclib.ptprint_(ptmisclib.out_ifnot(f"\n{'='*64}\n{' '*28}{ptmisclib.get_colored_text('CONTENT', 'TITLE')}\n{'='*64}", "", self.use_json))
        ptmisclib.ptprint_(ptmisclib.out_ifnot(response.text, "", self.use_json), end="")


def get_help():
    return [
        {"description": ["Script retrieves page content & headers"]},
        {"usage": ["ptgetpage <options>"]},
        {"usage_example": [
            "ptgetpage -u https://www.example.com/"
        ]},
        {"options": [
            ["-u",  "--url",                    "<url>",            "Connect to URL"],
            ["-p",  "--proxy",                  "<proxy>",          "Set proxy (e.g. http://127.0.0.1:8080)"],
            ["-r",  "--redirects",              "",                 "Allow redirects (default False)"],
            ["-c",  "--cookie",                 "<cookie>",         "Set cookie"],
            ["-ua",  "--user-agent",            "<user-agent>",     "Set user agent"],
            ["-H",  "--headers",                "<header:value>",   "Set custom headers"],
            ["-j",  "--json",                   "",                 "Enable JSON output"],
            ["-v",  "--version",                "",                 "Show script version and exit"],
            ["-h",  "--help",                   "",                 "Show this help message and exit"]
        ]
        }]


def parse_args():
    parser = argparse.ArgumentParser(description="ptgetpage")
    parser.add_argument("-u", "--url", type=str, help="URL to test", required=True)
    parser.add_argument("-r", "--redirects", action="store_true")
    parser.add_argument("-p", "--proxy", type=str)
    parser.add_argument("-c", "--cookie", type=str)
    parser.add_argument("-H", "--headers", type=str, nargs="+")
    parser.add_argument("-ua", "--user-agent", type=str, default="Penterep Tools")
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
    SCRIPTNAME = "ptgetpage"
    requests.packages.urllib3.disable_warnings()
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    args = parse_args()
    script = ptgetpage(args)
    script.run()


if __name__ == "__main__":
    main()
