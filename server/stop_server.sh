screen -ls | grep Detached | cut -d "." -f 1 | while read pid; 
do
	kill -9 $pid
done
