import subprocess
import asyncio
import time

import typer
from typing_extensions import Annotated, Optional

from KickAI import KickAI
from DisplayInfo import DisplayInfo
from CustomAI import CustomAI
from RandomAI import RandomAI
from pyftg.socket.aio.gateway import Gateway
from pyftg.utils.logging import DEBUG, set_logging

app = typer.Typer(pretty_exceptions_enable=False)


async def start_process(host: str, port: int, character: str = "ZEN", game_num: int = 1):
    gateway = Gateway(host, port)
    
    agent1 = KickAI()
    gateway.register_ai("KickAI", agent1)

    agent2 = DisplayInfo()
    gateway.register_ai("DisplayInfo", agent2)

    agent3 = CustomAI()
    gateway.register_ai("CustomAI", agent3)

    agent4 = RandomAI()
    gateway.register_ai("RandomAI", agent4)

    await gateway.run_game([character, character], ["CustomAI", "RandomAI"], game_num)


@app.command()
def main(
        host: Annotated[Optional[str], typer.Option(help="Host used by DareFightingICE")] = "127.0.0.1",
        port: Annotated[Optional[int], typer.Option(help="Port used by DareFightingICE")] = 31415):
    asyncio.run(start_process(host, port))


if __name__ == '__main__':
    set_logging(log_level=DEBUG)

    # https://github.com/TeamFightingICE/FightingICE/blob/master/src/core/Game.java
    server_cmd = [
        "java",
        "-XstartOnFirstThread",
        "-cp",
        "FightingICE.jar:./lib/*:./lib/lwjgl/*:./lib/lwjgl/natives/macos/arm64/*:./lib/grpc/*",
        "Main",
        "--limithp", "400", "400",
        "--grey-bg",
        "--pyftg-mode",
        "--input-sync"
    ]
    server_proc = subprocess.Popen(server_cmd, cwd="../../DareFightingICE-7.0")

    # server_cmd = """
    # java -XstartOnFirstThread \
    # -cp "FightingICE.jar:./lib/*:./lib/lwjgl/*:./lib/lwjgl/natives/macos/arm64/*:./lib/grpc/*" \
    # Main --limithp 400 400 --grey-bg --pyftg-mode
    # """

    # # 별도 zsh에서 실행
    # server_proc = subprocess.Popen(
    #     ["zsh", "-c", server_cmd],
    #     cwd="../../DareFightingICE-7.0"
    # )

    time.sleep(2)

    try:
        app()
    finally:
        server_proc.terminate()
        server_proc.wait()
