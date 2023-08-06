import os
import subprocess
import sys

def filestart(filename):
	try:
		try:
			os.startfile(filename)
		except Exception:
			opener = "open" if sys.platform == "darwin" else "xdg-open"
			subprocess.call([opener, filename])

	except Exception as e:
		print(f"Could Not Start File: {e}")
