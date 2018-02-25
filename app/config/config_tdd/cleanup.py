CLEANUPQUEUE = []

def DOCLEANUP():
	print("Doing Cleanup")
	for i in CLEANUPQUEUE:
		i.doCleanUp()
	print("Done")