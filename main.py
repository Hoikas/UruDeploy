#    This file is part of UruDeploy.
#
#    UruDeploy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    UruDeploy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with UruDeploy.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import configparser

from build_cwe import CWEBuilder, PackPythonBuilder

parser = argparse.ArgumentParser(prog="Uru Deploy", description="")
parser.add_argument("configfile", metavar="INI")
parser.add_argument("--no-build-cwe", default=False, action="store_true")
parser.add_argument("--no-pack-python", default=False, action="store_true")
parser.add_argument("--no-build-server", default=False, action="store_true")
parser.add_argument("--no-synch-data", default=False, action="store_true")
parser.add_argument("--no-generate-manifests", default=False, action="store_true")

if __name__ == "__main__":
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.configfile)

    if not args.no_build_cwe:
        print("Building CyanWorlds.com Engine...")
        print()
        cwe = CWEBuilder(config)
        cwe.start_async()

    # Before we pack the python, CWE must be done...
    if not args.no_pack_python:
        cwe.join()
        print("Packing Python...")
        print()
        pypack = PackPythonBuilder(config)
        pypack.start_async()

    # TODO: someday we will build datafiles, manifest, etc
