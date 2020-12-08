PYTHON	= python3

.PHONY	= help all run clean

.DEFAULT_GOAL	= help

help: 
	@echo "---------------- HELP ----------------"
	@echo "* To test the setup, type 'make test'    "
	@echo "* To clean temp files, type 'make clean' "
	@echo "* To prepare the data sets, type 'make prepare'"
	@echo "--------------------------------------"

current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))

directory = $(current_dir)data

directory_lib = $(current_dir)lib

test: | $(directory) $(directory_lib)
$(directory):
	@echo "Folder $(directory) does not exist!"
$(directory_lib):
	@echo "Folder $(directory_lib) does not exist!"

prepare: 
	${PYTHON} $(directory_lib)/crop_data.py

clean:
	rm -r *.txt *.log 
