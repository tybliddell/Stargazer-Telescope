from telescope import Telescope


def run(telescope: Telescope):
    while True:
        if len(telescope.queue) > 0:
            func, params = telescope.queue.popleft()
            func(*params)
