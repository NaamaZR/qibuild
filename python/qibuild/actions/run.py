## Copyright (c) 2012-2015 Aldebaran Robotics. All rights reserved.
## Use of this source code is governed by a BSD-style license that can be
## found in the COPYING file.

""" Run a package found with qibuild find

"""

import sys

from qisys import ui
import qibuild.find
import qibuild.parsers
import qisys.parsers
import qisys.command
import qibuild.run

def configure_parser(parser):
    """Configure parser for this action"""
    qibuild.parsers.cmake_build_parser(parser)
    parser.add_argument("binary")
    parser.add_argument("bin_args", metavar="-- Binary arguments", nargs="*",
                        help="Binary arguments -- to escape the leading '-'")

def do(args):
    """Main entry point """
    build_worktree = qibuild.parsers.get_build_worktree(args)
    env = build_worktree.get_env()
    retcode = qibuild.run.run(build_worktree.build_projects, args.binary, args.bin_args,
                              env=env)
    if retcode < 0:
        ui.error("Process crashed: (%s)" % qisys.command.str_from_signal(-retcode))
        sys.exit(1)
    sys.exit(retcode)
