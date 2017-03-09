#! python3

PROFILE = "~/comiccrawler"

from os import getcwd
from os.path import expanduser, normpath, join

def set(profile):
	global PROFILE
	PROFILE = profile

def get(file=None):
	if file is not None:
		return normpath(join(getcwd(), expanduser(PROFILE), expanduser(file)))
	else:
		return normpath(join(getcwd(), expanduser(PROFILE)))
