#Get Subjects ID from html source code
import re

# Now we have a list to fill, 
# each has this type of url https://unipoll.neptun.elte.hu/Survey.aspx?FillOutId=375042069&displaymode=noframe&lng=en-US
# every subject has similar url except for "375042069", we call this ID of subject
# now we need to find all of them
def getID(fname):
    data = []
    with open(fname, 'r', encoding="utf-8") as fi:
        for line in fi:
            m = re.findall(r'A2.Sel\(\'[0-9]{9}', line)
            if len(m) != 0:
                data.append(str(m)[-2-9:-2])
    # data = list(map(int, data))
    return data

# def getDecision():
    

def test():
    listSubject = getID('ou.ou')
    originalUrl = "https://unipoll.neptun.elte.hu/Survey.aspx?FillOutId=000000000&displaymode=noframe&lng=en-US"
    for subject in listSubject:
        subjectUrl = originalUrl.replace("000000000", subject)
        print(subjectUrl)