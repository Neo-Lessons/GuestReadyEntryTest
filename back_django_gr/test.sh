FFF=9
#echo $FFF
echo "${FFF}"

SNAME=localhost
echo $SNAME
echo $(nc -v -z localhost 5430)
echo $(nc -v -z localhost 5432)
echo $(nc -v -z 127.0.0.1 5430)
echo $(nc -v -z 127.0.0.1 5432)

if nc -z localhost 5430
then
  echo "seccess connection on localhost:5430"
fi

#while ! nc -z $SNAME 5432; do
#  sleep 0.1
#  echo "not connected"
#done

#x=1
#while [ $x -le 5 ];
#do
#  echo "ooo"
#  x=$(( x+1 ))
#done

#echo "end"


