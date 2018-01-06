import bpy
import textwrap
import re

__version__ = '0.0.1'
__author__ = 'Patrick W. Crawford <moo-ack@theduckcow.com>'


class BlenderMarkdownClass():

	def __init__(self):
		self.wrap = 70

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

		# padding to account for some kerning
		self.wrap = width/7

		# create an isolated subview, and space it closer together
		c = element.column()
		c.scale_y = 0.7

		# convert text, ignoring special characters beyond ascii
		text = str(text.encode('utf-8').decode('ascii', 'ignore'))
		label_lines = text.split("\n")
		lines = len(label_lines)

		for i,ln in enumerate(label_lines):
			#stripped, features = self.strip_formatting(ln)
			# don't do line wrapping until inside each element,
			# e.g. if bullet points, must pad more.
			
			# need to transform wordwrap in the same parallel fashion,
			# so that indices still match end/start formatting

			# regex pattern to find images in text

			nx_ln_srp = pv_ln_srp = ""
			if i<lines-2:
				nx_ln_srp = label_lines[i+1].rstrip()
			if i!=0:
				pv_ln_srp = label_lines[i-1].rstrip()
			
			if len(ln)==0:continue
			elif ln.startswith('#') and not ln.startswith('#'*7):
				# headers defiend up from 1-6 #'s, 7+ will be just displayed as-is
				self.display_headers(ln,c)
			elif nx_ln_srp == len(nx_ln_srp) * '=' and nx_ln_srp !='':
				self.display_headers(ln,c)
				continue
			elif ln == len(ln) * '=':
				continue # skip this, previously already recognized as header
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

		# get the <h#> level
		if text.startswith("######"):
			header_level = 6
		elif text.startswith("#####"):
			header_level = 5
		elif text.startswith("####"):
			header_level = 4
		elif text.startswith("###"):
			header_level = 3
		elif text.startswith("##"):
			header_level = 2
		elif text.startswith("#"):
			header_level = 1
		else:
			header_level = 1 # e.g. if it's based on === full header

		spl = ln.split("#")
		ln = ""
		for y in spl:ln+=y
		
		sub_lns = textwrap.fill(ln, self.wrap) # ERRORS occur here sometiems..
		
		row = c.row()
		row.scale_y = 0.5
		row.label("")
		
		row = c.row()
		row.scale_y = 0.5
		if header_level==1:
			row.label("."*1000)
		elif header_level <4:
			row.label("."*150)
		else:
			row.label("."*150)
		
		sub_lns = sub_lns.split("\n")
		row = c.row()
		row.label(sub_lns[0], icon="RIGHTARROW")
		if len(sub_lns)>1:
			for s in sub_lns[1:]:
				row = c.row()
				row.label(s, icon="RIGHTARROW")
		
		row = c.row()
		row.scale_y = 0.2
		if header_level==1:
			row.label("."*1000)
		elif header_level<4:
			row.label("."*150)
		
		row = c.row()
		row.scale_y = 0.5
		row.label("")
	
	def display_links_as_icons(self, text, row):

		"!\[[^\]]+\]\([^)]+\)"

		# the regex fpr image link is:


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
