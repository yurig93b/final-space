from controller import FlightController
import socketio
def main():
    c = FlightController('/')
    sio = socketio.Client()
    sio.register_namespace(c)
    sio.connect("http://localhost:3000")

    #c.run()
    sio.wait()

if __name__ == "__main__":
    main()