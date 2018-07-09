JavaPackages = \
          JavaModules/BEDUtils

JavaLibraries = \
	JavaModules/JavaLibs/commons-cli-1.4.jar


JavaMainClass = \
   	JavaModules.BEDUtils.EditingIndexBEDUtils

RunParameters =

# Javadoc
JavadocWindowTitle = 'A-to-I RNA Editing Index Java Utils'
JavadocDocTitle    = 'A-to-I RNA Editing Index'
JavadocHeader      = 'A-to-I Editing Index'
JavadocFooter      =

include $(DEV_ROOT)/make/Makefile
