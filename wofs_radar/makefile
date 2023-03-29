all: 
	rm -f utils/*.so
	f2py3 --f90flags='-O3' -c -m cressman utils/cressman.f90
	f2py3 --f90flags='-O3' -c -m sparsey utils/sparsey.f90

	cp *.so utils