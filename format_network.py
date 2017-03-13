import ndex.client as nc
import ndex.networkn as networkn
import ndex.beta.layouts as layouts
import ndex.beta.toolbox as toolbox
import argparse

# This is an example python command line script to
# get an NDEx network by its UUID
# optionally apply a graphic style from another network (a template)
# apply a layout
# and save the result to NDEx

parser = argparse.ArgumentParser(description='upload-ebs-to-ndex arguments')

# Argument Attributes:

# name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
# action - The basic type of action to be taken when this argument is encountered at the command line.
# nargs - The number of command-line arguments that should be consumed.
# const - A constant value required by some action and nargs selections.
# default - The value produced if the argument is absent from the command line.
# type - The type to which the command-line argument should be converted.
# choices - A container of the allowable values for the argument.
# required - Whether or not the command-line option may be omitted (optionals only).
# help - A brief description of what the argument does.
# metavar - A name for the argument in usage messages.
# dest - The name of the attribute to be added to the object returned by parse_args().


parser.add_argument('-i',
                    action='store',
                    dest='network_id',
                    default=None
                    )

parser.add_argument('-n',
                    action='store',
                    dest='server',
                    help='NDEx server for the target NDEx account',
                    default='http://www.ndexbio.org'
                    )

parser.add_argument('-u',
                    dest='username',
                    action='store',
                    help='username for the target NDEx account')

parser.add_argument('-p',
                    dest='password',
                    action='store',
                    help='password for the target NDEx account')


parser.add_argument('-t',
                    action='store',
                    dest='template_id',
                    help='network id for the network to use as a graphic template')


args = parser.parse_args()

print(vars(args))

ndex = nc.Ndex(args.server, args.username, args.password)

print("getting network: %s" % args.network_id)
response = ndex.get_network_as_cx_stream(args.network_id)
cx = response.json()
network = networkn.NdexGraph(cx)

if args.template_id:
    print("getting template network: %s" % args.template_id)
    response = ndex.get_network_as_cx_stream(args.template_id)
    template_cx = response.json()
    template_network = networkn.NdexGraph(template_cx)
    print("applying graphic style")
    toolbox.apply_network_as_template(network, template_network)

print("applying layout")
layouts.apply_directed_flow_layout(network, iterations=150, use_degree_edge_weights=True)

# useful for debugging:
# network.write_to('temp_network.cx')

# print("updating network")
# ndex.update_cx_network(network.to_cx_stream(), args.network_id)

print("saving new network with formatting")
ndex.save_new_network(network.to_cx())





