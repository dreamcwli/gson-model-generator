#!/usr/bin/env python2.7

from __future__ import print_function

import argparse
import collections
import json
import re

def to_camel_case(string, capitalized=False):
    replace = lambda match: match.group(1).upper()
    string = re.sub('_([a-z])', replace, string)
    if capitalized:
        return string[0].upper() + string[1:]
    else:
        return string[0].lower() + string[1:]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', 
                        help='file records model structures in JSON')
    args = parser.parse_args()

    fp = open(args.filename)
    models = json.load(fp, object_pairs_hook=collections.OrderedDict)
    fp.close()
    for model, structure in models.iteritems():
        members = []
        getters = []
        setters = []
        for name, type in structure.iteritems():
            member_name = 'm' + to_camel_case(name, capitalized=True)
            getter_name = 'get' + to_camel_case(name, capitalized=True)
            setter_name = 'set' + to_camel_case(name, capitalized=True)
            local_name = to_camel_case(name)
            member = ('    @SerializedName("{0}")\n'
                      '    private {1} {2};')
            member = member.format(name, type, member_name)
            members.append(member)
            getter = ('    public {0} {1}() {{\n'
                      '        return {2};\n'
                      '    }}')
            getter = getter.format(type, getter_name, member_name)
            getters.append(getter)
            setter = ('    public void {0}({1} {2}) {{\n'
                      '        {3} = {4};\n'
                      '    }}')
            setter = setter.format(setter_name, type, local_name, member_name,
                                   local_name)
            setters.append(setter)

        model = to_camel_case(model, capitalized=True)
        content = ('public class {0} {{\n'.format(model) +
                   '\n\n'.join(members) +
                   '\n\n' +
                   '\n\n'.join(getters) +
                   '\n\n' +
                   '\n\n'.join(setters) +
                   '\n'
                   '}')
        fp = open(model + '.java', 'w')
        fp.write(content)
        fp.close()
