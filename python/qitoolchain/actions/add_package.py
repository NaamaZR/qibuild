## Copyright (c) 2012-2016 Aldebaran Robotics. All rights reserved.
## Use of this source code is governed by a BSD-style license that can be
## found in the COPYING file.

"""Add a new package to a toolchain

"""

import argparse
import os
import zipfile

from qisys import ui
import qisys.archive
import qisys.worktree
import qitoolchain.parsers

def configure_parser(parser):
    """Configure parser for this action """
    qisys.parsers.worktree_parser(parser)
    qitoolchain.parsers.toolchain_parser(parser)
    parser.add_argument("package_path", metavar='PATH',
                        help="The path to the package")
    parser.add_argument("--name", help="DEPRECATED. Name of the package. "
                                       "Used for legacy format. "
                                       "You should create a package.xml and "
                                       "use `qitoolchain make-package` instead")

def do(args):
    """ Add a package to a toolchain

    - Check that there is a current toolchain
    - Add the package to the cache
    - Add the package from cache to toolchain

    """
    toolchain = qitoolchain.parsers.get_toolchain(args)
    name = args.name
    package_path = args.package_path
    legacy = False
    try:
        archive = zipfile.ZipFile(package_path)
        archive.read("package.xml")
    except KeyError:
        legacy = True
    if legacy and not args.name:
        ui.fatal("Must specify --name when using legacy format")
    if args.name and not legacy:
        ui.warning("--name ignored when using modern format")

    package = None
    if legacy:
        package = qitoolchain.qipackage.QiPackage(args.name)
    else:
        package = qitoolchain.qipackage.from_archive(package_path)

    # extract it to the default packages path of the toolchain
    tc_name = toolchain.name
    tc_packages_path = qitoolchain.toolchain.get_default_packages_path(tc_name)
    dest = os.path.join(tc_packages_path, package.name)
    qisys.sh.rm(dest)
    qitoolchain.qipackage.extract(package_path, dest)
    package.path = dest

    # add the package to the toolchain
    toolchain.add_package(package)
