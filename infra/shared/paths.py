from pathlib import PurePath, Path

THIS_DIRECTORY = Path(__file__).parent.absolute()
APP_PATH = str(PurePath(THIS_DIRECTORY.parent.parent, "app"))
WEB_PATH = str(PurePath(APP_PATH, "web"))
API_PATH = str(PurePath(APP_PATH, "api"))
WEB_DIST_PATH = str(PurePath(WEB_PATH, "dist"))