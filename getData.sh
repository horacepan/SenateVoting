# First arg is the year, 2nd arg is the session number, 3rd arg is the number of bills voted on
year=$1
session=$2
numBills=$3

mkdir -p data/$year
for i in $(seq 1 $numBills); do
    curl https://www.govtrack.us/congress/votes/$session-$year/s$i/export/csv -o data/$year/$i.csv
done
