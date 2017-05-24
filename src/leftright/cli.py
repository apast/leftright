import logging
from tornado.ioloop import IOLoop

from leftright.api import DiffApplication


LOG = logging.getLogger(__name__)


class DiffApplicationRunner():

    def prepare(self, port=8080, debug=False):
        app =  DiffApplication().build(debug=debug)
        LOG.info("Debug mode is %s", "enabled" if debug else "disabled")
        LOG.info("Setting server listen port to %s", port)
        app.listen(port)
        return app

    def start_loop(self):
        LOG.info("Starting server loop. Press Ctrl+C to quit")
        IOLoop.current().start()
        LOG.info("Server was stopped. Bye")


class DiffCLI():

    def run(self, input_args):
        args = self.fetch(input_args)
        runner = DiffApplicationRunner()
        app = runner.prepare(port=args.port, debug=args.debug)
        runner.start_loop()

    def fetch(self, input_args):
        import argparse

        parser = argparse.ArgumentParser()
        parser.description = "diff REST API server"

        parser.add_argument("-p", "--port", help="server port", default=8080,
                            type=int)

        parser.add_argument("-D", "--debug", help="start server under debug mode. Code changes will be deployed and reloaded in runtime",
                            default=False,
                            action="store_true")

        return parser.parse_args(input_args)


