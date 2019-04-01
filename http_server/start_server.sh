for i in {20101..20200}
do
	python -m http.server --cgi $i &
done