from app.repository.vectorStoreDb import fetch_documents



def query_repository(query: str, user_role : str = None):
        # 1. Get allowed docs based on user role
    context_sections = fetch_documents(path="./resources/data", query=query, role=user_role)

    # 5. Return the final response to the user
    return {"response": context_sections}



