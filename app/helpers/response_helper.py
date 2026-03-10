class ResponseHelper:
    @staticmethod
    def success(message : str, data = None):
        return {
            "status" : " success",
            "message": message,
            "data" : data
        }
    
    @staticmethod
    def error(message : str, error_type: str = "BAD_REQUEST"):
        return{
            "status" : "error",
            "error_type" : error_type,
            "message" : message
        }