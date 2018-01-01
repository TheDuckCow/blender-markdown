import bpy
import textwrap

__version__ = '0.0.1'
__author__ = 'Patrick W. Crawford <moo-ack@theduckcow.com>'


class BlenderMarkdownClass():

	def __init__(self):
		self.wrap = 70
		pass

	def dpi_scale(self):
		return bpy.context.user_preferences.system.pixel_size

	# removes bold (**b** -> b), markdown links ([text](link.com) -> text)
	def strip_formatting(raw):
		stripped = raw
		features = []
		
		astrix = find(raw,"*")
		# format of: type, index start of stripped formatting, end index, param if appropriate
		# Example:
		# orig = "This is _one_ __BOLD__ **bold** update, [check it out](www.google.com), ![included-mobs](/MCprep.png?raw=true)"
		# stripped: "This is one BOLD bold update, check it out, [included-mobs]##"
		# features: [ ['itallics',8,10,None], ['bold',12,15,None], ['bold',17,20,None], ['link',30,41,'www.google.com'],
		#				['image',44,45,'/MCprep.png?raw=true']]
		# note in this example: 'image' will REAPLCE the ## with an actual image icon + url_open operator (no emboss) to
		# also, same way should actually put ## or somethign in front of links and have a CONSTRAINT icon at end,
		# then disply without emboss.
		
		return stripped,features
	
	def find(s, ch):
		return [i for i, ltr in enumerate(s) if ltr == ch]
	
	def replace_escapes(text):
		# replace things like \* to be back to * and so forth
		return text
	
	# SHOULD IMPLEMENT SCROLLBAR?
	def display(self, element, text, width=100):

		# apply scale factor for retina screens etc
		width /= self.dpi_scale()

		c = element.column()
		c.scale_y = 0.7
		#self.wrap = int(width/7)-4 # padding to account for some kerning
		self.wrap = width/7
		#wrap=75 # could try to inheret from self or window?
		text = str(text.encode('utf-8').decode('ascii', 'ignore'))
		label_lines = text.split("\n")
		for ln in label_lines:
			#stripped, features = self.strip_formatting(ln)
			# don't do line wrapping until inside each element,
			# e.g. if bullet points, must pad more.
			
			# need to transform wordwrap in the same parallel fashion,
			# so that indices still match end/start formatting
			
			if len(ln)==0:continue
			if ln.startswith('#'):
				self.display_headers(ln,c)
			elif ln.lstrip().startswith('- '):
				self.display_bullets(ln,c)
			else:
				sub_lns = textwrap.fill(ln, self.wrap)
				spl = sub_lns.split("\n")
				for s in spl:
					row = c.row()
					row.label(s)
		row = c.row()
		row.scale_y = 0.5
		row.label("")

	def display_headers(self,text,row):
		c = row
		ln = text

		spl = ln.split("#")
		ln = ""
		for y in spl:ln+=y
		
		sub_lns = textwrap.fill(ln, self.wrap)
		
		row = c.row()
		row.scale_y = 0.5
		row.label("")
		
		row = c.row()
		row.scale_y = 0.5
		row.label("."*200)
		
		sub_lns = sub_lns.split("\n")
		row = c.row()
		row.label(sub_lns[0], icon="RIGHTARROW")
		if len(sub_lns)>1:
			for s in sub_lns[1:]:
				row = c.row()
				row.label(s, icon="RIGHTARROW")
		
		row = c.row()
		row.scale_y = 0.2
		row.label("."*200)
		
		row = c.row()
		row.scale_y = 0.5
		row.label("")
	
	def display_bullets(self,text,row):
		# some kind of bullet
		ln = text
		c = row
		row = c.row()
		
		# determine indentation level
		indent = len(ln)-len(ln.lstrip())
		indent = int(indent/2)-indent%2 # a creative way to do "floor"
		
		# now draw leading indents (ie sums of 2 spaces in a row)
		row = c.row()
		for i in range(indent):
			row.label("",icon="BLANK1")	
		
		# draw first bullet
		sub_lns = textwrap.fill(ln.lstrip()[2:], self.wrap-2*indent-2)
		spl = sub_lns.split("\n")
		row.label(spl[0],icon="DOT")
		if len(spl)!=1:
			for s in spl[1:]:
				row = c.row()
				for i in range(indent):
					row.label("",icon="BLANK1")	
				row.label(s,icon="BLANK1")

# instance for importing
BlenderMarkdown = BlenderMarkdownClass()
