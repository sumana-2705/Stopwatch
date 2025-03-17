from time import monotonic

from textual import on
from textual.app import App
from textual.widgets import Footer,Header,Button,Static
from textual.reactive import reactive
from textual.containers import ScrollableContainer

class TimeDisplay(Static):
    """A widget to display elapsed time."""

    accumulated_time = 0
    start_time = monotonic()
    time_elapsed = reactive(0)

    def on_mount (self):
        self.update_timer = self.set_interval(
            1/60,
            self.update_time_elapsed,
            pause=True,
        )

    def update_time_elapsed(self):
        self.time_elapsed = (
            self.accumulated_time +
            (monotonic() - self.start_time) 
        )

    def watch_time_elapsed(self) -> None:
        """Called when the time attribute changes."""
        time = self.time_elapsed
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        """Method to stop the time display updating."""
        self.accumulated_time = self.time_elapsed
        self.update_timer.pause()

    def reset(self) -> None:
        """Method to reset the time display to zero."""
        self.accumulated_time = 0
        self.time_elapsed = 0



class Stopwatch(Static):
    """ custom widget """
    @on(Button.Pressed, "#start")
    def start_stopwatch(self):
        self.add_class("started")
        self.query_one(TimeDisplay).start()

    @on(Button.Pressed, "#stop")
    def stop_stopwatch(self):
        self.remove_class("started")
        self.query_one(TimeDisplay).stop()

    @on(Button.Pressed, "#reset")
    def reset_stopwatch(self):
        self.query_one(TimeDisplay).reset()

    def compose(self):
        yield Button("Start", variant="success",id="start")
        yield Button("Stop", variant="error", id="stop")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00.00")

class StopwatchApp(App):
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("a", "add_stopwatch","Add"),
        ("r", "remove_stopwatch", "Remove"),
        ]
    
    CSS_PATH= "styles.css"

    def compose(self):
        yield Header(show_clock=True)
        yield Footer()
        with ScrollableContainer(id="stopwatches"):
            yield Stopwatch()
            yield Stopwatch()
            yield Stopwatch()

        # Another method to use containers
        """        
        yield ScrollableContainer(
            Stopwatch(),
            Stopwatch(),
            Stopwatch(),
            id="stopwatches"
        )
        """
        
    
    # prefix (action_) is important to because it is an action method
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_add_stopwatch(self):
        stopwatch = Stopwatch()
        container = self.query_one("#stopwatches")
        container.mount(stopwatch)
        stopwatch.scroll_visible()

    def action_remove_stopwatch(self):
        stopwatches = self.query(Stopwatch)
        if stopwatches:
            stopwatches.last().remove()
    

if __name__ == "__main__":
    StopwatchApp().run()
