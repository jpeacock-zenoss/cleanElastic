#
# Usage: python gen.py
#
# Purpose: present a tree of services from a running serviced instance, allow the
#          selection of services, then generate scripts to remove those services
#          from elastic.

import json
import os
import re
import shutil
import subprocess
import sys


# The script won't run unless the serviced version
# matches one of these.
versions = ["1.2.[0-9]", "1.1.[0-9]"]


# Process helper
def shell(command):
        p = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return p.returncode, stdout.encode('ascii', 'ignore'), stderr.encode('ascii', 'ignore')


def yellow(message, *args):
    if len(args):
        return "%s%s%s" % ("\033[93m", message % args, "\033[0m")
    return "%s%s%s" % ("\033[93m", message, "\033[0m")


# Check the serviced version.  Fail if it isn't whitelisted.
result = shell("serviced version")
matched = False
for line in result[1].split('\n'):
    if "Version:" in line:
        ccversion = line
        break

for version in versions:
    matcher = "Version: *%s" % version
    if re.match(matcher, ccversion):
        matched = True
        break

if not matched:
    print yellow("Control Center %s is unsupported/untested", ccversion)
    sys.exit(1)


# Get the service definitions.
servicesJson = shell("serviced service list -v")
if servicesJson[0] != 0 or not servicesJson[1]:
    print "Unable to get the output from 'serviced service list -v'"
    sys.exit(1)

# Load the service data.
servicedefs = json.loads(servicesJson[1])
if len(servicedefs) == 0:
    print "No services loaded from service definition."
    sys.exit(1)

print "Got %d services" % len(servicedefs)


class Service(object):
    def __init__(self, name, serviceid, parentid):
        self.children = []
        self.name = name
        self.id = serviceid
        self.parent = parentid
        self.selected = False
    def name(self):
        return self.name
    def id(self):
        return self.id
    def parent(self):
        return self.parent
    def addChild(self, child):
        self.children.append(child)
    def children(self):
        return children
    def selection(self):
        if self.selected:
            return '[x]'
        return '[ ]'
    def select(self, value):
        self.selected = value
        for child in self.children:
            child.select(value)
    def _tree(self, level, number, items):
        items.append(self)
        result = "%3d. %s%s %s [%s]" % (number, '  '  * level, self.selection(), self.name, self.id)
        for child in self.children:
            number = number + 1
            desc, number, items = child._tree(level + 1, number, items)
            result = result + "\n" + desc
        return result.encode('ascii', 'ignore'), number, items
    def tree(self):
        """
        Returns a tuple of the string representation of the service, how many items there
        are, and an array of those items in the same order presented in the representation.
        """
        return self._tree(0, 1, [])
    def __repr__(self):
        return "%s [%s]" % (self.name, self.id)


# Process the servicedefs into a set of services.
services = []
for servicedef in servicedefs:
    service = Service(servicedef['Name'], servicedef['ID'], servicedef['ParentServiceID'])
    services.append(service)

# Find the top level service.
top = None
for service in services[:]:
    if service.parent == '':
        services.remove(service)
        top = service
        break

print "Top level service is: %s" % top

def findParent(depth, parent, service):
    for child in parent.children:
        if service.parent == child.id:
            return child
        recurse = findParent(depth + 1, child, service)
        if recurse:
            return recurse
    return None


# Create the parent/child relationships for all services.
while len(services) > 0:
    print ""
    for service in services[:]:
        if service.parent == top.id:
            services.remove(service)
            top.addChild(service)
        else:
            parent = findParent(1, top, service)
            if parent:
                services.remove(service)
                parent.addChild(service)


def writeElasticRun(runcmd):
    """
    Writes /tmp/startElastic.sh for mounting into the container.
    """
    with open('/tmp/startElastic.sh', 'w') as fd:
        fd.write('#!/bin/bash\n')
        fd.write('%s &\n' % runcmd.strip())


def parseElasticArgs(container):
    ret, stdout, stderr = shell("docker inspect %s" % container)
    args = json.loads(stdout)
    runargs=args[0]["Args"]
    elasticid=args[0]["Image"].encode('ascii', 'ignore')
    #print "Parsed container id: %s" % elasticid
    mounts=args[0]["Mounts"]
    for arg in runargs:
        match = re.match(".*(exec .*)", arg)
        if match:
            runcmd = match.group(1)
    if not runcmd:
        print "Unable to parse the Elastic start command from: %s" % runargs
        sys.exit(1)
    #print "Parsed elastic run command: %s" % runcmd
    mountcmd = ""
    for mount in mounts:
        mountcmd = "%s -v %s:%s" % (mountcmd, mount["Source"], mount["Destination"])
    #print "Parsed mounts: %s" % mountcmd
    # Add additional scripts for Elastic cleanup into /tmp in the container.
    pyScriptPath = os.path.dirname(os.path.abspath(__file__))
    mountcmd += " -v /tmp/startElastic.sh:/tmp/startElastic.sh"
    mountcmd += " -v %s/removeService.py:/tmp/removeService.py" % pyScriptPath
    mountcmd += " -v /tmp/removeServices.sh:/tmp/removeServices.sh"
    writeElasticRun(runcmd)
    return "docker run %s -it %s bash" % (mountcmd, elasticid)


def parseElasticContainer():
    """
    Looks at the docker information for elastic and creates a docker run
    command to fire up Elastic after serviced has been shut down.
    """
    ret, stdout, stderr = shell("docker ps")
    for line in stdout.split('\n'):
        if "serviced-isvcs_elasticsearch-serviced" in line:
                match = re.match("^([0-9a-z]*) ", line)
                #print "Found elastic container: %s" % match.group(0)
                runcmd = parseElasticArgs(match.group(0))
    if not runcmd:
        print "Unable to parse the Elastic args from docker. Is service running?"
        sys.exit(1)
    print ""
    print "Steps to clean services from Elastic:\n"
    print yellow("  1) Stop serviced:") + " sudo systemctl stop serviced " + yellow("(on all hosts)")
    print yellow("  2) Backup isvcs:") + " sudo tar -czvf isvcs.tgz /opt/serviced/var/isvcs " + yellow("(adjust the location of the tgz as needed)")
    print yellow("  3) run: ") + runcmd
    print yellow("    a) In the container: ") + "bash /tmp/startElastic.sh " + yellow("(wait for 'recovered [1] indices into cluster_state')")
    print yellow("       * Note: If you don't see '[1] indices', check to make sure all serviced are stopped and try again")
    print yellow("    b) In the container: ") + "bash /tmp/removeServices.sh"
    print yellow("    c) Exit the container: ") + "exit"
    print yellow("  4) run: ") + "sudo rm -rf /opt/serviced/var/isvcs/zookeeper " + yellow("*for ALL hosts*")
    print yellow("  5) Start serviced: ") + "sudo systemctl start serviced " + yellow("(master first, then delegates)")
    print ""


def process(fd, service):
    """
    Takes the selected service tree items and processes them, generating the
    scripts needed to remove them from Elastic.
    """
    print "Generating scripts for %s" % service
    fd.write("python /tmp/removeService.py %s\n" % service.id)


# Find out what services they want to remove.
while True:
    tree, count, items = top.tree()
    print tree
    response = raw_input("\nSelect a service by number, 'p' to process the items, 'quit' or 'exit' to abort: ")
    if response.isdigit():
        n = int(response)
        if n < 1 or n > len(items):
            print yellow('\nInvalid index')
            continue
        items[n-1].select(not items[n-1].selected)
        continue
    else:
        if response.startswith('quit') or response.startswith('exit') or response == 'q':
            print yellow('\nAborted\n')
            break
        if response == 'p':
            print ""
            count = 0
            fd = None
            for item in items:
                if item.selected:
                    if not fd:
                        # Create the remove command that gets mapped into
                        # the container.  This will remove each service selected.
                        fd = open('/tmp/removeServices.sh', 'w')
                        fd.write("#!/bin/bash\n\n")
                        fd.write("set -e\n")
                        fd.write("set -o pipefail\n\n")
                    count = count + 1
                    process(fd, item)
            if fd:
                fd.close()
            if count == 0:
                print yellow("\nNo services were selected")
            parseElasticContainer()
            break
        print yellow('\nInvalid selection\n')


