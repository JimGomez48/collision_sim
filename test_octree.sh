echo "Simulation Name,Objects,Sim Time, Last Frame, Min FPS, Max FPS, Min Compared, Max Compared" > results.csv

for n in 128 256 512
do
    #No collisions
    python main.py 1 $n --sim_time 3
    
    #Brute Force
    python main.py 2 $n --sim_time 3
    
    #Octree
    for l in `seq 1 1`
    do
        python main.py 3 $n --octree_levels $l --sim_time 10
    done
    
done
