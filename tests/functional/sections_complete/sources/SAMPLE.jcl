//SAMPJCL JOB 1,CLASS=6,MSGCLASS=0,NOTIFY=&SYSUID
//*
//STEP010  EXEC PGM=SORT
//SORTIN   DD DSN=JCL.SAMPLE.INPUT,DISP=SHR
//SORTOUT  DD DSN=JCL.SAMPLE.OUTPUT,
//         DISP=(NEW,CATLG,CATLG),DATACLAS=DSIZE50
//SYSOUT   DD SYSOUT=*
//SYSUDUMP DD SYSOUT=C
//SYSPRINT DD SYSOUT=*
//SYSIN    DD *
  SORT FIELDS=COPY
  INCLUDE COND=(28,3,CH,EQ,C'XXX')
/*                      