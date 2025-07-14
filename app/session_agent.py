session_history = []

def store_user_query(query):
    session_history.append(query)

def get_personalized_keywords():
    return list(set(session_history))[-3:]  # last 3 unique
