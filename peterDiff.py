import difflib
from datetime import datetime

def main():
    diff_files("file1.txt", "file2.txt", context=False, report_name="peter_Test.html")
    #diff_files("500k_test1.csv", "500k_test2.csv", context=False, report_name="peter_Test.html")

#this function will make the file diff and pass data to be written to report
def diff_files(file1, file2, context=False, report_name="diff_report.html"):
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
/*pre{white-space: pre-wrap;}*/
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

#coloring the changed words in lines
def color_words(diff):
    # print(diff)
    for i in range(len(diff)):
        if diff[i][0] == '?':
            diff[i-1] = str(diff[i-1] + "\n<span class='word'><strong>" + diff[i]) + "</strong></span>"
    for i in diff:
        if i[0] == "?":
            diff.remove(i)
    if len(diff) < 2:
        diff.append(diff[0])
    # print(diff)
    return diff

def complete_html_format(report_name):
    with open(report_name, "a") as report:
        report.write("</table></body>")


if __name__=="__main__":
    main()
