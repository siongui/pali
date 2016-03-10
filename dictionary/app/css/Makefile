SOURCE_CSS_FILES=$(filter-out %.min.css, $(wildcard *.css))
MINIFIED_CSS=app.min.css

minify: concat
	@# remove css comments
	sed -r ':a; s%(.*)/\*.*\*/%\1%; ta; /\/\*/ !b; N; ba' -i $(MINIFIED_CSS)
	@# remove leading spaces and tabs
	sed 's/^\s*//' -i $(MINIFIED_CSS)
	@# remove trailing spaces, tabs, and newline
	sed 's/\s*$$//' -i $(MINIFIED_CSS)
	@# remove newline
	tr --delete '\n' < $(MINIFIED_CSS) > tmp.css
	mv tmp.css $(MINIFIED_CSS)

concat:
	cat $(SOURCE_CSS_FILES) > $(MINIFIED_CSS)
