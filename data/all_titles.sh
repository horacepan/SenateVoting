numBills=88
year=2016
for i in $(seq 1 $numBills); do
    head -n 1 $year/$i.csv >> titles_2016.txt
done
