# simplestat
Very minimal statistics module. Useful when you dont have the disk space for numpy

Only contains the following functions (and only for 1d arrays):
mean(q)
std(q,m=None)#can set m=mean(q) to save computation time
min(q)
argmin(q)
max(q)
argmax(q)
statinf(q)
  return information about the object as dictionary
sstr(q)
  statinf+json.dumps(indent=2)
sprint(q)
  print(sstr())