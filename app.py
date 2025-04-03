import argparse, os
import json

from github_tracker import process_github_tracker

DB_PATH = 'github_db.json'

def create_json_if_not_exists(fp):
    if not os.path.exists(fp):
        try:
            with open(fp, 'w') as f:
                data = {}
                json.dump(data, f)
            print(f'File created: {fp}')
        except OSError as e:
            print(f'Error creating file: {e}')


def main():
    create_json_if_not_exists(DB_PATH)
    parser = argparse.ArgumentParser()
    parser.add_argument('user', type=str)
    args = parser.parse_args()
    process_github_tracker(args.user)


if __name__ == '__main__':
    main()