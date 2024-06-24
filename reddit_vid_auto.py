import main
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('grab')
parser.add_argument('-p', '--vid_path')
parser.add_argument('-s', '--save_path')
parser.add_argument('-i', '--id')
parser.add_argument('-n', '--non_api')
parser.add_argument('-t', '--target_s', action="store_true")
parser.add_argument('-v', '--vertical', action="store_true")
parser.add_argument('-c', '--target_c', action="store_true")
parser.add_argument('-j', '--json_save', action="store_true")

args = parser.parse_args()
if args.json_save:
    main.save_story(grab=args.grab, sub_id=args.id, story_target=args.target_s)
else:
    main.vid_auto(args.grab, args.vid_path, args.save_path, args.id, args.target_s, args.vertical, args.target_c, args.non_api)
