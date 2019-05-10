for ((i=0; i<2; i++))
    do
        python -m referee -l red_random_$i.txt player.mix player.random player.random
        python -m referee -l green_random_$i.txt player.random player.mix player.random
        python -m referee -l blue_random_$i.txt player.random player.random player.mix
    done

for ((i=0; i<2; i++))
    do
        python -m referee -l red_greedy_$i.txt player.mix player.greedy player.greedy
        python -m referee -l green_greedy_$i.txt player.greedy player.mix player.greedy
        python -m referee -l blue_greedy_$i.txt player.greedy player.greedy player.mix
    done

for ((i=0; i<2; i++))
    do
    python -m referee -l red_runner_$i.txt player.mix player.runner player.runner
    python -m referee -l green_runner_$i.txt player.runner player.mix player.runner
    python -m referee -l blue_runner_$i.txt player.runner player.runner player.mix
    done