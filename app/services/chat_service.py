from app.repository.chat_repository import ChatRepository


class ChatService:
    """ ChatService class to handle chat related requests """
    
    def __init__(self, chat_repository: ChatRepository = None):
        self.prefix = "/chat"
        self.chat_repository = chat_repository or ChatRepository()
        self.tags = ["chat"]

    def query_repository(self, query: str, user_role : str = None):
            # 1. Get allowed docs based on user role
        context_sections = self.chat_repository.fetch_documents(path="./resources/data", query=query, role=user_role)

        # 5. Return the final response to the user
        return {"response": context_sections}



