echo "Objects,Octree Levels,Sim Time, Last Frame, Min FPS, Max FPS, Min Compared, Max Compared" > results.csv
for i in `seq 1 10`
do
    python main.py 3 512 --octree_levels $i --sim_time 10
done

