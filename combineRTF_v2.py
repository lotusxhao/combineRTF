#!/usr/bin/env python
# -*- coding: utf-8 -*-#
#-------------------------------------------------------------------------------
# Name:        combineRTF
# Purpose:     combine multiple RTF files in a folder into one RTF file
#
# Author:      john-dell
#
# Created:     06/08/2016
# Copyright:   (c) john-dell 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import os
import sys
import codecs
import glob
import tempfile
import time
import re
import datetime
import logging
import pandas as pd

class combineRTF(object):
    """
    combine multiple RTF files in a folder into one RTF file
    """

    def __init__(self):
        self.pathin = " "
        self.pathout = " "
        self.pagestr = "{\\field{\\*\\fldinst { PAGE }}}{ of }{\\field{\\*\\fldinst { NUMPAGES }}}"
        self.rtffilepattern = "t_*.rtf"
        self.fileout = "combined.rtf"
        self.filelist = []
        self.totalfiles = 0
        self.file_pages = {}

    def replacePageXofY(self, pathin, filein, pathout):
        """
        update the pagexofy into real string instead of RTF tag
        remove the bookmark level 2 and 3, only keep the first occurence of
            bookmark for one RTF file

        Args:
            pathin (str): The path for the input RTF file.
            filein (str): The file name for the input RTF file.
            pathout (str): The path for the output RTF file.
        Returns:
            NA
        Raises:
            NA

        """

        f = codecs.open(pathin + filein, 'r', encoding='utf-8')
        fout = codecs.open(pathout + filein, 'w', encoding='utf-8')

        totalpage = 0

        writetofile = False

        myre = re.compile(r"{(.*)}") #r"\\pard}}{\\upr{\\bkmkstart IDX1}{\\ud{\\bkmkstart IDX1}}}{\\bkmkend IDX1}\\trowd\\trkeep\\trhdr\\trqc"

        for aline in f.readlines():
            if aline.find("{ NUMPAGES }") > -1:
                totalpage = totalpage + 1

        self.file_pages[filein] = totalpage

        currentpage = 0
        f.seek(0, 0)

        currentbookmark = 0

        for aline in f.readlines():
            if aline.find("{ NUMPAGES }") > -1:
                currentpage = currentpage + 1
                pagenumber = "%s of %s" % (currentpage, totalpage)

                newline = aline.replace(self.pagestr, pagenumber)

                fout.write(newline)

            elif aline.find("\\bkmkend") > -1:
                #only keep the first occurence of bookmark
                currentbookmark += 1

                if currentbookmark > 1:
                    if myre.search(aline):
                        #print myre.search(aline).group()
                        newline = myre.sub(" ",aline)
                        #print newline
                        #fout.write("\\pard}}\\trowd\\trkeep\\trhdr\\trqc")
                        fout.write(newline)
                        fout.write("\n")
                    else:
                        fout.write("\n")
                else:
                    fout.write(aline)

            elif aline.find("\\tcl2") > -1:
                #remove level 2 bookmark
                fout.write("\n")

            elif aline.find("\\tcl3") > -1:
                #remove level 3 bookmark
                fout.write("\n")

            else:
                fout.write(aline)

        fout.flush()
        fout.close()

        f.close()
        print "Replacing Page numbers done"

    def remove_head(self, path, file):
        """
        remove the header of RTF file

        Args:
            path (str): The path for the input RTF file.
            file (str): The file name for the input RTF file.
        Returns:
            filestream object: Returns the processed RTF file stream.
        Raises:
            NA

        """

        tfile = codecs.open(path + file,'r',encoding='utf-8')

        temp = tempfile.TemporaryFile()

        writeyesno = False

        for line in tfile.readlines():
            if line.find("\\sectd") > -1:
                writeyesno = True

            if writeyesno:
                temp.write(line)

        print "removing head"
        temp.seek(0,0)
        tfile.close()
        return temp

    def remove_tail(self, path, file):
        """
        remove the tail of RTF file, the last row

        Args:
            path (str): The path for the input RTF file.
            file (str): The file name for the input RTF file.
        Returns:
            filestream object: Returns the processed RTF file stream.
        Raises:
            NA

        """

        tfile = codecs.open(path + file,'r',encoding='utf-8')
        total_lines = 0

        for line in tfile.readlines():
            total_lines += 1

        tfile.seek(0, 0)

        temp = tempfile.TemporaryFile()

        new_total_lines = 0
        for line in tfile.readlines():
            new_total_lines += 1
            if new_total_lines < total_lines:
                temp.write(line)
            elif new_total_lines == total_lines:
                if line.find("\\pard}\\par}}") > -1:
                    temp.write("}}\n")
                elif line.find("{\\par}}") > -1:
                    temp.write(line[0:-3])
                elif line.find("\\pard}") > -1:
                    temp.write("\n")
                elif line.find("}\par}}") > -1:
                    temp.write("}\par}\n")

        print "removing tail"
        temp.seek(0,0)
        tfile.close()
        return temp


    def remove_head_tail(self, path, file):
        """
        remove the header and the tail (the last row) of RTF file

        Args:
            path (str): The path for the input RTF file.
            file (str): The file name for the input RTF file.
        Returns:
            filestream object: Returns the processed RTF file stream.
        Raises:
            NA

        """

        tfile = codecs.open(path + file,'r',encoding='utf-8')
        total_lines = 0

        for line in tfile.readlines():
            total_lines += 1

        tfile.seek(0, 0)

        temp = tempfile.TemporaryFile()

        writeyesno = False
        new_total_lines = 0
        for line in tfile.readlines():
            new_total_lines += 1

            if line.find("\\sectd") > -1:
                writeyesno = True

            if writeyesno and new_total_lines < total_lines:
                temp.write(line)

            elif writeyesno and new_total_lines == total_lines:
                if line.find("\\pard}\\par}}") > -1:
                    temp.write("}}\n")
                elif line.find("{\\par}}") > -1:
                    temp.write(line[0:-3])
                elif line.find("\\pard}") > -1:
                    temp.write("\n")

        print "removing head and tail"
        temp.seek(0,0)
        tfile.close()
        return temp

    def getfilelist(self):
        "get file lists from pathin "

        self.filelist = glob.glob(self.pathin + self.rtffilepattern)
        self.totalfiles = len(self.filelist)

        return True


    def combineRTF(self):
        """
        combine multiple RTF files in a folder into one RTF file
        """

        starttime = time.clock()

        if self.totalfiles == 0:
            print "WARNING: There is no RTF files to combine. Please re-check!"
            return False

        combined_file = codecs.open(self.pathout + self.fileout,'w', encoding='utf-8')

        total_files = self.totalfiles

        for file in self.filelist:
            print "processing file (pagexofy) " + file
            filepath, filename = file.split("\\")
            self.replacePageXofY(self.pathin,filename,self.pathout)

        current_file = 0

        for file in self.filelist:
            print "processing file (combining) " + file
            current_file = current_file + 1
            filepath, filename = file.split("\\")

            if current_file == 1:
                tmpfile = self.remove_tail(self.pathout, filename)
            elif current_file == total_files:
                tmpfile = self.remove_head(self.pathout, filename)
            else:
                tmpfile = self.remove_head_tail(self.pathout, filename)

            combined_file.write(tmpfile.read())
            tmpfile.close()

            # remove current file
            os.remove(os.path.join(self.pathout, filename))

            if current_file < total_files:
                combined_file.write("\\pard\\sect")

        combined_file.flush()
        combined_file.close()

        print "Combine RTF files finished: %s " % self.fileout

        endtime = time.clock()
        print "Elapsed time: %s" % (endtime-starttime)

    def genPDFtkBookmark(self,pageoffset=1,titledescription={},fileout="mybookmark_pdftk.txt"):
        """
        create bookmark in PDFtk format

        Args:
            pageoffset (int): The page offset for the PDF file. Usually the page
                number for the first page of the first report.
            titledescription (dict): The dictionary for the table title. The key
                should be RTF file names, and the value should be the title of
                those RTF reports.
            fileout (str): The file name for the output bookmark file.
        Returns:
            NA
        Raises:
            NA

        """

        if self.totalfiles == 0:
            print "WARNING: There is no RTF files to combine. Please re-check!"
            return False

        page_accumulate = 0

        if pageoffset:
            page_accumulate += pageoffset

        fbookmark = codecs.open(self.pathout + fileout, 'w', 'utf-8')

        fbookmark.write('BookmarkBegin\n')
        fbookmark.write('BookmarkTitle: Table of Contents \n')
        fbookmark.write('BookmarkLevel: 1\n')
        fbookmark.write('BookmarkPageNumber: 1 \n')

        if len(titledescription) == 0:
            for ktfile,vtfile in enumerate(self.filelist):
                ff = vtfile.split('\\')[1]

                fbookmark.write('BookmarkBegin\n')
                fbookmark.write('BookmarkTitle: %s \n' % ff)
                fbookmark.write('BookmarkLevel: 2\n')
                fbookmark.write('BookmarkPageNumber: %s \n' % page_accumulate)

                page_accumulate += self.file_pages[ff]
                self.file_pages[ff] = page_accumulate

        else:
            for ktfile,vtfile in enumerate(self.filelist):
                ff = vtfile.split('\\')[1]
                if ff in self.file_pages and ff.split('.')[0] in titledescription:

                    fbookmark.write('BookmarkBegin\n')
                    fbookmark.write('BookmarkTitle: %s \n' % titledescription[ff.split('.')[0]].encode('ascii','xmlcharrefreplace'))
                    fbookmark.write('BookmarkLevel: 2\n')
                    fbookmark.write('BookmarkPageNumber: %s \n' % page_accumulate)

                    page_accumulate += self.file_pages[ff]
                    self.file_pages[vtfile.split('\\')[1]] = page_accumulate

        fbookmark.write('\n')
        fbookmark.close()

        print "PDFtk bookmark file %s is created! " % fileout

if __name__ == '__main__':

    comb = combineRTF()

    td = datetime.date.today()
    tddtc = datetime.date.isoformat(td)
    comb.pathin = "C:/TEMP/"
    comb.pathout = "C:/TEMP/Combined/"

    comb.rtffilepattern = "class_*.rtf"
    comb.fileout = "combined_tables_%s.rtf" % tddtc

    comb.getfilelist()
    ttfiles = comb.filelist

    print "original ======================="
    for ktfile,vtfile in enumerate(ttfiles):
        print ktfile,vtfile

    ttfiles.sort(key=lambda x:(int(x.split('\\class_')[1][0:-4])))
    comb.filelist = ttfiles

    print "sorted ======================="
    for ktfile,vtfile in enumerate(ttfiles):
        print ktfile,vtfile

    comb.combineRTF()

    toc = pd.read_excel("c:/temp/tocfile.xlsx",sheetname="Sheet1")
##    print toc[toc['filename'] == "class_3"]['titledescription'].values[0]
##    titledesc = toc[toc['filename'] == "class_3"]['titledescription'].values[0].encode('ascii','xmlcharrefreplace')
    tdesc = dict([(f,desc) for f, desc in zip(toc.filename, toc.titledescription)])
    comb.genPDFtkBookmark(pageoffset=5,titledescription=tdesc)

    ## 中文书签支持
    ## https://www.pdflabs.com/blog/export-and-import-pdf-bookmarks/
    ## http://stackoverflow.com/questions/24646723/convert-chinese-characters-into-xml-html-style-numerical-entities-and-into-unico
##    text = u"中文支持如何"
##    ee = text.encode('ascii','xmlcharrefreplace')


