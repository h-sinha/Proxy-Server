for i in {20101..20200}
do
	python3 -m http.server --cgi $i &
done