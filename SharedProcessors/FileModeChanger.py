#!/usr/bin/python
#
# Antti Pettinen
# Copyright 2018 Antti Pettinen
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
"""See docstring for FileModeChanger class"""
#import re
import os

from autopkglib import Processor, ProcessorError

__all__ = ["FileModeChanger"]
DEFAULT_MODE = "0644"


class FileModeChanger(Processor):
    """
    Changes the mode, i.e. file system permissions for a given file, or
    alternatively, an array of files. Will use the same permission for each file
    in the array.
    """
    description = __doc__
    input_variables = {
        "filenames": {
            "required": True,
            "description": ("paths to the files"),
        },
        "mode": {
            "required": True,
            "description": ("Desired mode in octal representation. Default is
                            %s" %DEFAULT_MODE),
        }
    }
    
    def main(self):
        """Change the mode according to output"""
        filepaths = self.env.get("filenames")
        file_mode = self.env.get("mode", DEFAULT_MODE)

        for filename in filepaths:
            try:
                os.chmod(filename, file_mode)
            except BaseException as err:
                raise ProcessorError("Could not change mode for %s"
                                     %(filename))
