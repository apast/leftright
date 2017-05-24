def run():
    import logging
    import sys
    from leftright.cli import DiffCLI

    logging.basicConfig(level=logging.INFO)
    DiffCLI().run(sys.argv[1:])


if __name__ == '__main__': run()
