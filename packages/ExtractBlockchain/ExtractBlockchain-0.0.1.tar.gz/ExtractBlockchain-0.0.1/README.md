## Readme file 

## blockchain (bl)

```
pip install BlockChainData
import BlockChainData as bd
```

1. mine_block(str)  
```
b=bd.bl.Blockchain()
b.mine_block("hello")
```
2. get_previous_block()
```
b.get_previous_block()
``` 

3. is_chain_valid
```
b.is_chain_valid()
``` 
4. chain
```
b.chain
b.chain[index]["data"]="changed data"

```

## getdata (gd)

1. getd(str) - to get data of any account 
```
import BlockChainData as bd 
bd.gd.getd(a)
here a is address of block
```

## Tools (t)

1. Check_connection()
```
import BlockChainData as bd
bd.t.check_connection()
```
2. create_Acc()
```
bd.t.create_acc()
```
3. check_bal
```
bd.t.check_bal()
```
4. transaction()
```
bd.t.transaction(0,1,5)
```
5. receipt(str)
```
bd.t.receipt("0xe6dd40cdeff86105912b0f79065224c73e5a32d7e625f790effa16419e25e073")
``` 