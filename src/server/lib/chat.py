from server.database.db import get_cursor

class Chat():
    def __init__(self):
        self.chat_queue = []

    def add_message(self, message):
        self.chat_queue.append(message)
        # Here you would also save the message to your database or message queue

        #Add message to DB
        cursor, sql_db = get_cursor()
        query = """
            INSERT INTO chat (sender_id, message)
            VALUES (%s, %s)
        """
        cursor.execute(query, (message['sender_id'], message['message']))
        sql_db.commit()
        cursor.close()
        print(f"New message from {message['sender_id']}: {message['message']}")

    def get_history(self):
        # This method would fetch chat history from your database or message queue
        cursor, _ = get_cursor(dictionary=True)
        query = "SELECT * FROM chat ORDER BY timestamp DESC LIMIT 100"
        cursor.execute(query)
        messages = cursor.fetchall()
        cursor.close()
        return messages

    def listen(self):
        # This method would be called in a loop to check for new messages
        while True:
            if self.chat_queue:
                message = self.chat_queue.pop(0)
                yield message
            else:
                break


chatroom = Chat()
