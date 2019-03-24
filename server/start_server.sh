for i in {20101..20200}
do
	# create a detached screen
	screen -dm python -m SimpleHTTPServer $i &
done