import bpy
import re

modifier_type = "Build"
base_name     = 'IVY_Curve'

frame_per_face        = 1 / 4   # how to allocate a total build animation length according to the number of faces on a branch
build_interval        = 15      # how many frames to wait until starting to build 2nd branch
wait_between_branches = 4       # how many frames to wait between branches
build_start_frame     = 1       # Build animation start frame for the first ivy branch

ivy_objects = []

for current_obj in bpy.data.objects:  # browse all objects and filter out ivy branches
    if re.search(base_name, current_obj.name):          # if the object name contains the base_name
        current_obj.data.update(calc_tessface=True)     # calculate face data so that...
        face_count = len(current_obj.data.tessfaces)    # we can obtain the total number of faces
        
        ivy_objects.append( { "name" : current_obj.name, "facecount" : face_count } ) # add ivy object to list, include name and face count

biggest_obj = ""
most_faces  = 0

# Find the biggest object (highest face count)
for obj in ivy_objects:
    if obj["facecount"] > most_faces:   # if this object's facecount is larger than the previous highscore,
        most_faces  = obj["facecount"]  # then make this facecount one the new max
        biggest_obj = obj["name"]       # and update the biggest object's name

# set base build animation length according to the biggest object's size
base_build_length = int( most_faces * frame_per_face )

count = 0

# set animation length and start frames to all objects in list
for obj in ivy_objects:
    name = obj["name"]
    current_object = bpy.data.objects[name]

    # set the start frame of each object's build anim. by the order of names (which corresponds to order of creation)
    if count != 0: # Set build start for all the branches after the first one:
        bpy.data.objects[name].modifiers[modifier_type].frame_start = int( build_start_frame + build_interval + count * wait_between_branches )
    else:   # Set when the first branch starts to build
        bpy.data.objects[name].modifiers[modifier_type].frame_start = int( build_start_frame )
    
    # Set build length in proportion to face count
    ratio = obj["facecount"] / most_faces
    bpy.data.objects[name].modifiers[modifier_type].frame_duration = int( ratio * base_build_length )

    count += 1