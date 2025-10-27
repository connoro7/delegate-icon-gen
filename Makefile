PHONY: help clean

help:
	@echo "Makefile commands:"
	@echo "  make clean - Empty output directory of PNG files"
	@echo "  make help  - Show this help message"

clean:
	rm ./output/*.png

