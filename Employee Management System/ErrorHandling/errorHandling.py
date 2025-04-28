from fastapi import HTTPException,status
from fastapi.responses import JSONResponse
from traceback import format_exc,extract_tb
from sys import exc_info

# 200-299
def successHTTP(status,message,data):
    return JSONResponse(content={
        "status": status,
        "message": message,
        "data":data,
    }, status_code=201)
# 400-599

def clientErrorHandling(statCode,status,message,data):
    raise HTTPException(status_code=statCode,
                         detail={
                            "status": status,
                            "msg": message,
                            "data":data,
                        })

def serverErrorHandling(e):
    exc_type, exc_value, exc_traceback = exc_info()
    tb_info = extract_tb(exc_traceback)
        
    last_trace = tb_info[-1]  
    file_name, line_number, func_name, text = last_trace

    raise HTTPException(status_code=500,
                         detail={
                            "status": 500,
                            "error": type(e).__name__,
                            "file": file_name,
                            "line": line_number,
                            "function": func_name,
                            "code": text,
                            "msg": str(e)
                        })

def token_exception():
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or Expired Token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return token_exception

def credentials_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized Access",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return credentials_exception