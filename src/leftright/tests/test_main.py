import unittest
from unittest.mock import patch

from leftright.cli import DiffCLI, DiffApplicationRunner

from tornado.ioloop import IOLoop


class TestRun(unittest.TestCase):

    @patch("logging.basicConfig")
    @patch("leftright.cli.DiffCLI.run")
    def test_main_run(self, cli_run, log_config):
        from leftright.__main__ import run
        run()
        log_config.assert_called_once()
        cli_run.assert_called_once()


class TestDiffApplicationRunner(unittest.TestCase):

    @patch("tornado.web.Application.listen")
    @patch("leftright.api.DiffApplication.build")
    def test_prepare(self, build, listen):
        DiffApplicationRunner().prepare(port=8080)
        build.assert_called_with(debug=False)

        DiffApplicationRunner().prepare(debug=True)
        build.assert_called_with(debug=True)

    @patch("tornado.ioloop.IOLoop.current")
    def test_ioloop(self, current):
        runner = DiffApplicationRunner()
        runner.prepare()
        runner.start_loop()
        current.assert_called()


class TestDiffCLI(unittest.TestCase):

    @patch("leftright.cli.DiffApplicationRunner.start_loop")
    @patch("leftright.cli.DiffApplicationRunner.prepare")
    def test_full_run(self, prepare, start_loop):
        DiffCLI().run([])
        prepare.assert_called()
        start_loop.assert_called()

    def test_cli_arguments(self):
        self.assertEqual(False, DiffCLI().fetch([]).debug,
                         "debug mode should be disabled by default")

        self.assertEqual(8080, DiffCLI().fetch([]).port,
                         "default port should be 8080")

        self.assertEqual(80, DiffCLI().fetch(["-p", "80"]).port,
                         "port setup should be flexible")

        self.assertEqual(True, DiffCLI().fetch(["--debug"]).debug,
                         "debug mode is a decision of user")
