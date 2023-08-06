import random
import math
import json


def mean(q):
  ret=0.0
  for qq in q:
    ret+=qq
  return ret/len(q)
def std(q,m=None):
  if len(q)<2:return 0.0
  if m is None:m=mean(q)
  ret=0.0
  for qq in q:
    ret+=(qq-m)**2
  ret/=len(q)-1
  return math.sqrt(ret)
def argmax(q):
  if len(q)==0:return -1
  maxi=0
  maxv=q[0]
  for i in range(1,len(q)):
    if q[i]>maxv:
      maxv=q[i]
      maxi=i
  return maxi
def max(q):
  if len(q)==0:return -1
  maxv=q[0]
  for i in range(1,len(q)):
    if q[i]>maxv:
      maxv=q[i]
  return maxv

def argmin(q):
  if len(q)==0:return -1
  mini=0
  minv=q[0]
  for i in range(1,len(q)):
    if q[i]<minv:
      minv=q[i]
      mini=i
  return mini
def min(q):
  if len(q)==0:return -1
  minv=q[0]
  for i in range(1,len(q)):
    if q[i]<minv:
      minv=q[i]
  return minv

def statinf(q):
  ret={}
  if hasattr(q,"shape"):
    s=getattr(q,"shape")
    if callable(s):
      s=s()
    ret["shape"]=s
  if hasattr(q,"__len__"):
    l=getattr(q,"__len__")
    if callable(l):
      l=l()
    ret["len"]=l
  ret["mean"]=mean(q)
  ret["std"]=std(q)
  ret["argmax"]=argmax(q)
  ret["max"]=q[ret["argmax"]]
  ret["argmin"]=argmin(q)
  ret["min"]=q[ret["argmin"]]
  return ret

def sstr(q):
  return json.dumps(statinf(q),indent=2)
def sprint(q):
  print(sstr(q))



