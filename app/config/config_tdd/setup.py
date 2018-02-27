try:
	from ..env import env as enviornment
except ImportError:
	enviornment = "production"

print(enviornment)

CLEANUPQUEUE = []

def DOCLEANUP():
	print("Doing Cleanup")
	for i in CLEANUPQUEUE:
		i.doCleanUp()
	print("Done")