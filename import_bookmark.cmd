set startTime=%time%
pdftk combined_tables_2016-11-13.pdf update_info mybookmark_pdftk.txt output combined_tables_2016-11-13_bookmarked.pdf
echo Start Time: %startTime%
echo Finish Time: %time%

timeout 30

