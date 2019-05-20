for ((i=0; i<50; i++))
    do
        python -m referee -v0 -l logs/red/red_random_$i.txt _blank_ rando rando
        python -m referee -v0 -l logs/green/green_random_$i.txt rando _blank_ rando
        python -m referee -v0 -l logs/blue/blue_random_$i.txt rando rando _blank_
    done