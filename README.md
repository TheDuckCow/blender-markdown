# blender-markdown
Class for effectively displaying markdown formatted text in blender panels and popups

# Demo testing code

This is a complete sample demo code using the converter

```
import bpy
from .blender_markdown import BlenderMarkdown

sample_raw_markdown="""

# Primary title

## Secondary title

### Tertiary title

#### Click the button below to directly download MCprep
_By downloading and installing, you agree to the following [privacy policy](theduckcow.com/privacy-policy) including anonymous data tracking clause. Do not download the zip file from the readme page, you must click the button above_

### New in this (3.0.2) release:
- Added brand new feature: Meshswap block spawning!
  - You can now directly append meshswap groups into your scene from either the Shift-A menu, or the spawner panel
  - Future versions will expand blocks available significantly.
    - More indentation! Like a whooole ton, seriously! There is sooooo much indentation here.
  - Automatically can snap blocks to grid and auto prep materials (into cycles format or BI)
  - Demo link [available here](https://twitter.com/TheDuckCow/status/865971279979048961)
- Last version claimed compatibility improvement - this one actually makes it work properly for everyone. Enjoy your blending down to 2.72, for real this time!

### Numbered lists
1. This is number 1
2. This is number 2
   - With bullet 1
   - With bullet 2
3. This is number 3
   1. With sub 1
   2. With sub 2

Demo Usage
======

*[Mob spawner demo](https://www.youtube.com/watch?v=C3YoZx-seFE)*


"""


class DemoMarkdownPanel(bpy.types.Panel):
	"""Demo for the blender markdown panel"""
	bl_label = "Demo Markdown Panel"
	bl_idname = "OBJECT_PT_markdowndemo"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "object"

	def draw(self, context):
		layout = self.layout
		
		width = 0
		for region in bpy.context.area.regions:
			width = region.width

		col = layout.column()
		row = col.row(align=True)
		box = col.box()
		print(width)
		margin = 50 # this accounts for scrollbar of panel+ margins left/right of a box
		BlenderMarkdown.display(box,sample_raw_markdown,width-margin)
		
def register():
	bpy.utils.register_class(DemoMarkdownPanel)

def unregister():
	bpy.utils.unregister_class(DemoMarkdownPanel)

if __name__ == "__main__":
	register()

```