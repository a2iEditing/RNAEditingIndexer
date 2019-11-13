AC_INIT([RNAEditingIndexer], [0.1.b], [shalomhillel.roth@live.biu.ac.il])
AM_INIT_AUTOMAKE

AC_PROG_EGREP
AC_PROG_AWK

AC_SUBST(DEV_ROOT, $abs_top_srcdir)
AC_SUBST(IS_UNIX, true)
AC_SUBST(BEDTOOLS_PATH, [bedtools])
AC_SUBST(SAMTOOLS_PATH, [samtools])
AC_SUBST(RESOURCES_DIR, [$srcdir/Resources])
AC_SUBST(JAVA_HOME, [/usr])
AC_SUBST(BAM_UTILS_PATH, [bam])
AC_SUBST(PYTHON27_PATH, [python])
AC_SUBST(DONT_DOWNLOAD, [false])
AC_SUBST(DONT_WRITE, [false])

AC_ARG_VAR(BEDTOOLS_PATH, [set bedtools invoke command. (default is: bedtools)])
AC_ARG_VAR(SAMTOOLS_PATH, [set samtools invoke command. (default is: samtools)])
AC_ARG_VAR(RESOURCES_DIR, set the path of the resources dir to download to. (default is: $srcdir/Resources))
AC_ARG_VAR(JAVA_HOME, [set java home dir. (default is: /usr)])
AC_ARG_VAR(BAM_UTILS_PATH, [set bamUtils invoke command. (default is: bam)])
AC_ARG_VAR(PYTHON27_PATH, [set python 2.7 invoke command. (default is: python)])
AC_ARG_VAR(DONT_DOWNLOAD, [do not download resources, only create Resources.ini file and directories])
AC_ARG_VAR(DONT_WRITE, [do not write resources file (Resources.ini file), to avoid overriding your changes])

# test bedtools
AS_IF([AS_EXECUTABLE_P(BEDTOOLS_PATH)], [BTV=$(${BEDTOOLS_PATH} --version|  egrep -o "([0-9]{1,}\.)+[0-9]{1,}"|awk -F "." '(($1 > 2)||($1 ==2 && $2 > 25))')],
        [AC_MSG_ERROR(["bedtools Path Executable Test - Failed"])])
echo "bedtools Path Executable Test - Succeeded"
AS_VERSION_COMPARE([BTV], [2.26.0], [AC_MSG_ERROR(["bedtools Version Must Be Equal or Greater Than 2.26.0 (detected version ${BTV})"]],
                    [echo "bedtools Version Test - Succeeded (detected version ${BTV})"],
                    [echo "bedtools Version Test - Succeeded (detected version ${BTV})"])

# test samtools
AS_IF([AS_EXECUTABLE_P(SAMTOOLS_PATH)], [STV=$(${SAMTOOLS_PATH} --version|  egrep -o -m 1 "([0-9]{1,}\.)+[0-9]{1,}"|awk -F "." '($1 >=1 && $2 > 7)')],
        [AC_MSG_ERROR(["samtools Path Executable Test - Failed"])])
echo "samtools Path Executable Test - Succeeded"
AS_VERSION_COMPARE([STV], [1.8], [AC_MSG_ERROR(["samtools Version Must Be Equal or Greater Than 1.8 (detected version ${STV})"]],
                    [echo "samtools Version Test - Succeeded (detected version ${STV})"],
                    [echo "samtools Version Test - Succeeded (detected version ${STV})"])

# test bamUtils
AS_IF([AS_EXECUTABLE_P(BAM_UTILS_PATH)], [BUV=$(${BAM_UTILS_PATH} help 2>&1|  egrep -o -m 1 "([0-9]{1,}\.)+[0-9]{1,}")],
        [AC_MSG_ERROR(["bamUtils Path Executable Test - Failed"])])
echo "bamUtils Path Executable Test - Succeeded"
AS_VERSION_COMPARE([BUV], [1.8], [AC_MSG_WARN(["bamUtils Version is Lower Than 1.0.13 (detected version ${BUV})"]],
                   [echo "bamUtils Version Test - Succeeded (detected version ${BUV})"],
                   [echo "bamUtils Version Test - Succeeded (detected version ${BUV})"])
# test java
JAVA_FULL="${JAVA_HOME}/bin/java"
AS_IF([AS_EXECUTABLE_P(JAVA_FULL)], [JV=$(${JAVA_FULL}  -XshowSettings:properties -version 2>&1| egrep -o -m 1 "java.version = ([0-9]{1,}\.)+[0-9]{1,}")],
        [AC_MSG_ERROR(["bamUtils Path Executable Test - Failed"])])
echo "bamUtils Path Executable Test - Succeeded"
AS_VERSION_COMPARE([BUV], [1.8], [AC_MSG_WARN(["bamUtils Version is Lower Than 1.0.13 (detected version ${BUV})"]],
                   [echo "bamUtils Version Test - Succeeded (detected version ${BUV})"],
                   [echo "bamUtils Version Test - Succeeded (detected version ${BUV})"])
