from __future__ import annotations
from pathlib import Path
from logging import getLogger
import rich.repr
from rich import box
from rich.align import Align
from rich.console import RenderableType
from rich.panel import Panel
from rich.pretty import Pretty
from rich.table import Table

from textual import events
from textual.widget import Reactive, Widget
from textual.widgets import ScrollView

log = getLogger("rich")


@rich.repr.auto(angular=False)
class MainTable(Widget, can_focus=True):

    has_focus: Reactive[bool] = Reactive(False)
    mouse_over: Reactive[bool] = Reactive(False)
    style: Reactive[str] = Reactive("")
    height: Reactive[int | None] = Reactive(None)

    def __init__(self,
                 *,
                 name: str | None = None,
                 height: int | None = None) -> None:
        super().__init__(name=name)
        self.height = height
        self.images = list(
            Path("/home/cp264607/Datasets/ixi/T2/").glob("*.nii.gz"))

    def __rich_repr__(self) -> rich.repr.Result:
        yield "name", self.name
        yield "has_focus", self.has_focus, False
        yield "mouse_over", self.mouse_over, False

    def on_mount(self):
        self.set_interval(1, self.refresh)

    def render(self) -> RenderableType:
        table = Table(title="Star Wars Movies",
                      border_style="green" if self.mouse_over else "blue",
                      box=box.HEAVY if self.has_focus else box.ROUNDED,
                      style=self.style,
                      expand=True)

        table.add_column("File", justify="left", style="cyan", no_wrap=True)
        table.add_column("Status", style="magenta")
        table.add_column("Progress", justify="right", style="green")

        for image in self.images:
            table.add_row(str(image), "Pending...", "0%")

        return table

    async def on_focus(self, event: events.Focus) -> None:
        self.has_focus = True

    async def on_blur(self, event: events.Blur) -> None:
        self.has_focus = False

    async def on_enter(self, event: events.Enter) -> None:
        self.mouse_over = True

    async def on_leave(self, event: events.Leave) -> None:
        self.mouse_over = False
