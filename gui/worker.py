import threading


class Worker:
    def __init__(self, root, on_done):
        self.root = root
        self.on_done = on_done
        self.thread = None
        self.result = None

    @property
    def busy(self):
        return self.thread is not None and self.thread.is_alive()

    def start(self, func, *args):
        self.result = None
        self.thread = threading.Thread(target=self.run, args=(func, *args), daemon=True)
        self.thread.start()
        self.root.after(100, self.poll)

    def run(self, func, *args):
        try:
            self.result = func(*args)
        except Exception as e:
            self.result = e

    def poll(self):
        if self.busy:
            self.root.after(100, self.poll)
        else:
            self.on_done(self.result)