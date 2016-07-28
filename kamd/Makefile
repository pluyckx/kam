
builddeb: clean
	@tar -cJf ../kamd_$$(cat etc/kam/version).orig.tar.xz --exclude=debian --exclude=kamd.egg-info *
	@dch -r
	debuild
	rm -R kamd.egg-info
	debuild -S

newversion:
	@dch -v ${DCHVERSION}

inc:
	@dch -i

clean:
	if [ -e kamd.egg-infi ]; then rm -R kamd.egg-info; fi
	rm ../kamd_*
	rm ../python3-kamd*
	rm ../python-kamd*
