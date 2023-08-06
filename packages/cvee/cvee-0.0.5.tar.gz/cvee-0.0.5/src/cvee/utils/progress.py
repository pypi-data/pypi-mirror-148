from rich.progress import Progress, TextColumn, BarColumn, ProgressColumn, TimeRemainingColumn
from rich.text import Text

import cvee.utils

_progress_bar = None


def get_progress_bar():
    global _progress_bar
    if _progress_bar is None:
        _progress_bar = ProgressBar()
    return _progress_bar


class ProgressBar(Progress):
    def __init__(self):
        console = cvee.utils.get_console()
        super().__init__(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[magenta]{task.completed}/{task.total}"),
            TimeElapsedColumn(compact=True),
            TimeRemainingColumn(compact=True),
            console=console,
        )

    def step(self, task_id, description=None):
        if description is not None:
            self.update(task_id, advance=1, description=description)
        else:
            self.update(task_id, advance=1)


class TimeElapsedColumn(ProgressColumn):
    def __init__(self, compact=True):
        self.compact = compact
        super().__init__()

    def render(self, task):
        elapsed = task.finished_time if task.finished else task.elapsed
        style = "progress.elapsed"

        if elapsed is None:
            return Text("--:--" if self.compact else "-:--:--", style=style)

        minutes, seconds = divmod(int(elapsed), 60)
        hours, minutes = divmod(minutes, 60)

        if self.compact and not hours:
            formatted = f"{minutes:02d}:{seconds:02d}"
        else:
            formatted = f"{hours:d}:{minutes:02d}:{seconds:02d}"

        return Text(formatted, style=style)


def track(sequence, total=None, description="", update_period=0.1):
    pbar = get_progress_bar()
    with pbar:
        yield from pbar.track(sequence, total=total, description=description, update_period=update_period)


if __name__ == "__main__":
    import time

    log = cvee.get_logger("cvee")

    for i in track(range(10)):
        log.info(str(i))
        time.sleep(1)
