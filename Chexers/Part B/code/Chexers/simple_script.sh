python -m referee -l logs/sample/red_random.txt player.mix player.random player.random
python -m referee -l logs/sample/green_random.txt player.random player.mix player.random
python -m referee -l logs/sample/blue_random.txt player.random player.random player.mix

python -m referee -l logs/sample/red_greedy.txt player.mix player.greedy player.greedy
python -m referee -l logs/sample/green_greedy.txt player.greedy player.mix player.greedy
python -m referee -l logs/sample/blue_greedy.txt player.greedy player.greedy player.mix

python -m referee -l logs/sample/red_runner.txt player.mix player.runner player.runner
python -m referee -l logs/sample/green_runner.txt player.runner player.mix player.runner
python -m referee -l logs/sample/blue_runner.txt player.runner player.runner player.mix

cd '.\logs\sample'

python results.py

$SHELL