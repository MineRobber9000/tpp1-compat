import csv,os

table_lines = []

with open("results.csv") as f:
	r = csv.reader(f)
	for l in r:
		table_lines.append([l[0],l[1],l[2]])

notes = dict()
files = os.listdir("notes")
for file in files:
	with open(os.path.join("notes",file)) as f:
		notes[file]=f.read()

if ".gitkeep" in notes:
	del notes[".gitkeep"]

table_lines[0] = ["Emulator","Did it load?","Error Count"]

html = """<html>
<head>
<title>TPP1 Compatibility Tracker</title>
<style>
body {
	background-color: #e0b0ff;
}
td.failure {
	background-color: #fd0000;
}
td.success {
	background-color: #00fd00;
}
table {
	width: 100%;
	border-collapse: collapse;
}
table,th,td {
	border: 1px solid black;
}
hr {
	background-color: black;
	color: black;
}
</style>
</head>
<body>
<h1>TPP Compatibility Tracker</h1>
<em>Expect a lot of failures, this is still pretty new</em>
<table>
"""
first = True
for line in table_lines:
	html+="\t<tr>\n"
	if first:
		html+="\t\t<th>{}</th>\n\t\t<th>{}</th>\n\t\t<th>{}</th>\n".format(*line)
		first=False
	else:
		emu_name = line[0]
		if notes.get(emu_name,False):
			emu_name+="*"
		t = list(line[1])
		t[0]=t[0].upper()
		t = "".join(t)
		if eval(t):
			cls="success"
		else:
			cls="failure"
		html+="\t\t<td>{}</td>\n\t\t<td class=\"{}\">{}</td>\n\t\t<td>{}</td>\n".format(emu_name,cls,line[1],line[2])
	html+="\t</tr>\n"
html+="""</table>
<hr noshade>
"""
if len(notes.keys())>0:
	for k in notes:
		html+="<h2>Notes for {}</h2>\n<p>{}</p>\n<hr noshade>\n".format(k,notes[k])
html+="""<p>Reminder that, since TPP1 is relatively new still, not many emulators will support it.</p>
<p><a href="https://github.com/MineRobber9000/tpp1-compat">Give me more emulators that crash!</a></p>
</body>
</html>"""
with open("index.html","w") as f:
	f.write(html)
