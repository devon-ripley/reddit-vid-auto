import main
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('grab')
parser.add_argument('-p', '--path_vid')
parser.add_argument('-s', '--save')
parser.add_argument('-i', '--id')
parser.add_argument('-n', '--non_api')
parser.add_argument('-t', '--target_s', action="store_true")
parser.add_argument('-v', '--vertical', action="store_true")
parser.add_argument('-c', '--target_c', action="store_true")

args = parser.parse_args()
main.vid_auto(args.grab, args.path_vid, args.save, args.id, args.target_s, args.vertical, args.target_c, args.non_api)
