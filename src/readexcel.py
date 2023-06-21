import xlrd
import random
loc = ("Questions.xls")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
print(sheet.nrows)
rows=sheet.nrows
emotion="Angry"
que=[]
cat=[]
indices=[]
for i in range(1,rows):
    que.append(sheet.cell_value(i, 0))
    cat.append(sheet.cell_value(i, 1))
ind=0
for x in cat:
    if(x==emotion):
        indices.append(ind)
    ind=ind+1
    print(x)
print(indices)
ele=random.choice(indices)
askque=que[ele]
print(askque)
