import subprocess


class CobCompiler:
    def __init__(self):
        self.return_code = 0
        self.command = ""
        self.opt_string = ""
        

    def ofcbpp(self):
        """
        OpenFrame COBOL Preprocessor 4
        Usage : ofcbpp -i file_name [options]
        Options:
        -o <filename>                 : Specify output file name
        -copypath <path>              : Add single copybook path to find the copybook
        --add-miss-period             : Add missing section/paragraph end period
        --collating-seq-ebcdic        : Set collating sequence to EBCDIC
        --conv-stop-run               : Convert Stop Statement to Goback Statement
        --enable-osvs                 : Enable OSVS Cobol features
        --enable-rw                   : Enable IBM REPORT WRITER features
        --enable-include              : Expand the 'EXEC SQL INCLUDE' Statement.
        --enable-declare              : Expand the 'EXEC SQL INCLUDE' Statement and Insert 'EXEC SQL DECLARE' before/after DataItem which is used by EXEC SQL statement in DATA DIVISION
        """
        pass

    def tbpcb(self):
        """
        Usage: tbpcb [-h] [-v] [options] file...

        -h   show this help.
        -v   show tbESQL version.

        Option Name         Default   Description
        --------------------------------------------------------------------------------
        CLOSE_ON_COMMIT     NO        Close all cursors on COMMIT
        CODE                COBOL     The user language type
        COLUMNS             72        valid column range
        COMP5               YES       Convert from COMP type to COMP-5 type
        CONFIG              default   The name of user configuration file
        DB2_SYNTAX          NO        Support DB2 array select/insert syntax only
        DYNAMIC             TIBERO    Tibero or ANSI, Oracle Dyn-SQL Semantics
        END_OF_FETCH        1403      End of FETCH SQLCODE value { 1403 | 100 }
        ERROR_CODE          DEFAULT   The error code to DEFAULT or TIBERO
        HOLD_CURSOR         NO        Control holding of cursors after closing
        IGNORE_ERROR        NO        Ignore the semantic check error.
        INAME               N/A       The name of the input file
        INCLUDE             N/A       Directory paths for included files
        INSERT_NO_DATA_ERRORNO        it returns 1403 as error code when data is not fou
        LOG_LVL             NONE      whether to make log file for debugging
        MODE                TIBERO    Code conformance to Tibero or ANSI, Oracle
        ONAME               N/A       The name of the output file
        ORACA               NO        Whether to use the oraca sturucture
        PIC9_WITH_SIGN      YES       If yes, PIC 9 type includes a sign
        PICX                CHARF     Mapping of character arrays and strings
        PREFETCH            1         Number of rows pre-fetched at cursor OPEN time
        RELEASE_CURSOR      NO        Control release of cursors after closing
        RESERVED_WORD_COL   YES       Whether the 'COL' is a reserved word
        RESERVED_WORD_CURSORYES       Whether the 'CURSOR' is a reserved word
        RUNTIME_MODE        TIBERO    TIBERO, ODBC or ORACLE to use for esql runtime
        SELECT_ERROR        YES       Control flagging of select errors
        SQLCHECK            SYNTAX    Amount of compile-time SQL checking
        STMT_CACHE          0         Size of the statement cache
        SYS_INCLUDE         N/A       Directory paths for system header files
        THREADS             NO        Indicates multi-threads application
        TYPE_CODE           TIBERO    Tibero or ANSI, Oracle type codes for Dyn-SQL
        UNSAFE_NULL         NO        prevent 1405 error when indicator is not specified
        USERID              N/A       Specifies Tibero username and password
        VARCHAR             NO        Accept user defined VARCHAR
        VARCHAR_SIZE        NO        Aligns the data for varchar structures
        WORDSIZE            64        Wordsize of platform generated source will be used
        VARCHAR_TEXT        NO        Translates VARCHAR into LEN and TEXT (default). If
        DECLARE_SECTION     NO        Only consider variables inside the DECLARE SECTION
        """
        pass

    def osccblpp(self):
        """
        osccblpp version 7.0.3(14) obuild@tplinux64:ofsrc7/osc(#1) 2018-09-19 21:03:58
        OpenFrame OSC EXEC CICS Interface Preprocessor
        Usage: osccblpp [-c] [-nl] [-n] [-V] [-p <prefix>] <file> ...
            | osccblpp [-c] [-nl] [-n] [-V] [-p <prefix>] [-o <output>] <file>
            | osccblpp [-h | -v]
        <file>  Specify file name to preprocess
        Options:
        -c          Preprocess without DFHCOMMAREA insertion at LINKAGE SECTION
        -n          Preprocess without EXEC CICS Interface translation
        -nl         Preprocess without DFHCOMMAREA DFHEIBLK modification at
                    LINKAGE SECTION and PROCEDURE DIVISION
        -o <output> Set <output> as output file name (stronger than -p)
        -p <prefix> Set <prefix> as output file prefix
        -V          Preprocess in verbose mode
        -h          Display this information
        -v          Display version information
        """
        pass

    def db2prep(self):
        pass

    def db2bind(self):
        pass

    def ofcob(self):
        """
        OpenFrame COBOL Compiler 4
        Usage : ofcob [options] file_name
        Options:
        -o <filename>         : Specify output file name
        -U                    : Make output file as shared object file
        -l<library>           : Search the library file when linking
        -L<dir>               : Add directory to be searched for -l
        -g                    : Compile debugging mode
        --version             : Display compiler version information
        --save-temps          : Save intermediate files
        --time-stamp          : Display current time
        --license             : Display license infomation
        --trace               : Allow READY/RESET TRACE statement
        --notrunc             : Do not truncate exceed digit when USAGE is COMP,COMP-4, or BINARY
        --force-trace         : Apply READY TRACE statement with the beginning of the program
        --enable-debug        : Enable debugging message
        --enable-ofasm        : Enable OFASM features
        --enable-osvs         : Enable OSVS Cobol features
        --enable-rw           : Enable Report Writer features
        --enable-cbltdli      : Add a parameter-counting parameter in every CBLTDLI call
        --enable-aertdli      : Add a parameter-counting parameter in every AERTDLI call
        --enable-asa-byte     : Insert control character at the start of each line in a print file.
        --enable-caf <funcname>       : Call <funcname> with the beginning of the progame
        --check-file-id       : Check when the file name is distinguished from PROGRAM ID
        --check-invalid-data  : Check when move statement's source is invalid data
        --check-index         : Check when the ouccurs's index over than max / min
        --init-space          : Initialize space variable initial value
        --DIR <filename>      : Get the OFCOBOL option from specified file name
        --cpm-name <filename> : Set cpm name
        --ptr-redef           : Modify redefine subject item if redefine object has USAGE POINTER
        """
        pass