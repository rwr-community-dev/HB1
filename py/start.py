"""start.py - rwr-community-dev utility script for package testing.

Usage:
    start.py
"""
import dataclasses
import sys
import time
import pathlib
import subprocess
import xml.etree.ElementTree as XmlET

# import docopt

# this magic allows for Ctrl+C to PyCharm run console to be handled nicely
try:
    from console_thrift import KeyboardInterruptException as KeyboardInterrupt  # noqa
except ImportError:
    pass

PY_DIR = pathlib.Path(__file__).parent
PKG_DIR, SCRIPTS_DIR = PY_DIR.parent, PY_DIR.parent / "scripts"
PKG_CFG = PKG_DIR / "package_config.xml"
RWR_ROOT = PKG_DIR.parent.parent.parent
RWR_GAME, RWR_SERV = RWR_ROOT / "rwr_game.exe", RWR_ROOT / "rwr_server.exe"
RWR_STEAM_URI = "steam://rungameid/270150//"


@dataclasses.dataclass
class PackageConfig:
    name: str
    description: str
    campaign_entry_script: str
    quickmatch_entry_script: str

    @classmethod
    def fromXmlFile(cls, path: pathlib.Path):
        with path.open(mode="r", encoding="utf-8") as f:
            pkg_cfg_xml = XmlET.fromstring(f.read())
        name = pkg_cfg_xml.attrib["name"]
        description = pkg_cfg_xml.attrib["description"]
        campaign_entry_script = pkg_cfg_xml.attrib["campaign_entry_script"]
        quickmatch_entry_script = pkg_cfg_xml.attrib["quick_match_entry_script"]
        return cls(name, description, campaign_entry_script, quickmatch_entry_script)


if __name__ == '__main__':
    # args = docopt.docopt(__doc__)
    # print(f"docopt args={args}")

    # print(PKG_DIR)
    print(f"Starting RWR from within '{PKG_DIR}'...")
    if not PKG_CFG.exists():
        print(f"Error: no package_config.xml found in '{PKG_DIR}' :/")
        sys.exit(1)

    print("Reading package config...")
    # with PKG_CFG.open(mode="r", encoding="utf-8") as f:
    pkg_cfg = PackageConfig.fromXmlFile(PKG_CFG)
    print(f"Package name: {pkg_cfg.name}, script: {pkg_cfg.campaign_entry_script}")

    print("Locating RWR server executable...")
    if not RWR_SERV.exists():
        print(f"Error: couldn't find rwr_server in '{RWR_ROOT}' :cry:")
        sys.exit(2)

    print(f"Starting '{RWR_SERV}'...")
    rwr_serv_args = [f"{RWR_SERV}"]
    # print(rwr_serv_args)

    rwr_serv = subprocess.Popen(rwr_serv_args, cwd=RWR_ROOT.absolute(), encoding="utf-8",
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    try:
        trailing_data = None
        while True:
            # for line in sys.stdin:
            #     print(line)
            output_line = rwr_serv.stdout.readline()
            print(output_line, end="")
            stripped_line = output_line.strip()
            if stripped_line == "Game loaded":
                print(f"Starting script '{pkg_cfg.campaign_entry_script}'...")
                rwr_serv.stdin.write("help\n")
                # rwr_serv.stdin.write()
                rwr_serv.stdin.flush()
                pkg_dir = f"media/packages/{PKG_DIR.name}"
                print(pkg_dir)
    except KeyboardInterrupt:
        print("Ctrl-C detected, shutting down!")
        rwr_serv.kill()
        # rwr_serv.stdin.write("quit\n")
        # rwr_serv.stdin.flush()

    # oouts, oerrs = None, None
    # try:
    #     while True:
    #         try:
    #             outs, errs = rwr_serv.communicate(timeout=3)
    #             print(f"{outs=}\n{errs=}")
    #             if outs != oouts:
    #                 for out in outs:
    #                     print(f"~ {out!r}")
    #             if errs != oerrs:
    #                 for err in errs:
    #                     print(f"~ {err!r}")
    #             # print(f"sdfc{outs=}\n{errs=}")
    #             oouts, oerrs = outs, errs
    #             time.sleep(0.1)
    #         except subprocess.TimeoutExpired as e:
    #             print(f"timeout expired - {e.stdout} :/")
    #             time.sleep(2)
    # except KeyboardInterrupt:
    #     print("Ctrl-C detected - shutting down...")
    #     # print(rwr_serv.stdout.read())
    #     rwr_serv.kill()

    # try:
    #     while True:
    #         i = input(">> ").lower()
    #         if i in ["q", "quit"]:
    #             print("Quitting...")
    #             break
    # except KeyboardInterrupt:
    #     print("Ctrl-C detected!")

