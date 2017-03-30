#!/usr/bin/python
#
# Antti Pettinen
# Copyright 2017 Tampere University of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for MSTeamsURLProvider class"""
#import re
import urllib2

from autopkglib import Processor, ProcessorError

__all__ = ["MSTeamsURLProvider"]

BASE_URL = "https://teams.microsoft.com/downloads/DesktopURL?env=production&plat=osx"

class MSTeamsURLProvider(Processor):
    """Provides a download URL for the latest MS Teams release"""
    description = __doc__
    input_variables = {
        "base_url": {
            "required": False,
            "description": ("Default is %s" % BASE_URL),
        },
    }
    output_variables = {
        "url": {
            "description": "URL to the latest MSTeams release.",
        },
    }

    def get_msteams_pkg_url(self, base_url):
        """Finds a download URL for latest MSTeams release"""
        try:
            fref = urllib2.urlopen(base_url)
            dl_url = fref.read()
            fref.close()
        except BaseException as err:
            raise ProcessorError("Could not retrieve %s: %s" %(base_url, err))
        # if the URL is empty, raise error
        if not dl_url:
            raise ProcessorError(
                "Could not find MSTeams download URL in %s" %base_url)
        return dl_url

    def main(self):
        """Find and return download URL for MSTeams"""
        base_url = self.env.get("base_url", BASE_URL)
        self.env["url"] = self.get_msteams_pkg_url(base_url)
        self.output("MSTeams URL found: %s" % self.env["url"])

if __name__ == "__main__":
    PROCESSOR = MSTeamsURLProvider()
    PROCESSOR.execute_shell()
