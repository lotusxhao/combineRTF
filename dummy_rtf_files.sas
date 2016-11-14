
proc sort data=sashelp.class out=class;
    by name;
run;

data class;
    set class;
    pagenumber = floor(_n_/10);
run;

proc sort data=class;
    by pagenumber;
run;


proc template;
   define style Styles.MyStyle;
   parent=styles.rtf;
   style usertext from usertext /
      foreground=white
      background=white;
   end;
run;


%macro dummy_report;

ods noresults;
options topmargin=1in bottommargin=1in leftmargin=1in rightmargin=1in orientation=landscape nodate nonumber label papersize=A4;
ods escapechar="~";
title;
footnote;
ods document name=hello;

%do i=1 %to 200;

    %if "&i" = "1" %then %do;
    ods rtf file="c:\temp\class_&i..rtf" style=styles.MyStyle bookmark="table_idx_&i._"  toc_data bodytitle;
    %end;
    %else %do;
    ods rtf file="c:\temp\class_&i..rtf" style=styles.MyStyle bookmark="table_idx_&i._"  toc_data bodytitle;
    %end;

    title1 "test &i title in test RTF";
    title2 "Page ~{pageof}";
    footnote "footnote in test RTF";

    ods proclabel = "test &i title in test RTF";

    proc report data=class nowindows 
            style(report)={width=100% asis=yes rules=groups frame=hsides borderwidth=3 bordercolor=black borderstyle=solid}
            style(header)={backgroundcolor=white bordertopwidth=3 bordertopcolor=black bordertopstyle=solid
                            borderbottomwidth=1 borderbottomcolor=black borderbottomstyle=solid}
            contents=""
            ;
        define pagenumber /group order noprint contents="";
        break after pagenumber/page contents="";
    run;

    ods rtf close;
    ods pdf close;
    title;
    footnote;
%end;

ods document close;

%mend dummy_report;

%dummy_report;

