from __future__ import annotations

from logging import getLogger

import rich.repr
from cpuinfo import get_cpu_info
from deepsparse import cpu
# from GPUtil import getGPUs
from hsf.engines import deepsparse_support
from rich import box
from rich.align import Align
from rich.console import RenderableType
from rich.panel import Panel
from rich.pretty import Pretty
from rich.text import Text
from textual import events
from textual.widget import Reactive, Widget

log = getLogger("rich")


@rich.repr.auto(angular=False)
class SystemPanel(Widget, can_focus=True):
    """_summary_

    Args:
        Widget (_type_): _description_
        can_focus (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_

    Yields:
        _type_: _description_
    """
    style: Reactive[str] = Reactive("")
    height: Reactive[int | None] = Reactive(None)

    def __init__(self,
                 *,
                 name: str | None = None,
                 height: int | None = None) -> None:
        super().__init__(name=name)
        self.height = height
        self.cpuinfo = get_cpu_info()
        # self.gpuinfo = getGPUs()

    def __rich_repr__(self) -> rich.repr.Result:
        yield "name", self.name

    def system_info(self) -> Text:
        cpu_name = self.cpuinfo["brand_raw"]
        arch = self.cpuinfo["arch"]
        avx2 = cpu.cpu_avx2_compatible()
        avx512 = cpu.cpu_avx512_compatible()
        vnni = cpu.cpu_vnni_compatible()
        deepsparse = deepsparse_support()

        if vnni:
            instructions = "AVX512-VNNI"
        elif avx512:
            instructions = "AVX512"
        elif avx2:
            instructions = "AVX2"
        else:
            instructions = "None"

        return Text(
            f"{arch} CPU: {cpu_name}\nDeepSparse Support: {deepsparse} ({instructions})",
            no_wrap=True,
            overflow="ellipsis")

    def render(self) -> RenderableType:
        return Panel(
            Align.center(self.system_info(), vertical="middle"),
            title=self.name,
            style=self.style,
            height=self.height,
        )
