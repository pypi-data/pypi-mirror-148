from rich import box
from rich.align import Align
from rich.console import RenderableType
from rich.panel import Panel
from rich.pretty import Pretty
from textual.app import App
from textual.widget import Widget
from textual.widgets import DirectoryTree, Header, Footer, Placeholder, ScrollView

from tui.main import MainTable
from tui.system import SystemPanel


class HsfUi(App):

    async def on_load(self) -> None:
        """Sent before going in to application mode."""

        # Bind our basic keys
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        """Make a simple grid arrangement."""

        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")

        grid = await self.view.dock_grid(edge="left", name="left")

        grid.add_column(fraction=5, name="left", min_size=20)
        grid.add_column(fraction=3, name="right")

        grid.add_row(fraction=1, name="header", min_size=2)
        grid.add_row(fraction=4, name="main")

        grid.add_areas(
            software_info="left,header",
            system_info="right,header",
            main_content="left-start|right-end,main",
        )

        grid.place(
            software_info=Placeholder(name="software_info"),
            system_info=SystemPanel(name="System Info"),
            main_content=MainTable(name="main_content"),
        )


if __name__ == "__main__":
    HsfUi.run(title="HSF UI", log="hsf.log")
