QUIET=@
ECHO=echo
RM=rm -f

all:

test:
	$(QUIET)$(ECHO) "Program Test"
	./Benchmark.py ../data/Setting.json
	./Main.py ../data/Setting.json ../data/File.meta ../data/Weight.json

clean:
	$(QUIET)$(ECHO) "Removing compiled files"
	$(QUIET)$(RM) *.pyc
