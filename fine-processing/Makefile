REQ_VER := 3.6
REQ_PY  := $(shell command -v python$(REQ_VER) 2> /dev/null)

REQUIREMENTS := requirements.txt

ENV_DIR  := env
ENV_BIN  := $(ENV_DIR)/bin
ACTIVATE := $(ENV_BIN)/activate
PIP      := $(ENV_BIN)/pip
PY       := $(ENV_BIN)/python

SRC_DIR  := python_scripts


init: $(ACTIVATE)

$(ACTIVATE): $(REQUIREMENTS)
ifndef REQ_PY
	$(error Need python version $(REQ_VER) to run)
else
	virtualenv -p $(REQ_PY) $(ENV_DIR) --no-site-packages
	$(PIP) install -r $(REQUIREMENTS)
	touch $(ACTIVATE)
endif
