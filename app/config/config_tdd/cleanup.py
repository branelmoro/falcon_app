CLEANUPQUEUE = []

def DOCLEANUP():
	for i in CLEANUPQUEUE:
		i.doCleanUp()