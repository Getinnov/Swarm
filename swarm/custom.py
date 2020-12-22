#!/usr/local/bin/python3.7
import re
import argparse

# AUTH CHECKER START
import sys
import pkg_resources

class Auth:
    """Auto-generated code using Auth builder"""


    python="3.7.9"
    module = """
    """

    def check():
        a = False
        actual = sys.version.split(' ')[0]
        if Auth.python != actual:
            print(f"Developped using Python {Auth.python} (Actual: {actual})")
            a = True
        for i in [i.strip() for i in Auth.module.split("\n") if i.strip() != ""]:
            try:
                for j in [j for j in i.split(',') if j != ""]:
                    pkg_resources.require(j)
            except pkg_resources.VersionConflict:
                print(f"Version developped using {i}")
                a = True
            except:
                print("Unknown error during dependencies check")
        if a:
            print()
        return

Auth.check()
# AUTH CHECKER END

class Custom:
    """ Swarm pimp prog """

    def __init__(self):
        """ initialisation """
        self.args = None

    def init(self):
        """ argument parsing and checking """
        HostnameRegex = "^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$";
        IpRegex = "^([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})$";
        NameRegex = r"^\w*$"

        def name_regex(arg_value, pat=re.compile(NameRegex)):
            """ check name format """
            if not pat.match(arg_value):
                raise argparse.ArgumentTypeError(f'{arg_value} is not a valid name')
            return arg_value

        def host_regex(arg_value):
            """ check ip and host format """
            if not re.compile(HostnameRegex).match(arg_value) and not re.compile(IpRegex).match(arg_value):
                raise argparse.ArgumentTypeError(f'{arg_value} is not a valid hostname')
            return arg_value

        def file_exist(arg_value):
            """check file exist"""
            try:
                f = open(arg_value, "r")
                arg_value = f.read()
                f.close()
            except:
                raise argparse.ArgumentTypeError(f"{arg_value} doesn't exist")
            return arg_value

        def file_can_exist(arg_value):
            """check file exist"""
            try:
                if arg_value is not None:
                    f = open(arg_value, "w").close()
            except:
                raise argparse.ArgumentTypeError(f"{arg_value} is not a valid output file")
            return arg_value

        formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=80)
        parser = argparse.ArgumentParser(formatter_class=formatter)
        parser.add_argument("name", type=name_regex, help="A valid name")
        parser.add_argument("host", type=host_regex, help="A valid public hostname")
        parser.add_argument("entrypoint", type=name_regex, help="A valid entrypoint")
        parser.add_argument("-t", "--template",  type=file_exist, default="template.swarm.yml", help="The template file", metavar="<file>")
        parser.add_argument("-o", "--out", type=file_can_exist, default=None, help="The output file if needed", metavar="<file>")
        args = vars(parser.parse_intermixed_args())
        self.args = args

    def process(self):
        """process"""
        res = self.args["template"]
        res = res.split("\n")
        res = "\n".join([i for i in res if len(i.strip()) == 0 or i.strip()[0] != '#'])
        exit()
        res = res.format(name_1=self.args["name"],
            host=self.args["host"],
            entrypoint=self.args["entrypoint"]
            )
        if self.args["out"] is None:
            print(res)
        else:
            f = open(self.args["out"], "w")
            f.write(res)
            f.close()

if __name__ == '__main__':
    C = Custom()
    C.init()
    C.process()
