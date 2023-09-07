# Copyright 2023 Nito T.M.
# License https://www.apache.org/licenses/LICENSE-2.0 Apache-2.0
# Author Nito T.M. (https://github.com/nitotm)
# Package pypi.org/project/eld/

class SubsetResult:
    def __init__(self, success, languages=None, error=None, file=None):
        self.success = success
        self.languages = list(languages.values()) if languages else None
        self.error = error
        self.file = file
