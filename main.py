from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Item(BaseModel):
    name:str
    is_found:bool =False


app = FastAPI()

#we are going to use a list to store lost items
lost_items = []

#used to post items that are lost
@app.post('/items')
def item_lost(item:Item):
    lost_items.append(item)
    return item

@app.get('/items')
def item_list():
    return lost_items[0:len(lost_items)]

@app.get('/items/{item_id}')
def get_item(item_id:int):
    if(item_id < len(lost_items)):
        return lost_items[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not in Lost and Found")

@app.delete('/items')
def item_found(item:Item):
    index = -1
    for _ in range(len(lost_items)):
        if item==lost_items[_]:
            index = _
            break
    if index == -1:
        return 'Item not in Lost and Found'
    popped = lost_items[index]
    lost_items.pop(index)
    return popped