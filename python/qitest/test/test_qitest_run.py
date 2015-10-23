## Copyright (c) 2012-2015 Aldebaran Robotics. All rights reserved.
## Use of this source code is governed by a BSD-style license that can be
## found in the COPYING file.

import sys
import json

import qisys.command
import qibuild.find

def test_simple_run(tmpdir, qitest_action):
    ls = qisys.command.find_program("ls")
    tests = [
            { "name": "ls", "cmd" : [ls], "timeout" : 1 }
    ]
    qitest_json = tmpdir.join("qitest.json")
    qitest_json.write(json.dumps(tests))
    qitest_action("run", cwd=tmpdir.strpath)

def test_repeat_until_fail(tmpdir, qitest_action):
    ls = qisys.command.find_program("ls")
    rm = qisys.command.find_program("rm")
    foo = tmpdir.join("foo")
    foo.write("this is foo\n")
    tests = [
            {"name" : "ls", "cmd" : [ls, foo.strpath], "timeout" : 1 },
            {"name" : "rm", "cmd" : [rm, foo.strpath], "timeout" : 1 },
    ]
    qitest_json = tmpdir.join("qitest.json")
    qitest_json.write(json.dumps(tests))
    rc = qitest_action("run", "--repeat-until-fail", "2",
                       cwd=tmpdir.strpath, retcode=True)
    assert rc != 0

def test_no_capture(tmpdir, qitest_action):
    if not sys.stdout.isatty():
        # The test will fail anyway
        return

    test_tty = tmpdir.join("test_tty.py")
    test_tty.write("""
import sys
if not sys.stdout.isatty():
    sys.exit("sys.stdout is not a tty")
""")

    tests = [
            { "name": "test_tty", "cmd" : [sys.executable, test_tty.strpath], "timeout" : 1 }
    ]
    qitest_json = tmpdir.join("qitest.json")
    qitest_json.write(json.dumps(tests))
    rc = qitest_action("run", "--no-capture",
                       cwd=tmpdir.strpath, retcode=True)
    assert rc == 0

def test_run_last_failed(tmpdir, qitest_action, record_messages):
    test_one = tmpdir.join("test_one.py")
    test_one.write("import sys; sys.exit(1)")
    test_two = tmpdir.join("test_two.py")
    test_two.write("")
    qitest_json = tmpdir.join("qitest.json")
    tests = [
              { "name": "test_one", "cmd" : [sys.executable, test_one.strpath], "timeout" : 1},
              { "name": "test_two", "cmd" : [sys.executable, test_two.strpath], "timeout" : 1},
           ]
    qitest_json.write(json.dumps(tests))
    qitest_action.chdir(tmpdir)
    qitest_action("run", retcode=True)
    record_messages.reset()
    qitest_action("run", "--last-failed", retcode=True)
    assert not record_messages.find("\(2/2\) test_two")
    assert record_messages.find("\(1/1\) test_one")
    test_one.write("")
    record_messages.reset()
    qitest_action("run", "--last-failed", retcode=True)
    qitest_action("run", "--last-failed", retcode=True)
    assert record_messages.find("No failing tests found")
