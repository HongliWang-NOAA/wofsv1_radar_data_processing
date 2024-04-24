all: 
	rm -f utils/*.so
	python -m numpy.f2py --f90flags='-O3' -c -m cressman utils/cressman.f90
	python -m numpy.f2py --f90flags='-O3' -c -m sparsey utils/sparsey.f90

	cp *.so utils