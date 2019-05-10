for ((i=0; i<20; i++))
    do
        python -m battleground -l logs/battleground/match_$i.txt player.mix gathering_data_thanks
    done