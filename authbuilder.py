#!/usr/local/bin/python3.7
"""
The main goal of this project is to create a handy, automated way to
generate code that will be able to check dependencies and authenticity for a given script
"""
import argparse
import sys
import pkg_resources
import inspect
import importlib
from modulefinder import ModuleFinder
import hashlib
import json

class Auth:
    python = "3.7.9"
    module = """
    """
    hash = {}

    def check():
        a = False
        b = False
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
        for i, j in inspect.getmembers(sys.modules[__name__]):
            if i != "Auth" and str(j) == f"<class '__main__.{i}'>":
                source = inspect.getsource(j)
                h = hashlib.sha256(source.encode('utf-8')).hexdigest()
                if i not in Auth.hash or h != Auth.hash[i]:
                    print(f"Integrity compromised on module {i}")
                    b = True
        if b:
            exit()
        if a:
            print()
        return

    def build(file):
        path = file.replace("./", "").replace("/", ".")[:-3]
        mod = importlib.import_module(path)
        obj = [x for x in dir(mod) if inspect.isclass(type(x))]
        h = {}
        for i in obj:
            if i != "Auth" and str(getattr(mod, i)) == f"<class '{path}.{i}'>":
                source = inspect.getsource(getattr(mod, i))
                hash = hashlib.sha256(source.encode('utf-8')).hexdigest()
                h[i] = hash
        h = json.dumps(h).replace(",", ",\n" + " " * 11)[1:-1]
        finder = ModuleFinder()
        finder.run_script(file)
        imp = "import sys\nimport hashlib\nimport inspect\nimport pkg_resources"
        name = "class Auth:"
        header = "\"\"\"Auto-generated code using Auth builder\"\"\""
        code = inspect.getsource(Auth.check)
        python = f"""python=\"{sys.version.split(' ')[0]}\""""
        module = "module = \"\"\""
        hash = f"hash = {{\n{' ' * 12 + h}\n{' ' * 11}}}"
        for i, mod in finder.modules.items():
            try:
                if len(i.split('.')) == 1:
                    v = pkg_resources.get_distribution(i).version
                    module += f"\n{' ' * 14}{i}=={v}"
            except:
                continue
        module += f"\n{' ' * 13}\"\"\""
        print(f"# AUTH CHECKER START\n{imp}")
        print(f"\n{name}\n    {header}\n")
        print(f"\n    {python}\n    {module}")
        print(f"    {hash}\n\n\n{code}")
        print("\nAuth.check()\n# AUTH CHECKER END")
        return

if __name__ == '__main__':
    Auth.check()

    def module_exist(arg_value):
        """check file exist"""
        try:
            f = open(arg_value, "r")
            f.close()
        except:
            raise argparse.ArgumentTypeError(f"{arg_value} doesn't exist")
        path = arg_value.replace("./", "").replace("/", ".")[:-3]
        try:
            importlib.import_module(path)
        except:
            raise argparse.ArgumentTypeError(f"{path} is not a valid module")
        return arg_value

    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=80)
    parser = argparse.ArgumentParser(formatter_class=formatter)
    parser.add_argument("file", type=module_exist, help="A valid python script")
    args = vars(parser.parse_intermixed_args())
    if args["file"] is not None:
        Auth.build(args["file"])
