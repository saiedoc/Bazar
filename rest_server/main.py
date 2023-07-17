from starlette.responses import RedirectResponse
from StockmarketController import market_controller
import uvicorn
from fastapi import Request
import json

app_controller = market_controller()
app = app_controller.app


@app.post("/sign-up")
async def sign_up(request: Request):
    json_data = await request.json()
    return app_controller.add_account(json_data.get("username"), json_data.get("password"))


@app.post("/login")
async def login(request: Request):
    json_data = await request.json()
    return app_controller.authenticate_account(json_data.get("username"), json_data.get("password"))


@app.post("/logout")
async def logout(request: Request):
    json_data = await request.json()
    username = json_data.get("username")
    password = json_data.get("password")
    username = None
    password = None
    redirect_url = "/login"
    return RedirectResponse(redirect_url)


@app.post("/remove-acc")
async def remove_acc(request: Request):
    json_data = await request.json()
    return app_controller.remove_acc(json_data.get("username"), json_data.get("password"))


@app.post("/pay-in")
async def pay_in(request: Request):
    json_data = await request.json()
    return app_controller.pay_in(json_data.get("user_id"), json_data.get("amount"))


@app.post("/pay-out")
async def pay_out(request: Request):
    json_data = await request.json()
    return app_controller.pay_out(json_data.get("user_id"), json_data.get("amount"))


@app.post("/sell")
async def sell(request: Request):
    json_data = await request.json()
    return app_controller.sell(json_data.get("amount"), json_data.get("item_name"), json_data.get("user_id"))


@app.post("/buy")
async def buy(request: Request):
    json_data = await request.json()
    return app_controller.buy(json_data.get("amount"), json_data.get("item_name"), json_data.get("user_id"))


@app.get("/get-items")
async def get_items(request: Request):
    # json_data = await request.json()
    # print(json_data)
    return app_controller.get_items()


@app.post("/get-user-items")
async def get_user_items(request: Request):
    json_data = await request.json()
    print(json_data)
    return app_controller.get_user_items(json_data.get("user_id"))


@app.post("/get-user")
async def get_user_items(request: Request):
    json_data = await request.json()
    print(json_data)
    return app_controller.get_user(json_data.get("user_id"))


@app.post("/update-prices")
async def update_prices(request: Request):
    return app_controller.update_price()


uvicorn.run(app_controller.app, host="localhost", port=8000)
