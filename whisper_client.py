import socket
import pyaudio
import threading

# Audio configuration
FORMAT = pyaudio.paInt16     # Equivalent to S16_LE
CHANNELS = 1                 # Mono audio
RATE = 16000                 # Sample rate (Hz)
CHUNK = 1024                 # Buffer size (small chunks for low latency)

# Server configuration
HOST = 'localhost'           # IP of the server
PORT = 43007             # Port the server is listening on

def audio_stream(client_socket):
    """Capture and stream audio data continuously."""
    audio = pyaudio.PyAudio()

    # Open audio stream with low latency settings
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print(f"✅ Connected to {HOST}:{PORT}. Streaming audio...")

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            client_socket.sendall(data)
    except KeyboardInterrupt:
        print("\n⏹️ Streaming stopped by user.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        client_socket.close()

def main():
    """Establish socket connection and handle reconnection logic."""
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, PORT))
                audio_stream(client_socket)
        except ConnectionRefusedError:
            print(f"🔁 Server not available. Retrying in 5 seconds...")
        except Exception as e:
            print(f"❗ Unexpected error: {e}")
        finally:
            import time
            time.sleep(5)  # Delay before retrying connection

if __name__ == "__main__":
    main()
