#! /usr/bin/python
#
#
# Copyright 2014 Abid Hasan Mujtaba
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Author: Abid H. Mujtaba
# Date: 2014-04-04
#
# Collection of functions which are common to a number of utilities.


import os


def add_parent_to_path():
    """
    Method for adding the grand-parent folder to the PYTHON PATH which allows us to import from the package defined by the parent folder.
    """

    parentdir = os.path.dirname( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )

    os.sys.path.insert(0, parentdir)
