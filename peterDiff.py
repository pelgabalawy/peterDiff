import difflib
from datetime import datetime

#----------------------------------------------------------------------------------------------
##sample run from command line:
#-----------------------------
#peterDiff(<file1> <file2> <context=True/False> <report_name=report.html> <logging=True/False>)
#----------------------------------------------------------------------------------------------
##Details:
#--------
#-file1: the first file to be compared
#-file2: the second file to be compared
#-context: True: Thre report will contains the similarites as well as the differences
#         False(Default): The report will contain the differences only
#-report_name: The name of the final html report
#            Default: diff_report.html
#-logging: True: every line being compared will be logging a line in the shell while the script is executing
#         False: No logging will be showing in the shell while the script is executing
#----------------------------------------------------------------------------------------------
#This main function is for testing for now, until I make this project a command line tool
def main():
    diff_files("500k_test1.csv", "500k_test2.csv", context=True, report_name="peter_Test.html", logging=True)
    #diff_files("500k_test1.csv", "500k_test2.csv", context=False, report_name="peter_Test.html")

#Choosing what function to use in the diff
def choose_diff_method(file1, file2, context=False, report_name="diff_report.html", logging=False):
        file1_l = len(open(file1).readlines())
        file2_l = len(open(file2).readlines())
        if (file1_l == file2_l):
            diff_files(file1, file2, context=context, report_name=report_name, logging=logging)
        else:
            detailed_comparison(file1, file2, context=context, report_name=report_name, logging=logging)

#this function will make the file diff and pass data to be written to report
def diff_files(file1, file2, context=False, report_name="diff_report.html", logging=False):
    #the count starts at 1
    count = 1
    #setup the report file to start the diff
    setup_report(report_name, file1, file2)
    #open both files to start the diff
    with open(file1, "r") as f1, open(file2, "r") as f2:
        for line1, line2 in zip(f1,f2):
            status = ""
            diff = list(difflib.ndiff([line1], [line2]))
            #the line is completely changed
            if len(diff) == 2:
                status = "!="
            elif len(diff) == 4:
                status = "!="
            elif len(diff) == 3:
                status = "!="
            elif len(diff) == 1:
                status = "=="
            if logging:
                print("Line Number: " + str(count) + " is done!")
            diff = color_words(diff)
            write_line_diff(report_name, count, diff[0], diff[1], status, context=context)
            count = count + 1
    complete_html_format(report_name)

#Used to set up the report to start adding the diff
def setup_report(report_name, file1, file2):
    report_temp = '''<!DOCTYPE html>
<html><head><style>
table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}
td, th {border: 2px groove white;text-align: left;border-radius: 5px;}th {padding: 4px;}td {padding: 0px;}
body{background-color: #E6E6E6; white-space: pre;}
pre{white-space: pre-wrap;}
.red{background-color: #ffb3b3;}.green{background-color: #90EE90;}
.word{color: red;}.center{text-align: center;}.red-text {color: red;}
</style></head><body>
<p><strong>Report Name: </strong>'''+ report_name +'''<p>
<p><strong>Timestamp: </strong>'''+ str(datetime.now()) +'''<p>
<table>
  <tr>
    <th class="center">lines</th>
    <th class="center">'''+ file1+ '''</th>
    <th class="center">Status</th>
    <th class="center">'''+ file2 +'''</th>
  </tr>'''
    with open(report_name, "w") as report:
     report.write(report_temp)

#IT's only used to write the diff line by line until the end
def write_line_diff(report_name, count, line1, line2, status, context=True):
    color = ""
    if status != "==":
        color = "red"
    else:
        color = "green"
    lines_temp = '''<tr>
        <td class="center">'''+ str(count) +''' </td>
        <td class='''+ color +'''><pre>'''+ str(line1) +'''</pre></td>
        <td class="center '''+ color +'''">'''+ str(status) +'''</td>
        <td class='''+ color +'''><pre>'''+ str(line2) +'''</pre></td>
    </tr>'''
    if context == False and status == "==":
        pass
    else:
        with open(report_name, "a") as report:
            report.write(lines_temp)


# #coloring the changed words in lines
def color_words(diff):
    if len(diff) == 2:
        for i in range(len(diff)):
            diff[i] = "<span class='word'>" + diff[i] + "</span>"
    elif len(diff) > 2:
        #loop tru the list of lines diffed using the difflib
        for line in range(len(diff)):
            index = []
            #if the line starts with ? means it's the results of the diff
            if diff[line][0] == '?':
                str = list(diff[line])
                #find all the indexes that got changed and store them in the index array
                for k in range(len(str)):
                    if str[k] == '^' or str[k] == '+' or str[k] == '-':
                        index.append(k)
                #split the line before the diff line means it's the line that got the change
                line_to_color = list(diff[line-1])
                #color the text that was found in the index array
                for l in index:
                    line_to_color[l] = "<span class='word'>" + line_to_color[l] + "</span>"
                diff[line-1] = "".join(line_to_color)
    #just in case clean up the diff array of any diff results lines if there is any
    for i in diff:
        if i[0] == "?":
            diff.remove(i)
    #if the lilne has no change, we will end up with one line, so it will be duplicated here to be returned
    #and later on, it will be writed to the report
    if len(diff) < 2:
        diff.append(diff[0])
    return diff


def complete_html_format(report_name):
    with open(report_name, "a") as report:
        report.write("</table></body>")

#---------------------------------------------------------------------------------------------------------------
def detailed_comparison(file1, file2, context=False, report_name="diff_report.html", logging=False):
    print("this function will take longer in execution but it will be a very detailed comparison")


if __name__=="__main__":
    main()
