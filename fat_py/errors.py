def handle_error_response(resp):
    codes = {
        -1: FATdAPIError,
        -32600: InvalidRequest,
        -32601: MethodNotFound,
        -32602: InvalidParams,
        -32603: InternalError,
        -32700: ParseError,
        -32800: TokenNotFound,
        -32801: InvalidToken,
        -32802: InvalidAddress,
        -32803: TransactionNotFound,
        -32804: InvalidTransaction,
        -32805: TokenSyncing,
    }

    error = resp.json().get("error", {})
    message = error.get("message")
    code = error.get("code", -1)
    data = error.get("data", {})

    raise codes[code](message=message, code=code, data=data, response=resp)


class FATdAPIError(Exception):
    response = None
    data = {}
    code = -1
    message = "An unknown error occurred"

    def __init__(self, message=None, code=None, data=None, response=None):
        if data is None:
            data = {}
        self.response = response
        if message:
            self.message = message
        if code:
            self.code = code
        if data:
            self.data = data

    def __str__(self):
        if self.code:
            return "{}: {}".format(self.code, self.message)
        return self.message


class InvalidRequest(FATdAPIError):
    pass


class MethodNotFound(FATdAPIError):
    pass


class InvalidParams(FATdAPIError):
    pass


class InternalError(FATdAPIError):
    pass


class ParseError(FATdAPIError):
    pass


class TokenNotFound(FATdAPIError):
    pass


class InvalidToken(FATdAPIError):
    pass


class InvalidAddress(FATdAPIError):
    pass


class TransactionNotFound(FATdAPIError):
    pass


class InvalidTransaction(FATdAPIError):
    pass


class TokenSyncing(FATdAPIError):
    pass
