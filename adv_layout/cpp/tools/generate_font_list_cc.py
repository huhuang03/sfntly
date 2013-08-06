#!/usr/bin/env python
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limit

"""Script to generate a C++ list of font paths to be used as test data."""

import os
from string import Template
import xml.dom.minidom as minidom
import argparse
from argparse import ArgumentParser
from utils import FixPath
from utils import GetFontList

cc_license = """/*
 * Copyright 2011 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

"""
do_not_edit = """/*
 * !!! DO NOT EDIT !!!
 * THIS FILE IS GENERATED BY A SCRIPT.
 * FOR MORE DETAILS SEE 'tools/README-test_data.txt'.
 */

"""


def GetFontPath(xml_path):
  """Gets the path attribute from an XML font description."""
  doc = minidom.parseString(open(xml_path, 'r').read())
  font_elements = doc.getElementsByTagName('font_test_data')
  if (not font_elements) or (len(font_elements) > 1):
    return ''
  return '  "' + str(font_elements[0].getAttribute('path')) + '"'


def main():
  parser = ArgumentParser(description="""Generates CMap table test data
from XML description files.""",
                          formatter_class=
                          argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--destination',
                      default='../src/test/autogenerated',
                      help='ouput folder for the generated files')
  parser.add_argument('--source',
                      default='../data/fonts',
                      help='input folder for the XML files')
  parser.add_argument('--name',
                      default='cmap_test_data',
                      help='base name of the generated test files')
  parser.add_argument('--fonts',
                      default='',
                      help="""space separated list of XML files to use as
source data""")
  parser.add_argument('--font_dir',
                      default='.',
                      help="""base directory of the fonts in the generated
source""")
  args = parser.parse_args()

  try:
    os.stat(args.destination)
  except OSError:
    os.mkdir(args.destination)

  args.destination = FixPath(args.destination)
  args.source = FixPath(args.source)
  args.font_dir = FixPath(args.font_dir)
  if args.font_dir == '.':
    args.font_dir = ''

  if not args.fonts:
    args.fonts = [path for path in
                  GetFontList(args.source, ['.ttf.xml', '.ttc.xml', '.otf.xml'])
                  if path.find('src') == -1 and path.find('archive') == -1]

  elif type(args.fonts) != 'list':
    args.fonts = [args.fonts]

  header_guard = ('TYPOGRAPHY_FONT_SFNTLY_SRC_TEST_AUTOGENERATED_'
                  + args.name.upper() + '_H_')

  h_file_name = args.destination + args.name + '.h'
  h_file = open(h_file_name, 'w')
  h_file.write(do_not_edit)
  h_file.write(cc_license)
  h_file.write('#ifndef ' + header_guard + '\n')
  h_file.write('#define ' + header_guard + '\n\n')
  h_file.write('#include "sfntly/port/type.h"\n\n')
  h_file.write('namespace sfntly {\n')
  h_file.write(Template('namespace $name {\n').substitute(name=args.name))
  # Writing the list of paths to the test array
  h_file.write(
      Template("""const char* kAllTests[] = {
$tests
};""").substitute(tests=',\n'.join(map(GetFontPath, args.fonts))))
  h_file.write(Template('\n}  // namespace $name\n').substitute(name=args.name))
  h_file.write('}  // namespace sfntly\n')
  h_file.write('\n#endif  // ' + header_guard + '\n')
  h_file.close()

if __name__ == '__main__':
  main()