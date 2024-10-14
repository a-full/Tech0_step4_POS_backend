from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware  # CORS設定用

app = FastAPI()

# CORS設定の追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURLを許可
    allow_credentials=True,
    allow_methods=["*"],  # 全てのHTTPメソッドを許可
    allow_headers=["*"],  # 全てのヘッダーを許可
)

# 仮の商品マスタデータ
product_master = {
    "12345678901": {"name": "おーいお茶", "price": 150},
    "98765432101": {"name": "ソフラン", "price": 300},
}

# 商品検索用のモデル
class ProductRequest(BaseModel):
    code: str

class ProductResponse(BaseModel):
    code: str
    name: str
    price: int

# 購入リクエスト/レスポンス用のモデル
class PurchaseItem(BaseModel):
    code: str
    name: str
    price: int

class PurchaseRequest(BaseModel):
    emp_code: str
    store_code: str
    pos_id: str
    items: List[PurchaseItem]

class PurchaseResponse(BaseModel):
    success: bool
    total_amount: int

@app.post("/product_search", response_model=ProductResponse)
def product_search(request: ProductRequest):
    product = product_master.get(request.code)
    if product:
        return {"code": request.code, "name": product["name"], "price": product["price"]}
    else:
        raise HTTPException(status_code=404, detail="商品がマスタ未登録です")

@app.post("/purchase", response_model=PurchaseResponse)
def purchase(request: PurchaseRequest):
    total_amount = sum(item.price for item in request.items)
    return {"success": True, "total_amount": total_amount}
