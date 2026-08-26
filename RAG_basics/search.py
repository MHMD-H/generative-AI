

class semintic_search :
    def __init__(self , vectorstore  = None) :
        self.vectorstore = vectorstore



    def vector_search(self,query,k,filter:dict) :
        return self.vectorstore.similarity_search(query=query,k=k,filter=filter)



class keyword_search :
    def __init__(self,bm25=None) : 
        self.bm25 = bm25
        

    def add_document(self,document) :
        return self.bm25.from_documents(document)

    
    def key_search(self,query) :
        return self.bm25.invoke(query)


class hybird_search :
    def __init__(self,method = None):
        self.method = method

    def RRF(self,query,semintic_search_method,hybird_search_method) :
        return self.method.rank_fusion(query=query,run_manager=[semintic_search_method,hybird_search_method])