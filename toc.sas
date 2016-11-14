

ods escapechar = '~';
ods _all_ close;
ods noresults;
ods rtf file="c:\temp\class_0.rtf" style=styles.rtf bodytitle;

title;
footnote;

ods text="~S={outputwidth=80% just=left fontsize=12pt}DELIVERY TITLE: POST-HOC BATCH 2";
ods text="~S={outputwidth=80% just=left fontsize=12pt}DELIVERY DATE: %sysfunc(today(), yymmdd10. )";
ods text=" ";
ods text="~S={outputwidth=80% just=center fontsize=12pt}TABLE OF CONTENTS";
ods text="~R/RTF' {\field\fldedit{\*\fldinst {\fs24 TOC \tcf67 \\h }}}'";
ods text=" ";

/*
data _blank;
    length col1 $100;
    col1 = ' ';
run;

proc report data=_blank nowindows
            style(report)={width=100% asis=yes rules=groups frame=hsides borderwidth=0 bordercolor=black borderstyle=solid}
            style(header)={backgroundcolor=white bordertopwidth=0 bordertopcolor=black bordertopstyle=solid
                            borderbottomwidth=0 borderbottomcolor=black borderbottomstyle=solid}
            contents="";
    define col1 /display "COMPANY CONFIDENTIAL" style(column)={backgroundcolor=white fontsize=10pt color=white};
run;
*/

ods rtf close;
ods results;
ods listing;
ods html;


