bl_info = {
    "name": "RandomDirection",
    "author": "Shawn Zhang",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object",
    "description": "Extrude a random face of the Cube to a random direction for a random distance",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}


import bpy 
import bmesh
import random
import math
from mathutils import Vector
from bpy.types import (
	AddonPreferences,
	Operator,
	Panel,
	PropertyGroup,
)

class OBJECT_OT_randomdirection(Operator):
	bl_label = "RandomDirection"
	bl_idname = "object.randomdirection"
	bl_description = "Extrude a random face of the Cube to a random direction for a random distance"
	bl_space_type = "VIEW 3D"
	bl_region_type = "UI"
	bl_options = {'REGISTER','UNDO'}
	
	
	def execute(self,context):
	
	
	
	
	
		#choose which side and how many steps
		steps = random.randint(10,90)
		
		


			#add a cube to the scene
		bpy.ops.mesh.primitive_cube_add(enter_editmode=False,size=10,align='WORLD')

		#if I comment the adding cube out, it works in the right way.
		cube = bpy.context.active_object

			#enter edit mode, and enter face select mode
		bpy.ops.object.mode_set(mode="EDIT")
		bpy.ops.mesh.select_all(action="DESELECT")
		bpy.context.tool_settings.mesh_select_mode = (True, False , True)

			#get data of the cube
		bm = bmesh.from_edit_mesh(cube.data)
		bm.verts.ensure_lookup_table()
			#bm.verts[0].select=True

		#attempt to extrude the face
		def extrude_faces():
			
			#random travel distance
			dx = random.randint(-90,90)
			dy = random.randint(-90,90)
			dz = random.randint(-90,90)

			#select a radnom face in edit mode
			#side = random.randint(0,5)
			
			#after comment the cube out, and add selection range
			side = random.randint(0,6)
			#the original value should be 0~5, after couple times, the variable could be as large as you want, since at the moment the model will have many many faces.
			print(side)
			#but right now, there must be some problems.
			#the prgram can not break the process and re-selct a random face of current mesh
			
			bm.faces.ensure_lookup_table()
			bm.faces[side].select=True
			#bpy.context.tool_settings.transform_pivot_point
			bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False},TRANSFORM_OT_translate={"value":(dx,dy,dz),"constraint_axis":(False,False,False)})
			#here is another problem, if I shut down all of the constraint axis, the final model suggests that the extrude direction still follows the Z-axis as a constraint axis. That's the reason why the direction only extends to one way.

		#excute
		for i in range(steps):
			extrude_faces()
			
			
		#back to Object mode after the extrusion
		bpy.ops.object.mode_set(mode="OBJECT")
		return {'FINISHED'}



def menu_func(self,context):
	self.layout.operator(OBJECT_OT_randomdirection.bl_idname)

def register():
	bpy.utils.register_class(OBJECT_OT_randomdirection)
	bpy.types.VIEW3D_MT_object.append(menu_func)
	
def unregister():
	bpy.utils.unregister_class(OBJECT_OT_randomdirection)
	bpy.types.VIEW3D_MT_object.remove(menu_func)
	
if __name__ == "__main__":
	register()