import glob
import xlwt

f = xlwt.Workbook()
sheet1 = f.add_sheet('Hostname',cell_overwrite_ok=True)
sheet1.write(0,0,"Host")

i = 1
for file in glob.glob('*.html'):
	file=file.replace(".html","")
	sheet1.write(i,0,file)
	i = i+1

f.save('hosts.xls')