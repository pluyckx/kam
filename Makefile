INSTALL_DIR = /usr/lib/kam
BIN_DIR = /usr/sbin
BIN_NAME = kamd
INIT_NAME = kam

.PHONY: all
all:
	# do nothing

.PHONY: install
install:
	

.PHONY: uninstall
uninstall:

.PHONY: update
update:
	$(MAKE) install
	$(MAKE) uninstall

