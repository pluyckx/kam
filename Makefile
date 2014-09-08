INSTALL_DIR = /usr/lib/kam
BIN_DIR = /usr/sbin
ETC_DIR = /etc/kam

BIN_NAME = kamd
INIT_NAME = kam

.PHONY: all
all:
	# do nothing

.PHONY: python3
python3:
	@dpkg -l python3 2>&1 > /dev/null; \
	if [ $$? -ne 0 ]; \
	then \
		apt-get install python3; \
	fi

.PHONY: python3-psutil
python3-psutil:
	@dpkg -l python3-psutil 2>&1 > /dev/null; \
	if [ $$? -ne 0 ]; \
	then \
		apt-get install python3-psutil; \
	fi

.PHONY: install
install: python3 python3-psutil
	@echo "Installing kam"
	@if [ -e "$(ETC_DIR)/version" ]; \
	then \
		echo "Kam is already installed, please uninstall it first!"; \
		exit 1; \
	fi

	mkdir -p $(INSTALL_DIR)
	mkdir -p $(ETC_DIR)
	mkdir -p $(BIN_DIR)

	cp -r kam_src/* $(INSTALL_DIR)
	if [ -e $(BIN_DIR)/$(BIN_NAME) ]; \
	then \
		rm $(BIN_DIR)/$(BIN_NAME); \
	fi

	ln -s $(INSTALL_DIR)/kam.py $(BIN_DIR)/$(BIN_NAME)

	cp kam.conf $(ETC_DIR)
	cp version $(ETC_DIR)
	cp kam.init /etc/init.d/kam

	update-rc.d kam defaults
	service kam start

.PHONY: uninstall-0.x
uninstall-0.x:
	@if [ -e "$(ETC_DIR)/version" ]; \
	then \
		version=$$(cat "$(ETC_DIR)/version"); \
	elif [ -e "$(ETC_DIR)" ]; \
		version="0.?"; \
	fi; \
	\
	if [ "$$(version)" != "" ]; \
	then \
		echo $$(version) | grep "^0\." 2>&1 > /dev/null; \
		if [ $$? -eq 0 ]; \
		then \
			echo "uninstall-0.x version $$(version)"; \
			rm /usr/sbin/kamd; \
			rm /etc/init.d/kam; \
			update-rc.d kam remove; \
		fi; \
	fi;		

.PHONY: uninstall
uninstall: uninstall-0.x
	@if [ -e "$(ETC_DIR)/version" ]; \
	then \
		echo "Uninstall version $$(cat \"$(ETC_DIR)/version\")"; \
		service kam stop; \
		rm /etc/init.d/kam; \
		update-rc.d kam remove; \
		\
		rm $(BIN_DIR)/$(BIN_NAME); \
		rm -r $(INSTALL_DIR); \
		rm -r $(ETC_DIR); \
	fi

.PHONY: update
update:
	$(MAKE) uninstall
	$(MAKE) install

