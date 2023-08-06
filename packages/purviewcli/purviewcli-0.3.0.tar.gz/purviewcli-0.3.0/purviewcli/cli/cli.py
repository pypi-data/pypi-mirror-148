
"""
usage: pv [--version] [--help] <command> [<args>...]

options:
   -v, --version
   -h, --help
   

The most commonly used pv commands are:
   pv entity           [Atlas] Entities are a collection of attributes that model or represent an asset.
   pv glossary         [Atlas] Vocabularies for business users.
   pv lineage          [Atlas] Helps you understand the source and impact of data and changes to data over time.
   pv relationship     [Atlas] Relationships describe connections between two entities.
   pv types            [Atlas] A Type in Atlas is a definition of how a particular object type is stored and accessed.
   pv account          [Other] Azure Purview account data plane.
   pv insight          [Other] Azure Purview insights.
   pv management       [Other] Azure Purview control plane operations (Account, Private Endpoint, Private Link, etc).
   pv policystore      [Other] Azure Purview Metadata Policies.
   pv scan             [Other] Azure Purview scan.
   pv search           [Other] Azure Purview search.

See 'pv <command>' for more information on a specific command.

"""
import sys
import json
import importlib
from docopt import docopt
from purviewcli import __version__
from purviewcli.client import settings

def main():
    # Append help flag if input is pv only
    if len(sys.argv) == 1:
        sys.argv.append('-h')
        sys.exit(main())

    # Dictionary return value from docopt with Options (e.g. --help), Arguments (<args>), and Commands (<command>)
    args = docopt(__doc__, version=__version__, options_first=True)

    # List of command line arguments passed to purviewcli (e.g. ['glossary', 'putTerm', '--termGuid', '12345')
    argv = [args['<command>']] + args['<args>']
    
    # Remove purviewName from argument list (if exists)
    if '--purviewName' in argv:
            pos = argv.index('--purviewName')
            del argv[pos]
            settings.PURVIEW_NAME = argv[pos]
            del argv[pos]

    # Command
    command = args['<command>']

    # Init sub-docopt
    if command in ['entity', 'relationship', 'lineage', 'glossary', 'types', 'scan', 'insight', 'search', 'management', 'policystore', 'account']:
        globals()[command] = importlib.import_module('purviewcli.cli.' + command)
        command_args = docopt(eval(command).__doc__, argv=argv)
    else:
        exit("%r is not a purviewcli command." % args['<command>'])

    # Action
    action = None
    for item in command_args:
        if item[0] != '-' and item[0] != '<' and item != command and command_args[item] is True:
            action = item
    
    # purviewcli.client Class
    module = importlib.import_module('purviewcli.client._' + command)
    class_ = getattr(module, command.title())
    instance = class_()

    # Method
    funcStr = command + action[0].upper() + action[1:]
    funcObj = eval('instance.' + funcStr)
    data = funcObj(command_args)
    
    # Print data
    if (type(data) is dict or type(data) is list) and len(data) > 0:
        print(json.dumps(data, indent=4, sort_keys=True)) 
    elif len(data) > 0:
        print(data)
    else:
        print('[INFO] No data returned in the response.')

if __name__ == '__main__':
    main()
