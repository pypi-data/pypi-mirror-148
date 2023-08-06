from . import md_lexing

class construct_html:
	def __init__(self, md):
		self.table = None
		self.space_repeated = None
		self.html = "\n"
		self.md = md

	def HEADING1(self, tok):
		s = tok.value[2:]
		self.html += "<h1 class=\"header1\" >" +  s + "</h1>\n"

	def construct(self):
		md_lexing.MDLexer.lexer.input(self.md)
		self.html += "<html>\n"

		while True:
			tok = md_lexing.MDLexer.lexer.token()
			if not tok:
				break
			elif tok.type == "HEADING1":
				self.HEADING1(tok)

		self.html += "</html>"
		return self.html


if __name__ == "__main__":
	pass
