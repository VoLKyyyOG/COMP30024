python -m referee -v0 -l logs/sample/red_greedy.txt player.mix player.greedy player.greedy
python -m referee -v0 -l logs/sample/green_greedy.txt player.greedy player.mix player.greedy
python -m referee -v0 -l logs/sample/blue_greedy.txt player.greedy player.greedy player.mix

python -m referee -v0 -l logs/sample/red_runner.txt player.mix player.runner player.runner
python -m referee -v0 -l logs/sample/green_runner.txt player.runner player.mix player.runner
python -m referee -v0 -l logs/sample/blue_runner.txt player.runner player.runner player.mix

python -m referee -v0 -l logs/sample/red_slow.txt player.mix player.slow player.slow
python -m referee -v0 -l logs/sample/green_slow.txt player.slow player.mix player.slow
python -m referee -v0 -l logs/sample/blue_slow.txt player.slow player.slow player.mix

cd '.\logs\sample'

python results.py

$SHELL