from tornado.ioloop import IOLoop

from leftright.api import DiffApplication


class DiffApplicationRunner():
    def run(self, input_args):
        args = self.fetch(input_args)
        app = self.prepare(port=args.port, debug=args.debug)
        self.start_loop()

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

    def prepare(self, port=8080, debug=False):
        app =  DiffApplication().build(debug=debug)
        app.listen(port)
        return app

    def start_loop(self):
        IOLoop.current().start()


if __name__ == '__main__':
    import sys
    runner = DiffApplicationRunner()
    runner.run(sys.argv[1:])