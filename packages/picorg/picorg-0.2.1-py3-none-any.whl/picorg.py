import argparse
from pathlib import Path

import settings
from duplicates import handle_duplicates
from rename import rename_files


def main():
    parser = argparse.ArgumentParser(
        description="A script that helps you organize your pictures."
    )
    parser.add_argument(
        "-a",
        "--action",
        choices=["rename", "duplicates"],
        required=True,
        help="The action to execute.",
    )

    args = parser.parse_args()

    if args.action == "rename":
        rename_files()
    elif args.action == "duplicates":
        pic_paths = settings.get("pic_paths", [])
        result = handle_duplicates([Path(p) for p in pic_paths])
        print(f"Found {len(result)} duplicates.")


if __name__ == "__main__":
    main()
