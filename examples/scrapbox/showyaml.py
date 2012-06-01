import yaml
import json
import sys
print json.dumps(yaml.load(open(sys.argv[1])), indent=2)
