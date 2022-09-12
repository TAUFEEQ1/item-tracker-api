import json
from app import logdb
from typing import List,Any

def getAll(txn,key:bytes)->List[Any]:
    tmp = txn.get(key.encode(),default='b[]')
    return json.loads(tmp)

def saveAll(txn,key:bytes,items:List[Any]):
    serialized = json.dumps(items)
    txn.put(key,serialized.encode())

def recordProductMissing(code:str):
    # recorded for foreinsics
    # blacklist code 
    index = b"missing:products"
    txn = logdb.begin(write=True) 
    missing = getAll(txn,index)
    missing.append(code)
    saveAll(txn,index,missing)


def recordDuplicateProduct(code:str,product:str):
    index = b"duplicate:products"
    txn = logdb.begin(write=True)
    duplicates = getAll(txn,index)
    duplicates.append({"code":code,"product":product})
    saveAll(txn,index,duplicates)

def recordProductViolation(code:str,user_id:str):
    index = b"product:violations"
    txn = logdb.begin(write=True)
    violations = getAll(txn,index)
    violations.append({"code":code,"user_id":user_id})
    saveAll(violations)


    

