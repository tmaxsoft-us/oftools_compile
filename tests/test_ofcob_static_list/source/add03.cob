       IDENTIFICATION DIVISION.
       PROGRAM-ID. ADD01.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 ITEM-01 PIC 9999.
       01 ITEM-02 PIC 9999.
       PROCEDURE DIVISION.
       MOVE 1234 TO ITEM-01.
       MOVE 1234 TO ITEM-02.
       ADD ITEM-01 TO ITEM-02.
       DISPLAY ITEM-02.
