# main.py がルートディレクトリにある場合

uvicorn main:app --reload --host 0.0.0.0 --port 8000

# main.py がルートディレクトリにない場合

uvicorn \*.main:app --reload --host 0.0.0.0 --port 8000

# example

from fastapi import FastAPI # ①

    app = FastAPI() # ②

    @app.get("/") # ③
        def read_root(): # ④
            return {"message": "Hello World"} # ⑤

① 必要なパッケージをインポート
② FastAPI インスタンスを生成
③ Path Operation Decorator で操作、パスを指定

# API ドキュメントを参照する

http://127.0.0.1:8000/docs
