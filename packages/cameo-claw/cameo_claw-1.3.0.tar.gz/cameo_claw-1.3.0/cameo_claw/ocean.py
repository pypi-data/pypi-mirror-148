from time import strftime
import msgpack
from starlette.requests import Request
from cameo_claw import mkdir
from cameo_claw.cameo_claw_reuse import fastapi_app
from fastapi.staticfiles import StaticFiles
import json

app = fastapi_app()

# .msgpack path and filename like:
# http://localhost:8000/data/log_msg/2022-04-30/2022-04-30_11_09.msgpack
app.mount("/data", StaticFiles(directory="data"))


# one json iot request size 757 bytes
# fastapi 3304 r/s, actix 22976 r/s 差異7倍速度
# fastapi 2.385 MB/s, actix 16.587 MB/s
@app.post("/api/log_msgpack/")
async def log_msgpack(request: Request):
    directory = f'data/log_msgpack/{strftime("%Y-%m-%d")}/'
    mkdir(directory)
    with open(f'{directory}{strftime("%Y-%m-%d_%H_%M")}.msgpack', 'ab') as f:
        f.write(msgpack.packb(
            {'headers': request.headers.items(),
             'body': json.loads(await request.body())}))
