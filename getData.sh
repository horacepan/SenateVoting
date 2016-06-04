for i in $(seq 1 88); do
    wget https://www.govtrack.us/congress/votes/114-2016/s$i/export/csv -O data/$i.csv
done
