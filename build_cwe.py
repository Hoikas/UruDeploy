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

import os.path
import shutil
import subprocess

from builder import BuildProcess

class CWEBuilder(BuildProcess):
    def __init__(self, config):
        self.build_id = config.get("client", "build_id")
        self.build_dir = config.get("cwe", "build_dir")
        self.internal_client = config.getboolean("cwe", "build_internal")
        self.external_client = config.getboolean("cwe", "build_external")
        self.staging_dir = config.get("client", "staging_dir")

    def run(self):
        # Unfortunately, this needs to be serialized...
        if self.internal_client:
            print("---INTERNAL CLIENT---")
            self._build_client(isExternal=False)
            print("---------------------")
        if self.external_client:
            print("---EXTERNAL CLIENT---")
            self._build_client(isExternal=True)
            print("---------------------")

    def _build_client(self, isExternal):
        # CMake options...
        cmake = "cmake \"{}\" -DPLASMA_BUILD_LAUNCHER=ON -DPLASMA_BUILD_TOOLS=ON -DPRODUCT_BUILD_ID={}".format(self.build_dir, self.build_id)
        if isExternal:
            cmake = "{} -DPLASMA_EXTERNAL_RELEASE".format(cmake)
        subprocess.call(cmake, shell=True)

        # Okay, donedone that. Now, we must run MSBuild
        sln = os.path.join(self.build_dir, "Plasma.sln")
        msbuild = "MSBuild.exe /maxcpucount /nologo /property:Configuration=RelWithDebInfo /target:Rebuild \"{}\"".format(sln)
        subprocess.call(msbuild, shell=True)

        # Build folder renaming, cause we don't want our PDBs to be blown away
        bin = os.path.join(self.build_dir, "bin")
        suffix = "_external" if isExternal else "_internal"
        suffix = "{}{}".format(suffix, self.build_id)
        src = os.path.join(bin, "RelWithDebInfo")
        dest = os.path.join(bin, "RelWithDebInfo_{}".format(suffix))

        if os.path.exists(dest):
            shutil.rmtree(dest, True)
        shutil.move(src, dest)
