import os
import sys

# Newer pytest defaults to importmode=importlib, which does not put the
# rootdir on sys.path the way the older `prepend` mode did — so `import src.*`
# from tests/ has to be made to resolve explicitly.
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Must be set before anything imports src.config / src.db, which read env
# and build the engine at import time.
os.environ.setdefault("DB_URL", "sqlite://")
os.environ.setdefault("SLACK_WEBHOOK", "")
