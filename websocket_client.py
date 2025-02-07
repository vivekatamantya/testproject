import time
import websocket

class WebSocketClient:
    def __init__(self, host='localhost', port=8765, reconnect_attempts=5, reconnect_delay=2):
        self.uri = f"ws://{host}:{port}"
        self.websocket = None
        self.reconnect_attempts = reconnect_attempts
        self.reconnect_delay = reconnect_delay
        self.is_connected = False

    def connect(self):
        attempt = 0
        while attempt < self.reconnect_attempts:
            try:
                self.websocket = websocket.create_connection(self.uri)
                self.is_connected = True
                print("[INFO]Connected to WebSocket")
                return True
            except Exception as e:
                print(f"[ERROR]Connection failed: {e}, retrying in {self.reconnect_delay} seconds...")
                attempt += 1
                time.sleep(self.reconnect_delay)
        print("[INFO]Max reconnection attempts reached. Could not connect.")
        self.is_connected = False
        return False

    def disconnect(self):
        if self.websocket:
            self.websocket.close()
            print("[INFO]Disconnected")

    def send(self, message, send_on_reconnect=False):
        if self.websocket:
            try:
                self.websocket.send(message)
                print(f"[INFO]Sent: {message}")
            except websocket.WebSocketConnectionClosedException:
                print("[ERROR]Connection lost, attempting to reconnect...")
                self.reconnect()
                if send_on_reconnect:
                    self.send(message, send_on_reconnect)
        else:
            print("[INFO]Not connected")

    def receive(self):
        if self.websocket:
            try:
                response = self.websocket.recv()
                return response
            except websocket.WebSocketConnectionClosedException:
                print("[INFO]Connection lost, attempting to reconnect...")
                self.reconnect()
                return self.receive()
        print("[INFO]Not connected")
        return None

    def reconnect(self):
        self.disconnect()
        print("[INFO]Attempting to reconnect...")
        self.connect()

# Example usage
# def main():
#     ws = WebSocketClient(host='localhost', port=8765)
#     if ws.connect():
#         ws.send("Hello, WebSocket!")
#         while True:
#             try:
#                 response = ws.receive()
#             except KeyboardInterrupt:
#                 break
#         ws.disconnect()

# if __name__ == "__main__":
#     main()