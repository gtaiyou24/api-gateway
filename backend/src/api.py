import os
from dataclasses import dataclass

from fastapi import FastAPI, Request, Response, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from common.exception import ErrorCode
from common.port.adapter.resource.error import ErrorJson


app = FastAPI(
    title="API Gateway",
    responses={
        422: {
            "model": ErrorJson,
            "description": "Unprocessable Entity",
            "content": {
                "application/json": {
                    "example": {
                        "type": "COMMON_2003",
                        "title": "無効なデータです",
                        "status": 422,
                        "instance": "https://localhost:8000/auth/token"
                    }
                }
            }
        }
    },
    root_path=os.getenv("OPENAPI_PREFIX"),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# app.add_middleware(HTTPSRedirectMiddleware)  # HTTPS を強制
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "example.com", "*.example.com"])  # ホストヘッダーを指定
# app.add_middleware(MonitoringMiddleware)  # エラー/ログ監視のためのモニタリングを実行
# app.add_middleware(PublishInternalTokenMiddleware)  # 内部通信用トークンを発行


@dataclass(frozen=True, eq=True)
class GetCurrentTenant:
    http_bearer = HTTPBearer(auto_error=False)

    async def __call__(self, request: Request) -> str | None:
        authorization: HTTPAuthorizationCredentials | None = await self.http_bearer(request)
        if authorization is None:
            return None

        tenants = {
            "api-key-1": "WEGO",
            "api-key-2": "UNIQLO",
        }
        return tenants.get(authorization.credentials, None)


@app.get('/path/to/vertex')
async def recommend(tenant: str | None = Depends(GetCurrentTenant())):
    """Vertex AI にリクエストを送信する"""
    # TODO: tenant が None なら未認証のリクエストとして403を返却しても良いし、別の処理を行なっても良いし、GetCurrentTenantクラス内で例外を送出してもよい
    # response = requests.post('https://vertexai.com/hogehoge')
    pass


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, error: ValueError) -> Response:
    print(error)
    return JSONResponse(
        status_code=ErrorCode.COMMON_2002.http_status,
        content=jsonable_encoder({
            "type": ErrorCode.COMMON_2002.name,
            "title": ErrorCode.COMMON_2002.message,
            "status": ErrorCode.COMMON_2002.http_status,
            "instance": str(request.url)
        })
    )


@app.exception_handler(AssertionError)
async def assertion_error_handler(request: Request, error: AssertionError) -> Response:
    print(error)
    return JSONResponse(
        status_code=ErrorCode.COMMON_2002.http_status,
        content=jsonable_encoder({
            "type": ErrorCode.COMMON_2002.name,
            "title": ErrorCode.COMMON_2002.message,
            "status": ErrorCode.COMMON_2002.http_status,
            "instance": str(request.url)
        })
    )


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request, error: RequestValidationError) -> Response:
    print(error)
    return JSONResponse(
        status_code=ErrorCode.COMMON_2003.http_status,
        content=jsonable_encoder({
            "type": ErrorCode.COMMON_2003.name,
            "title": ErrorCode.COMMON_2003.message,
            "status": ErrorCode.COMMON_2003.http_status,
            "instance": str(request.url)
        })
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, error: Exception) -> Response:
    print(error)
    return JSONResponse(
        status_code=ErrorCode.COMMON_1000.http_status,
        content=jsonable_encoder({
            "type": ErrorCode.COMMON_1000.name,
            "title": ErrorCode.COMMON_1000.message,
            "status": ErrorCode.COMMON_1000.http_status,
            "instance": str(request.url)
        }),
    )
