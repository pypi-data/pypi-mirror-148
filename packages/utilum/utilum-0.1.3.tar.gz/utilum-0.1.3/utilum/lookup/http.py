class STATUS:
    def __init__(self):

        self.CONTINUE = 100
        self.SWITCHING_PROTOCOLS = 101
        self.PROCESSING = 102
        
        self.OK = 200
        self.CREATED = 201
        self.ACCEPTED = 202
        self.NON_AUTHORITATIVE_INFORMATION = 203
        self.NO_CONTENT = 204	
        self.RESET_CONTENT = 205
        self.PARTIAL_CONTENT = 206
        self.MULTI_STATUS = 207	
        
        self.MULTIPLE_CHOICES = 300
        self.MOVED_PERMANENTLY = 301
        self.MOVED_TEMPORARILY = 302
        self.SEE_OTHER = 303	
        self.NOT_MODIFIED = 304	
        self.USE_PROXY = 305	
        self.TEMPORARY_REDIRECT = 307
        self.PERMANENT_REDIRECT = 308
        
        self.BAD_REQUEST = 400	
        self.UNAUTHORIZED = 401
        self.PAYMENT_REQUIRED = 402
        self.FORBIDDEN = 403	
        self.NOT_FOUND = 404	
        self.METHOD_NOT_ALLOWED = 405
        self.NOT_ACCEPTABLE = 406	
        self.PROXY_AUTHENTICATION_REQUIRED = 407
        self.REQUEST_TIMEOUT = 408	
        self.CONFLICT = 409	
        self.GONE = 410	
        self.LENGTH_REQUIRED = 411
        self.PRECONDITION_FAILED = 412
        self.REQUEST_TOO_LONG = 413	
        self.REQUEST_URI_TOO_LONG = 414	
        self.UNSUPPORTED_MEDIA_TYPE = 415	
        self.REQUESTED_RANGE_NOT_SATISFIABLE = 416
        self.EXPECTATION_FAILED = 417
        self.IM_A_TEAPOT = 418	
        self.INSUFFICIENT_SPACE_ON_RESOURCE = 419
        self.METHOD_FAILURE = 420	
        self.MISDIRECTED_REQUEST = 421
        self.UNPROCESSABLE_ENTITY = 422
        self.LOCKED = 423	
        self.FAILED_DEPENDENCY = 424	
        self.PRECONDITION_REQUIRED = 428
        self.TOO_MANY_REQUESTS = 429	
        self.REQUEST_HEADER_FIELDS_TOO_LARGE = 431
        self.UNAVAILABLE_FOR_LEGAL_REASONS = 451
        
        self.INTERNAL_SERVER_ERROR = 500
        self.NOT_IMPLEMENTED = 501
        self.BAD_GATEWAY = 502	
        self.SERVICE_UNAVAILABLE = 503
        self.GATEWAY_TIMEOUT = 504	
        self.HTTP_VERSION_NOT_SUPPORTED = 505
        self.INSUFFICIENT_STORAGE = 507	
        self.NETWORK_AUTHENTICATION_REQUIRED = 511