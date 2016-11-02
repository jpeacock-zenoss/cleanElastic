#
# Removes the service from Elastic specified as an argument.  If we see something that doesn't look
# right in queries/validation, prompt for an exit.
#

import json
import subprocess
import sys


# Process helper
def shell(command):
        p = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return p.returncode, stdout.encode('ascii', 'ignore'), stderr.encode('ascii', 'ignore')


def exit(message):
    print message
    response = raw_input("Press [enter] to exit, 'i' to ignore and continue: ")
    if not response == 'i':
        print "Exiting script.."
        sys.exit(1)


def getService():
    """
    Checks the command line for the right arguments.
    """
    args = sys.argv
    # Check arguments
    if not len(args) == 2:
        exit("Usage: %s <serviceid>" % __file__)
    # Get the service id.
    return args[1]


def verifyService(id):
    """
    Verifies that the service exists in elastic, and gives us the
    opportunity to abort if things don't work right.
    """
    ret = shell("curl -XGET 'http://localhost:9200/controlplane/service/%s'" % id)
    jsonData = json.loads(ret[1])
    if not jsonData:
        exit("Unable to parse Elastic return: %s" % ret[1])
    if "error" in jsonData:
        exit("Error validating service in Elastic: %s" % jsonData["error"])
    if not jsonData["exists"]:
        exit("Service '%s' doesn't exist in elastic" % id)


def removeService(id):
    """
    Performs the removal of the service from Elastic.
    """
    # Delete the service.
    print "Removing service %s.." % id
    shell("curl -XDELETE 'http://localhost:9200/controlplane/service/%s'" % id)
    # Delete the address assignment (if any)
    print "Removing address assignment (if any) for %s.." % id
    removeAssignments(id)
    # Remove all service configs for this service.
    print "Removing service configs for %s.." % id
    removeConfigs(id)


def removeAssignments(id):
    """
    Queries for all address assignments for the given service id.
    We have to query for assignments, then iterate the document ids to remove them.
    """
    query = '{ "query": { "filtered": { "filter": { "bool": { "must": [ {"query": {"wildcard": {"ServiceID": "%s"}}}, {"query": {"wildcard": {"_type": "addressassignment"}}} ] } } } } }' % id
    cmd = "curl -H \"Content-Type: application/json\" -XGET -d '%s' http://localhost:9200/_search" % query
    ret = shell(cmd)
    jsonData = json.loads(ret[1])
    if not jsonData:
        exit("Error querying for address assignments")
    # Get just the hit data
    jsonData = jsonData["hits"]
    # For each hit, delete the address assignment
    for hit in jsonData["hits"]:
        cmd = "curl -XDELETE 'http://localhost:9200/controlplane/addressassignment/%s'" % hit["_id"]
        shell(cmd)


def removeConfigs(id):
    """
    Queries for service config matches for this service id, then removes
    each of the configs.
    """
    cmd = "curl -H \"Content-Type: application/json\" -XGET -d '{\"fields\": [\"_id\"], \"query\": {\"wildcard\": { \"ServicePath\":  \"*/%s\" }}}' http://localhost:9200/_search" % id
    ret = shell(cmd)
    jsonData = json.loads(ret[1])
    if not jsonData:
        exit("Error querying for service configs")
    # Get just the hit data
    jsonData = jsonData["hits"]
    # For each hit, delete the config
    for hit in jsonData["hits"]:
        cmd = "curl -XDELETE 'http://localhost:9200/controlplane/svcconfigfile/%s'" % hit["_id"]
        shell(cmd)


if __name__ == "__main__":
    id = getService()
    verifyService(id)
    removeService(id)
