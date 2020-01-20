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

from __future__ import absolute_import

import re

from autopkglib import Processor, ProcessorError, URLGetter

__all__ = ["MSTeamsURLProvider"]

BASE_URL = "https://teams.microsoft.com/downloads/DesktopURL?"
TEAMS_ENVIRONMENT = "production"
TEAMS_PLATFORM = "osx"
TEAMS_ARCH = ""


class MSTeamsURLProvider(URLGetter):
    """Provides a download URL for the latest MS Teams release. Supports both macOS and Windows clients, with the latter requiring the architecture to be defined"""

    description = __doc__
    input_variables = {
        "base_url": {"required": False, "description": ("Default is %s" % BASE_URL),},
        "environment": {
            "required": False,
            "description": ("Default is %s" % TEAMS_ENVIRONMENT),
        },
        "platform": {
            "required": False,
            "description": ("Default is %s" % TEAMS_PLATFORM),
        },
        "architecture": {
            "required": False,
            "description": (
                "Default is empty string, as MS Teams for macOS does not provide different architectures."
            ),
        },
    }
    output_variables = {
        "url": {"description": "URL to the MSTeams release.",},
        "version": {"description": "The version of the MSTeams release.",},
    }

    def main(self):
        """Find and return download URL for MSTeams"""
        base_url = self.env.get("base_url", BASE_URL)
        teams_env = self.env.get("environment", TEAMS_ENVIRONMENT)
        teams_plat = self.env.get("platform", TEAMS_PLATFORM)
        teams_arch = self.env.get("architecture", TEAMS_ARCH)

        fetch_url = "".join([base_url, "env=", teams_env, "&plat=", teams_plat])
        # Windows only:
        if teams_arch and teams_plat == "windows":
            fetch_url = "".join([fetch_url, "&arch=", teams_arch])

        self.env["url"] = self.download(fetch_url, text=True)
        self.output("MSTeams URL found: %s" % self.env["url"])

        m = re.search(
            r"{0}-{1}/([\d\.]+)/Teams_{1}\.(pkg|exe)".format(teams_env, teams_plat),
            self.env["url"],
        )
        if m:
            self.env["version"] = m.group(1)
            self.output("MSTeams version found: %s" % self.env["version"])


if __name__ == "__main__":
    PROCESSOR = MSTeamsURLProvider()
    PROCESSOR.execute_shell()
