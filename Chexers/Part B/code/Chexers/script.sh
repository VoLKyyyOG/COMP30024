for ((i=0; i<100; i++))
    do
        python -m referee -v0 -l logs/red/red_random_$i.txt player.mix player.random player.random
        python -m referee -v0 -l logs/green/green_random_$i.txt player.random player.mix player.random
        python -m referee -v0 -l logs/blue/blue_random_$i.txt player.random player.random player.mix
    done

for ((i=0; i<100; i++))
    do
        python -m referee -v0 -l logs/red/red_greedy_$i.txt player.mix player.greedy player.greedy
        python -m referee -v0 -l logs/green/green_greedy_$i.txt player.greedy player.mix player.greedy
        python -m referee -v0 -l logs/blue/blue_greedy_$i.txt player.greedy player.greedy player.mix
    done

for ((i=0; i<100; i++))
    do
    python -m referee -v0 -l logs/red/red_runner_$i.txt player.mix player.runner player.runner
    python -m referee -v0 -l logs/green/green_runner_$i.txt player.runner player.mix player.runner
    python -m referee -v0 -l logs/blue/blue_runner_$i.txt player.runner player.runner player.mix
    done