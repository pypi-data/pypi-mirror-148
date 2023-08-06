import ply.lex as lex

class MDLexer:
	tokens = [
	"ROWS",
	"EMPHASIS",
	"ITALIC",
	"LINKS",
	"FOOT_NOTES",
	"QUOTED_TRIPLE",
	"QUOTED_DOUBLE",
	"QUOTED_SINGLE",
	"HEADING1",
	"HEADING2",
	"HEADING3",
	"HEADING4",
	"HEADING5",
	"HEADING6",
	"NEWLINE",
	"STR",
	"SPACE",
	"ESCAPE_SQUARE_BRACKET"
	]

	# For drawing tables
	t_ROWS = r"(" + r"\|" + r"\ +" + ".+" + r"\ +" + r"\|" + r")+"
	t_EMPHASIS = r"__.+__"
	t_ITALIC = "\*\*.+\*\*"
	t_LINKS = r'\[.+\]\(.+\)'
	t_QUOTED_TRIPLE = r'```(.|\n)*?```'
	t_QUOTED_DOUBLE = r'``.+``'
	t_QUOTED_SINGLE = r'`.+`'
	t_FOOT_NOTES = r"\[\^.+\]?"
	t_HEADING1 = r'\n\#\s.+'
	t_HEADING2 = r'\n\#\#\s.+'
	t_HEADING3 = r'\n\#\#\#\s.+'
	t_HEADING4 = r'\n\#\#\#\#\s.+'
	t_HEADING5 = r'\n\#\#\#\#\#\s.+'
	t_HEADING6 = r'\n\#\#\#\#\#\#\s.+'
	t_NEWLINE = r'\n'
	t_STR = r'.'
	t_SPACE = r'\ '
	# For escaping [ from being lexed into LINKS
	t_ESCAPE_SQUARE_BRACKET = r'\\\['

	t_ignore = "\t"

	def t_error(t):
		print("Illegal Character %s " % t.value[0])
		t.lexer.skip(1)

	lexer = lex.lex()

if __name__ == "__main__":
	pass
