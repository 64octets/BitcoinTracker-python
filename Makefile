.PHONY: buy, sell

buy:
	python bitcoin/utilities/extract_buy.py
	mv buy.txt prices.txt
	python analysis.py

sell:
	python bitcoin/utilities/extract_sell.py
	mv sell.txt prices.txt
	python analysis.py
