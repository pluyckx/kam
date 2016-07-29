
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
	@rm -R kamd.egg-info 2> /dev/null || echo "kamd.egg-info directory does not exist"
	@rm -R ../kamd_* 2> /dev/null || echo "../kamd_* files do not exist"
	@rm ../python3-kamd* 2> /dev/null || echo "../python3-kamd* files do not exist"
	@rm ../python-kamd* 2> /dev/null || echo "../python-kamd* files do not exist"
