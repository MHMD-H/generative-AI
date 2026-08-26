

class tokenbudget :
    def __init__ (self,max_tokens_per_request = 4000):
        self.max_tokens_per_request  = max_tokens_per_request
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.request_count = 0
    def limiting(self,total_tokens) :
        if total_tokens > self.max_tokens_per_request:
            raise ValueError("The context is too long")

    def calculate_tokens(self,input_tokens,output_tokns):
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokns
        self.request_count +=1
    
    def get_status(self):
        return  {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "request_count": self.request_count,
            "total_tokens": (
                self.total_input_tokens
                + self.total_output_tokens
            ),
        }