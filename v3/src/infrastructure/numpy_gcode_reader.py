import threading
import time


class NumpyGcodeReader(threading.Thread):
    def __init__(self, file_handle):
        threading.Thread.__init__(self)
        self.state = "Unstarted"
        self._running = True
        self._lock = threading.Lock()
        self._file_handle = file_handle
        self.commands_processed = 0
        self.layers = 0
        self.colors = {
            "Draw": [0.0, 1.0, 0.0, 1.0],
            "Move": [1.0, 0.0, 1.0, 1.0],
            "Vertical": [1.0, 0.2, 0.0, 1.0],
            "First Draw": [1.0, 0.0, 0.0, 1.0]
            }
        self._current_posisition = [0.0, 0.0, 0.0, 1.0]
        self._current_type = "Vertical"
        self._line_segments = []
        self._line_colors = []

    def get_current(self):
        return (self.state, self._line_segments, self._line_colors)

    def start(self):
        self.state = "Starting"
        threading.Thread.start(self)
        time.sleep(0.01) # Better way?

    def run(self):
        self.state = "Running"
        while self._running is True:
            with self._lock:
                if self._running is True:
                    self._run_loop()
        self._file_handle.close()
        print("Layers: %s" % self.layers)
        print("Commands: %s" % self.commands_processed)
        if self.state is not "Complete":
            self.state = "Aborted"

    def close(self):
        if self._running:
            self.state = "Aborting"
            self._running = False
        with self._lock:
            pass

    def _run_loop(self):
        try:
            self._process_command(self._file_handle.next())
        except StopIteration:
            self.state = "Complete"
            self._running = False

    def _process_command(self, command):
        self.commands_processed +=1
        details = command.split(' ')
        if details[0] in ["G0", "G00", "G1", "G01"]:
            
            next_move = list(self._current_posisition)
            next_color = self.colors['Move']

            for detail in details[1:]:
                if detail[0] == 'X':
                    next_move[0] = float(detail[1:])
                elif detail[0] == 'Y':
                    next_move[2] = float(detail[1:])
                elif detail[0] == 'Z':
                    self.layers += 1
                    next_move[1] = float(detail[1:])
                elif detail[0] == 'E':
                    if float(detail[1:]) > 0.0:
                        next_color = self.colors['Draw']
                    else:
                        next_color = self.colors['Move']

            self._line_segments.append(self._current_posisition)
            self._line_segments.append(next_move)
            self._line_colors.append(next_color)
            self._line_colors.append(next_color)
            self._current_posisition = next_move
