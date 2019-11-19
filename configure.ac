AC_INIT([RNAEditingIndexer], [0.1.b], [shalomhillel.roth@live.biu.ac.il])
# This work is licensed under the Creative Commons Attribution-Non-Commercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# For use of the software by commercial entities, please inquire with Tel Aviv University at ramot@ramot.org.
# (c) 2019 Tel Aviv University (Erez Y. Levanon, Erez.Levanon@biu.ac.il;
# Eli Eisenberg, elieis@post.tau.ac.il;
# Shalom Hillel Roth, shalomhillgel.roth@live.biu.ac.il).
AM_INIT_AUTOMAKE

AC_PROG_EGREP
AC_PROG_AWK



: ${BEDTOOLS_PATH='bedtools'}
: ${SAMTOOLS_PATH='samtools'}
: ${RESOURCES_DIR='$(DevRoot)/Resources'}
: ${BAM_UTILS_PATH='bam'}
: ${JAVA_HOME='/usr'}
: ${PYTHON27_PATH='python'}

AC_ARG_VAR(BEDTOOLS_PATH, [set bedtools invoke command. (default is: bedtools)])
AC_ARG_VAR(SAMTOOLS_PATH, [set samtools invoke command. (default is: samtools])
AC_ARG_VAR(RESOURCES_DIR, set the path of the resources dir to download to. (default is: <build dir>/Resources))
AC_ARG_VAR(JAVA_HOME, [set java home dir. (default is: /usr)])
AC_ARG_VAR(BAM_UTILS_PATH, [set bamUtils invoke command. (default is: bam)])
AC_ARG_VAR(PYTHON27_PATH, [set python 2.7 invoke command. (default is: python)])
AC_ARG_VAR(DONT_DOWNLOAD, [do not download resources, only create Resources.ini file and directories])
AC_ARG_VAR(DONT_WRITE, [do not write resources file (Resources.ini file), to avoid overriding your changes])

AC_ARG_ENABLE([download_resources],
    AS_HELP_STRING([--disable-download_resources], [do not download resources, only create Resources.ini file and directories]))

AS_IF([test "x$enable_download_resources" == "xno"], [AC_SUBST(DONT_DOWNLOAD, [true]) echo "Info: Downloading Resources is Disabled"], [AC_SUBST(DONT_DOWNLOAD, [false])])

AC_ARG_ENABLE([write_resources_ini],
    AS_HELP_STRING([--disable-write_resources_ini], [do not write resources file (Resources.ini file), to avoid overriding your changes]))

AS_IF([test "x$enable_write_resources_ini" == "xno"], [AC_SUBST(DONT_WRITE, [true]) echo "Info: Writing Resources.ini is Disabled"], [AC_SUBST(DONT_WRITE, [false])])

# test bedtools
AC_CHECK_PROG(BEDTOOLS_EXE, [$BEDTOOLS_PATH], yes)
AS_IF([test "$BEDTOOLS_EXE" == "yes" || test -x "$BEDTOOLS_PATH"], [AC_SUBST(BTV, [$(${BEDTOOLS_PATH} --version|egrep -o "(@<:@0-9@:>@{1,}\.)+@<:@0-9@:>@{1,}")])],
        [AC_MSG_ERROR(["bedtools Path Executable Test - Failed"])])
echo "bedtools Path Executable Test - Succeeded"

AS_VERSION_COMPARE([$BTV], [2.26.0], [AC_MSG_ERROR([bedtools Version Must Be Equal or Greater Than 2.26.0!(detected version ${BTV})])],
                    [echo "bedtools Version Test - Succeeded (detected version ${BTV})"],
                    [echo "bedtools Version Test - Succeeded (detected version ${BTV})"])

# test samtools
AC_CHECK_PROG(SAMTOOLS_EXE, [$SAMTOOLS_PATH], yes)
AS_IF([test "$SAMTOOLS_EXE" == "yes" || test -x "$SAMTOOLS_PATH"], [AC_SUBST(STV, [$(${SAMTOOLS_PATH} --version|  egrep -o -m 1 "(@<:@0-9@:>@{1,}\.)+@<:@0-9@:>@{1,}")])],
        [AC_MSG_ERROR(["samtools Path Executable Test - Failed"])])
echo "samtools Path Executable Test - Succeeded"
AS_VERSION_COMPARE([$STV], [1.8], [AC_MSG_ERROR([samtools Version Must Be Equal or Greater Than 1.8 (detected version ${STV})])],
                    [echo "samtools Version Test - Succeeded (detected version ${STV})"],
                    [echo "samtools Version Test - Succeeded (detected version ${STV})"])

# test bamUtils
AC_CHECK_PROG(BAM_UTILS_PATH_EXE, [$BAM_UTILS_PATH], yes)
AS_IF([test "$BAM_UTILS_PATH_EXE" == "yes" || test -x "$BAM_UTILS_PATH"], [AC_SUBST(BUV, [$(${BAM_UTILS_PATH} help 2>&1|  egrep -o -m 1 "(@<:@0-9@:>@{1,}\.)+@<:@0-9@:>@{1,}")])],
        [AC_MSG_ERROR([bamUtils Path Executable Test - Failed])])
echo "bamUtils Path Executable Test - Succeeded"
AS_VERSION_COMPARE([$BUV], [1.0.13], [AC_MSG_ERROR([bamUtils Version is Lower Than 1.0.13 (detected version ${BUV})])],
                   [echo "bamUtils Version Test - Succeeded (detected version ${BUV})"],
                   [echo "bamUtils Version Test - Succeeded (detected version ${BUV})"])
# test java
AC_SUBST(JAVA_FULL, [$JAVA_HOME/bin/java])
AC_CHECK_PROG(JAVA_FULL_EXE, [java], yes, no, [$JAVA_HOME/bin])
AS_IF([test "$JAVA_FULL_EXE" == "yes"], [AC_SUBST(JV, [$(${JAVA_FULL}  -XshowSettings:properties -version 2>&1| egrep -o -m 1 "java.version = (@<:@0-9@:>@{1,}\.)+@<:@0-9@:>@{1,}" | awk '{print $3}')])],
        [AC_MSG_ERROR([Java Path Executable Test - Failed])])
echo "Java Path Executable Test - Succeeded"
AS_VERSION_COMPARE([$JV], [1], [AC_MSG_ERROR([Java Version is Lower Than 7 (detected version ${JV})])],
                   [echo "Java Run Test - Succeeded (detected version ${JV})"],
                   [echo "Java Run  Test - Succeeded (detected version ${JV})"])

# test python
AC_CHECK_PROG(PYTHON27_PATH_EXE, [$PYTHON27_PATH], yes)
AS_IF([test "$PYTHON27_PATH_EXE" == "yes" || test -x "$PYTHON27_PATH"], [AC_SUBST(PV, [$(${PYTHON27_PATH} --version 2>&1| egrep -o -m 1 "(@<:@0-9@:>@{1,}\.)+@<:@0-9@:>@{1,}")])],
        [AC_MSG_ERROR([Python 2.7 Path Executable Test - Failed])])
echo "Python Path Executable Test - Succeeded"
AS_VERSION_COMPARE([$PV], [2.7], [AC_MSG_ERROR([Python Version Must Be 2.7.x! (detected version ${PV})])])
AS_VERSION_COMPARE([$PV], [3.0], [echo "Python Path Executable Test - Succeeded!"],
[AC_MSG_ERROR([Python Version Must Be 2.7.x! (detected version ${PV})])],
[AC_MSG_ERROR([Python Version Must Be 2.7.x! (detected version ${PV})])],
)

AC_CONFIG_FILES([Makefile make/Makefile src/EditingIndexJavaUtils/Makefile])

AC_OUTPUT