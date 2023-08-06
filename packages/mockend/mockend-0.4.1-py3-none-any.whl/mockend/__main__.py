import argparse
import json
from . import app, config

parser = argparse.ArgumentParser(prog='mockend', description='Mockend Service')
parser.add_argument('-c', '--config', metavar='', type=str, required=True, default='config.json', help='Path to the configuration file.')
parser.add_argument('-i', '--host', metavar='', type=str, required=False, default='localhost', help='Host address')
parser.add_argument('-p', '--port', metavar='', type=int, required=False, default=5555, help='Port number')
parser.add_argument('-d', '--debug', metavar='', type=bool, required=False, default=True, help='Debug mode')
parser.add_argument('-e', '--certificate', metavar='', type=str, required=False, default=None, help='Certificate file')
parser.add_argument('-k', '--key', metavar='', type=str, required=False, default=None, help='Key file')
args = parser.parse_args()

config.update(json.load(open(args.config)))
ssl_context = (args.certificate, args.key) if args.certificate and args.key else None
app.run(host=args.host, port=args.port, debug=args.debug, ssl_context=ssl_context)
