def handle_error_response(resp):
    codes = {
        -1: PegNetdAPIError,
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
        -32806: NoEntryCredits,
        -32808: AddressNotFound,
        -32809: ErrorNotFound,
    }

    error = resp.json().get("error", {})
    message = error.get("message")
    code = error.get("code", -1)
    data = error.get("data", {})

    raise codes[code](message=message, code=code, data=data, response=resp)


class PegNetdAPIError(Exception):
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


class InvalidRequest(PegNetdAPIError):
    pass


class MethodNotFound(PegNetdAPIError):
    pass


class InvalidParams(PegNetdAPIError):
    pass


class InternalError(PegNetdAPIError):
    pass


class ParseError(PegNetdAPIError):
    pass


class TokenNotFound(PegNetdAPIError):
    pass


class InvalidToken(PegNetdAPIError):
    pass


class InvalidAddress(PegNetdAPIError):
    pass


class TransactionNotFound(PegNetdAPIError):
    pass


class InvalidTransaction(PegNetdAPIError):
    pass


class TokenSyncing(PegNetdAPIError):
    pass


class NoEntryCredits(PegNetdAPIError):
    pass


class AddressNotFound(PegNetdAPIError):
    pass


class ErrorNotFound(PegNetdAPIError):
    pass
