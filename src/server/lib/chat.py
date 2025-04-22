import time
class Chat():
    def __init__(self):
        self.chat_queue = []

    def add_message(self, message):
        from database.db import do_query
        self.chat_queue.append(message)
        # Here you would also save the message to your database or message queue

        do_query("INSERT INTO chat (sender_id, message) VALUES (%s, %s)", (message['sender_id'], message['message']))
        print(f"New message from {message['sender_id']}: {message['message']}")

    def get_history(self):
        from database.db import  fetch_all

        # This method would fetch chat history from your database or message queue
        messages = fetch_all("SELECT * FROM chat ORDER BY timestamp DESC LIMIT 100")
        return messages

    def listen(self):
        # This method would be called in a loop to check for new messages
        while True:
            time.sleep(1)

            if self.chat_queue:
                while len(self.chat_queue) > 0:
                    message = self.chat_queue.pop(0)
                    time.sleep(0.1)
                    yield f'data: {message}\n\n'




chatroom = Chat()
