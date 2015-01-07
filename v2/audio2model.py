import logging
import argparse
import os
import sys

from ui.app import ViewerApp


def setup_logging(args):
    working_path = os.path.join(os.path.expanduser('~'), '.peachyviewer')
    if not os.path.exists(working_path):
        os.makedirs(working_path)
    logfile = os.path.join(working_path, 'log.log')

    logging_format = '%(levelname)s: %(asctime)s %(module)s - %(message)s'
    logging_level = getattr(logging, args.loglevel.upper(), "WARNING")
    if not isinstance(logging_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel)
    if args.console:
        rootLogger = logging.getLogger()
        logFormatter = logging.Formatter(logging_format)
        fileHandler = logging.FileHandler(logfile)
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)
        rootLogger.setLevel(logging_level)
    else:
        logging.basicConfig(filename=logfile, format=logging_format, level=logging_level)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("View Gcode")
    parser.add_argument('-l', '--log',     dest='loglevel', action='store',      required=False, default="WARNING", help="Enter the loglevel [DEBUG|INFO|WARNING|ERROR] default: WARNING")
    parser.add_argument('-c', '--console', dest='console',  action='store_true', required=False, help="Logs to console not file")
    args, unknown = parser.parse_known_args()

    setup_logging(args)

    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    else:
        path = os.path.dirname(os.path.realpath(__file__))

    app = ViewerApp(path)
    app.MainLoop()
