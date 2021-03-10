PYTHON	= python3

.PHONY	= help all run clean

.DEFAULT_GOAL	= help

help: 
	@echo " This is the 3Ddosimetry program         "
	@echo "						"
	@echo " Written by Lia Valdetaro		"
	@echo " Contact info: liavaldetaro@gmail.com	"
	@echo "                                         "
	@echo "---------------- HELP ----------------   "
	@echo "* To test the setup, type 'make test'    "
	@echo "	- this tests that all the directories can be found"
	@echo " 					"
	@echo "* To clean temp files, type 'make clean' "
	@echo "	- removes the temporary files		"
	@echo "						"
	@echo "* To convert the files from vff to mat format, type 'make convert'"
	@echo "                                         "
	@echo "* To prepare the data sets, type 'make prepare'"
	@echo "	- prepares the data sets by cropping the raw "
	@echo "	  files, and aligning all the data sets"
	@echo "                                        "
	@echo "--------------------------------------"

current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))

directory = $(current_dir)data

directory_lib = $(current_dir)lib

test: | $(directory) $(directory_lib)
$(directory):
	@echo "Folder $(directory) does not exist!"
$(directory_lib):
	@echo "Folder $(directory_lib) does not exist!"

convert:
	${PYTHON} $(directory_lib)/vff2mat.py
prepare: 
	${PYTHON} $(directory_lib)/crop_data.py
	${PYTHON} $(directory_lib)/align_data.py

clean:
	rm -r *.txt *.log 
