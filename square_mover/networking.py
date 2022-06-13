import multiprocessing as mp

from square_mover.client import run


class NetworkingProcess:
    """There is two processes in square_mover game
    1. Main process (a.k.a render process), it loads Pygame to draw game state
    2. Network process (this class is responsible to create one), it receives
       updates from UDP server
    
    This processes communicate through Pipe:
    """
    def __init__(self) -> None:
        # render_conn - first side of the Pipe, used for:
        #     recv -> Updates from server
        #     send -> Player actions
        # network_conn - second side of the Pipe, used for:
        #     recv -> Player actions
        #     send -> Updates from server
        self.render_conn, network_conn = mp.Pipe()
        self.proc = mp.Process(target=run, args=(network_conn,))

    def start(self):
        self.proc.start()
    
    def send_action(self, action):
        self.render_conn.send(action)

    def get_events(self):
        while self.render_conn.poll():
            yield self.render_conn.recv()
