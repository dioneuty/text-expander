import argparse

from src.debug_log import configure
from src.gui.app import Application


def main() -> None:
    parser = argparse.ArgumentParser(description="단축어 프로그램")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="키보드 후킹 디버그 로그 (data/hook_debug.log)",
    )
    args = parser.parse_args()
    configure(args.debug)
    Application().run()


if __name__ == "__main__":
    main()
