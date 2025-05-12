cdef class VXL:
    cdef MapData * map

    cpdef get_solid(self, int x, int y, int z)
    cpdef get_color(self, int x, int y, int z)
    cpdef tuple get_random_point(self, int x1, int y1, int x2, int y2)
    cpdef int get_z(self, int x, int y, int start = ?)
    cpdef int get_height(self, int x, int y)
    cpdef tuple get_safe_coords(self, int x, int y, int z)
    cpdef bint has_neighbors(self, int x, int y, int z)
    cpdef bint is_surface(self, int x, int y, int z)
    cpdef list get_neighbors(self, int x, int y, int z)
    cpdef int check_node(self, int x, int y, int z, bint destroy = ?)
    cpdef bint build_point(self, int x, int y, int z, tuple color)
    cpdef bint set_column_fast(self, int x, int y, int start_z,
        int end_z, int end_color_z, int color)
    cpdef update_shadows(self)
    
    
    
    










'''
<aoslib.vxl.VXL object at 0x09E5F620>
special variables
function variables
add_point = <built-in method add_point of aoslib.vxl.VXL object at 0x09E5F620>
add_static_light = <built-in method add_static_light of aoslib.vxl.VXL object at 0x09E5F620>
change_thread_state = <built-in method change_thread_state of aoslib.vxl.VXL object at 0x09E5F620>
check_only = <built-in method check_only of aoslib.vxl.VXL object at 0x09E5F620>
chunk_to_pointlist = <built-in method chunk_to_pointlist of aoslib.vxl.VXL object at 0x09E5F620>
cleanup = <built-in method cleanup of aoslib.vxl.VXL object at 0x09E5F620>
clear_checked_geometry = <built-in method clear_checked_geometry of aoslib.vxl.VXL object at 0x09E5F620>
color_block = <built-in method color_block of aoslib.vxl.VXL object at 0x09E5F620>
create_spot_shadows = <built-in method create_spot_shadows of aoslib.vxl.VXL object at 0x09E5F620>
destroy = <built-in method destroy of aoslib.vxl.VXL object at 0x09E5F620>
done_processing = <built-in method done_processing of aoslib.vxl.VXL object at 0x09E5F620>
draw = <built-in method draw of aoslib.vxl.VXL object at 0x09E5F620>
draw_sea = <built-in method draw_sea of aoslib.vxl.VXL object at 0x09E5F620>
draw_spot_shadows = <built-in method draw_spot_shadows of aoslib.vxl.VXL object at 0x09E5F620>
erase_prefab_from_world = <built-in method erase_prefab_from_world of aoslib.vxl.VXL object at 0x09E5F620>
generate_vxl = <built-in method generate_vxl of aoslib.vxl.VXL object at 0x09E5F620>
get_color = <built-in method get_color of aoslib.vxl.VXL object at 0x09E5F620>
get_color_tuple = <built-in method get_color_tuple of aoslib.vxl.VXL object at 0x09E5F620>
get_ground_colors = <built-in method get_ground_colors of aoslib.vxl.VXL object at 0x09E5F620>
get_max_modifiable_z = <built-in method get_max_modifiable_z of aoslib.vxl.VXL object at 0x09E5F620>
get_overview = <built-in method get_overview of aoslib.vxl.VXL object at 0x09E5F620>
get_point = <built-in method get_point of aoslib.vxl.VXL object at 0x09E5F620>
get_prefab_touches_world = <built-in method get_prefab_touches_world of aoslib.vxl.VXL object at 0x09E5F620>
get_solid = <built-in method get_solid of aoslib.vxl.VXL object at 0x09E5F620>
has_neighbors = <built-in method has_neighbors of aoslib.vxl.VXL object at 0x09E5F620>
is_space_to_add_blocks = <built-in method is_space_to_add_blocks of aoslib.vxl.VXL object at 0x09E5F620>
place_prefab_in_world = <built-in method place_prefab_in_world of aoslib.vxl.VXL object at 0x09E5F620>
post_load_draw_setup = <built-in method post_load_draw_setup of aoslib.vxl.VXL object at 0x09E5F620>
refresh_ground_colors = <built-in method refresh_ground_colors of aoslib.vxl.VXL object at 0x09E5F620>
remove_point = <built-in method remove_point of aoslib.vxl.VXL object at 0x09E5F620>
remove_point_nochecks = <built-in method remove_point_nochecks of aoslib.vxl.VXL object at 0x09E5F620>
remove_static_light = <built-in method remove_static_light of aoslib.vxl.VXL object at 0x09E5F620>
set_max_modifiable_z = <built-in method set_max_modifiable_z of aoslib.vxl.VXL object at 0x09E5F620>
set_point = <built-in method set_point of aoslib.vxl.VXL object at 0x09E5F620>
set_shadow_char_height = <built-in method set_shadow_char_height of aoslib.vxl.VXL object at 0x09E5F620>
update_static_light_colour = <built-in method update_static_light_colour of aoslib.vxl.VXL object at 0x09E5F620>







Function name	Segment	Start	Length	Locals	Arguments	R	F	L	M	O	S	B	T	=	X
															
init_ind2vec(long,float *,float *,float *)
initialize_vector_table(void)
index_to_vector(long)
CRC32(uchar *,int,uint)
encrypt(_object *,_object *)
replace_all(std::string &,char,char)
replace_unsupported_slashes(std::string &)
initialize(void)
load_kv6(char *,int)
scale_kv6(KV6Data *,int)
destroy_kv6(KV6Data *)
add_points(KV6Data *,_object *,int)
save_kv6(KV6Data *,char *)
set_default_color(float,float,float)
draw_display(KV6Display *)
calculate_kv6normal_for_quad(QuadKV6 &,glm::detail::tvec3<float> const&)
calculate_kv6normal_for_quad_nc(QuadNoColour &,glm::detail::tvec3<float> const&)
create_display(KV6Data *,int,int,bool)
destroy_display(KV6Display *)
extract_frustum(void)
sphere_in_frustum(float,float,float,float)
read_tga_bits(char const*,int *,int *,int *,uint *,signed char *)
load_tga_texture(char const*,uint,uint,uint)
get_vxl_size(uchar *,int)
initialise_floor(MapData *,int)
get_ground_colors_c(void)
reset_ground_colors_c(void)
add_ground_color_c(int,int,int,int)
generate_ground_color_table_c(void)
get_ground_color(int,int,int)
generate_static_light_color_table_c(int,int,int,int)
set_max_modifiable_z(int)
get_max_modifiable_z(void)
rotate_z_axis(Point,int)
rotate_x_axis(Point,int)
rotate_y_axis(Point,int)
get_prefab_touches_world(MapData *,KV6Data *,int,int,int,int,int,int,int)
place_prefab_in_world(MapData *,KV6Data *,int,int,int,int,int,int,int,int,float)
erase_prefab_from_world(MapData *,KV6Data *,int,int,int,int,int,int,int,int,float)
create_temp(void)
save_vxl(MapData *)
PrintGLErrors(char const*)
create_shadow_vbo(void)
set_shadow_char_height(int)
delete_shadow_vbo(void)
find_lowest_block(int,int,int,int &,int &,MapData *)
create_split_shadow_quad(float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float,float)
test_if_split_quad_in_frustum(float,float,float,float,float)
generate_shadow_quad(MapData *,float,float,float,float,float,float,float,float,int,int,int,int,float)
create_shadows_from_positions(MapData *,_object *,int)
draw_shadows(void)
add_static_point_light(MapData *,int,int,int,uchar,uchar,uchar,float)
update_static_point_light_colour(MapData *,int,int,int,uchar,uchar,uchar)
remove_static_point_light(MapData *,int,int,int)
calculate_static_lighting_quad_point(glm::detail::tvec3<float> const&,glm::detail::tvec3<float> const&,float,glm::detail::tvec3<float> const&,glm::detail::tvec3<float>&,float &)
get_quad_normals(glm::detail::tvec3<float> &,Quad &)
calculate_static_lighting_for_quad(std::map<int,StaticPointLight> *,Quad &,glm::detail::tvec3<float> const&)
check_for_static_light_influence(MapData *,Chunk *,StaticPointLight *,bool)
count_blocks_in_chunk(MapData const*,uint)
delta_chunk_count_with_block_change(MapData const*,uint,uint,uint,bool)
create_blank_map_data(int)
MapData::initialize(void)
initialise_chunk_data(MapData *)
initialise_sea_chunk_data(MapData *)
find_marker_points(MapData *)
post_load_map_setup(MapData *)
update_shadows(MapData *)
compute_static_occlusion(MapData *)
load_vxl(MapData *,uchar *,int)
load_part_vxl(MapData *,uchar *,int)
delete_map(MapData *)
add_leader(int,int,int,MapData *,int,bool)
add_marked_to_known_safe(void)
check_node(int,int,int,MapData *,FallingBlocks &)
update_shadow(MapData *,int,int,int,bool)
delete_gl_texture(uint *)
load_ao_texture(int)
reload_ao_texture(int)
delete_gl_vbo(MapData *)
cleanup_gl(MapData *)
post_load_draw_setup(MapData *,int)
draw_vbo(Chunk *,bool,bool)
compare_offsets(void const*,void const*)
make_sorted_offsets(void)
draw_position(MapData *,int,int,int,int)
update_vbo(Chunk *,MapData *)
draw_seascape_single_pass(MapData *)
update_vbo_sea(Chunk *,MapData *)
create_sea_data(MapData *)
draw_display(MapData *,int,int,int,int)
draw_sea(MapData *)
sunblock(MapData *,int,int,int)
compute_block_occlusion_texcoords(bool,bool,bool,bool,bool,bool,bool,bool)
compute_block_occlusion(BlockOcclusionTexCoords &,int,int,int,MapData *)
do_edge_highlight(BlockOcclusionTexCoords &,int,int,int,MapData *)
compute_dynamic_occlusion(MapData *,int,int,int)
print_occlusion_data(MapData *)
color_noise(int)
print_chunk_sizes(MapData *)
set_vert_text_coords(uchar,uchar,Quad &)
update_chunk_data(Chunk *,MapData *,bool)
update_chunks_near_player(MapData *)
refresh_ground_colors_c(MapData *)
run_thread(MapData *,int,uchar *,int)
change_thread(MapData *,int,uchar *,int)
close_thread(MapData *)
done_processing(MapData *)
Chunk::initialize(void)
MapData::refresh_block_and_chunk_counts(void)
_initvxl
__pyx_f_6aoslib_3vxl_3VXL_is_space_to_add_blocks(__pyx_obj_6aoslib_3vxl_VXL *,int)
__pyx_f_6aoslib_3vxl_3VXL__destroy(__pyx_obj_6aoslib_3vxl_VXL *)
__pyx_f_6aoslib_3vxl_3VXL__cleanup_gl(__pyx_obj_6aoslib_3vxl_VXL *)
__pyx_f_6aoslib_3vxl_3VXL_has_neighbors(__pyx_obj_6aoslib_3vxl_VXL *,int,int,int,int,int)
__pyx_f_6aoslib_3vxl_6CChunk__delete(__pyx_obj_6aoslib_3vxl_CChunk *)
__pyx_memoryview_get_item_pointer(__pyx_memoryview_obj *,_object *)
__pyx_memoryview_is_slice(__pyx_memoryview_obj *,_object *)
__pyx_memoryview_setitem_slice_assignment(__pyx_memoryview_obj *,_object *,_object *)
__pyx_memoryview_setitem_slice_assign_scalar(__pyx_memoryview_obj *,__pyx_memoryview_obj *,_object *)
__pyx_memoryview_setitem_indexed(__pyx_memoryview_obj *,_object *,_object *)
__pyx_memoryview_convert_item_to_object(__pyx_memoryview_obj *,char *)
__pyx_memoryview_assign_item_from_object(__pyx_memoryview_obj *,char *,_object *)
__pyx_memoryviewslice_convert_item_to_object(__pyx_memoryviewslice_obj *,char *)
__pyx_memoryviewslice_assign_item_from_object(__pyx_memoryviewslice_obj *,char *,_object *)
__Pyx_Import(_object *,_object *,int)
__pyx_array_getbuffer(_object *,bufferinfo *,int)
__pyx_memoryview_getbuffer(_object *,bufferinfo *,int)
__Pyx_AddTraceback(char const*,int,int,char const*)
__Pyx_Raise(_object *,_object *,_object *,_object *)
__Pyx_ErrRestore(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_13delete_shadow_vbo(_object *,_object *)
__pyx_pw_6aoslib_3vxl_11create_shadow_vbo(_object *,_object *)
__pyx_pw_6aoslib_3vxl_9sphere_in_frustum(_object *,_object *,_object *)
__Pyx_ParseOptionalKeywords(_object *,_object ***,_object *,_object **,long,char const*)
__pyx_tp_dealloc__memoryviewslice(_object *)
__pyx_tp_traverse__memoryviewslice(_object *,int (*)(_object *,void *),void *)
__pyx_tp_clear__memoryviewslice(_object *)
__pyx_tp_new__memoryviewslice(_typeobject *,_object *,_object *)
__pyx_tp_new_memoryview(_typeobject *,_object *,_object *)
__Pyx_PyInt_AsLong(_object *)
__pyx_getprop___pyx_memoryviewslice_base(_object *,void *)
__pyx_tp_clear_memoryview(_object *)
__pyx_fatalerror(char const*,...)
__pyx_tp_traverse_memoryview(_object *,int (*)(_object *,void *),void *)
__pyx_tp_dealloc_memoryview(_object *)
__pyx_memoryview___repr__(_object *)
__pyx_memoryview___str__(_object *)
__pyx_getprop___pyx_memoryview_T(_object *,void *)
__pyx_getprop___pyx_memoryview_base(_object *,void *)
__pyx_getprop___pyx_memoryview_shape(_object *,void *)
__pyx_getprop___pyx_memoryview_strides(_object *,void *)
__pyx_getprop___pyx_memoryview_suboffsets(_object *,void *)
__pyx_getprop___pyx_memoryview_ndim(_object *,void *)
__pyx_getprop___pyx_memoryview_itemsize(_object *,void *)
__pyx_getprop___pyx_memoryview_nbytes(_object *,void *)
__pyx_getprop___pyx_memoryview_size(_object *,void *)
__Pyx_TypeTest(_object *,_typeobject *)
__pyx_memslice_transpose(__Pyx_memviewslice *)
__pyx_memoryview_slice_copy(__pyx_memoryview_obj *,__Pyx_memviewslice *)
__pyx_memoryview_fromslice(__Pyx_memviewslice,int,_object * (*)(char *),int (*)(char *,_object *),int)
__pyx_memoryview_is_c_contig(_object *,_object *)
__pyx_memoryview_is_f_contig(_object *,_object *)
__pyx_memoryview_copy(_object *,_object *)
__pyx_memoryview_copy_fortran(_object *,_object *)
__pyx_memoryview_copy_new_contig(__Pyx_memviewslice const*,char const*,int,ulong,int,int)
__pyx_memoryview_copy_contents(__Pyx_memviewslice,__Pyx_memviewslice,int,int,int)
__pyx_memoryview_err_dim(_object *,char *,int)
_copy_strided_to_strided(char *,long *,char *,long *,long *,long *,int,ulong)
__pyx_memoryview_refcount_objects_in_slice(char *,long *,long *,int,int)
__pyx_memoryview_get_slice_from_memoryview(__pyx_memoryview_obj *,__Pyx_memviewslice *)
__Pyx_WriteUnraisable(char const*,int,int,char const*)
__pyx_memoryview___len__(_object *)
__pyx_memoryview___getitem__(_object *,_object *)
__pyx_mp_ass_subscript_memoryview(_object *,_object *,_object *)
_unellipsify(_object *,int)
__pyx_memoryview_slice_memviewslice(__Pyx_memviewslice *,long,long,long,int,int,int *,long,long,long,int,int,int,int)
__pyx_sq_item_memoryview(_object *,long)
__Pyx_GetException(_object **,_object **,_object **)
__pyx_memoryview__slice_assign_scalar(char *,long *,long *,int,ulong,void *)
__pyx_tp_dealloc_Enum(_object *)
__pyx_MemviewEnum___repr__(_object *)
__pyx_tp_traverse_Enum(_object *,int (*)(_object *,void *),void *)
__pyx_tp_clear_Enum(_object *)
__pyx_MemviewEnum___init__(_object *,_object *,_object *)
__pyx_tp_new_Enum(_typeobject *,_object *,_object *)
__pyx_tp_dealloc_array(_object *)
__pyx_tp_getattro_array(_object *,_object *)
__pyx_tp_traverse_array(_object *,int (*)(_object *,void *),void *)
__pyx_tp_clear_array(_object *)
__pyx_tp_new_array(_typeobject *,_object *,_object *)
__pyx_getprop___pyx_array_memview(_object *,void *)
__pyx_array___getattr__(_object *,_object *)
__pyx_array___getitem__(_object *,_object *)
__pyx_mp_ass_subscript_array(_object *,_object *,_object *)
__pyx_sq_item_array(_object *,long)
__pyx_tp_dealloc_6aoslib_3vxl_CChunk(_object *)
__pyx_pw_6aoslib_3vxl_6CChunk_1__init__(_object *,_object *,_object *)
__pyx_tp_new_6aoslib_3vxl_CChunk(_typeobject *,_object *,_object *)
__pyx_getprop_6aoslib_3vxl_6CChunk_x1(_object *,void *)
__pyx_getprop_6aoslib_3vxl_6CChunk_y1(_object *,void *)
__pyx_getprop_6aoslib_3vxl_6CChunk_z1(_object *,void *)
__pyx_getprop_6aoslib_3vxl_6CChunk_x2(_object *,void *)
__pyx_getprop_6aoslib_3vxl_6CChunk_y2(_object *,void *)
__pyx_getprop_6aoslib_3vxl_6CChunk_z2(_object *,void *)
__pyx_pw_6aoslib_3vxl_6CChunk_3draw(_object *,_object *)
__pyx_pw_6aoslib_3vxl_6CChunk_5get_colors(_object *,_object *)
__pyx_pw_6aoslib_3vxl_6CChunk_7to_block_list(_object *,_object *)
__pyx_pw_6aoslib_3vxl_6CChunk_9delete(_object *,_object *)
__pyx_pw_6aoslib_3vxl_6CChunk_11__del__(_object *,_object *)
__pyx_f_6aoslib_3vxl_get_color_tuple(int,int)
__pyx_tp_dealloc_6aoslib_3vxl_VXL(_object *)
__pyx_tp_traverse_6aoslib_3vxl_VXL(_object *,int (*)(_object *,void *),void *)
__pyx_tp_clear_6aoslib_3vxl_VXL(_object *)
__pyx_pw_6aoslib_3vxl_3VXL_1__init__(_object *,_object *,_object *)
__pyx_tp_new_6aoslib_3vxl_VXL(_typeobject *,_object *,_object *)
__pyx_getprop_6aoslib_3vxl_3VXL_minimap_texture(_object *,void *)
__pyx_setprop_6aoslib_3vxl_3VXL_minimap_texture(_object *,_object *,void *)
__pyx_pw_6aoslib_3vxl_3VXL_5create_spot_shadows(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_7set_shadow_char_height(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_9draw_spot_shadows(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_11done_processing(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_13change_thread_state(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_15add_static_light(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_17update_static_light_colour(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_19remove_static_light(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_21draw(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_23draw_sea(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_25get_ground_colors(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_27get_point(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_29get_solid(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_31is_space_to_add_blocks(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_33get_prefab_touches_world(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_35place_prefab_in_world(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_37erase_prefab_from_world(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_39color_block(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_41get_color(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_43get_color_tuple(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_45set_point(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_47add_point(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_49has_neighbors(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_51remove_point(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_53remove_point_nochecks(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_55check_only(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_57clear_checked_geometry(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_59chunk_to_pointlist(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_61post_load_draw_setup(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_63get_overview(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_65destroy(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_67cleanup(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_69refresh_ground_colors(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_71set_max_modifiable_z(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_73get_max_modifiable_z(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3VXL_75generate_vxl(_object *,_object *,_object *)
__pyx_pw_6aoslib_3vxl_1get_color_tuple(_object *,_object *)
__pyx_pw_6aoslib_3vxl_3reset_ground_colors(_object *,_object *)
__pyx_pw_6aoslib_3vxl_5generate_ground_color_table(_object *,_object *)
__pyx_pw_6aoslib_3vxl_7add_ground_color(_object *,_object *,_object *)
std::domain_error::~domain_error()
std::domain_error::~domain_error()
std::domain_error::~domain_error()
std::invalid_argument::~invalid_argument()
std::invalid_argument::~invalid_argument()
std::invalid_argument::~invalid_argument()
std::length_error::~length_error()
std::length_error::~length_error()
std::length_error::~length_error()
std::out_of_range::~out_of_range()
std::out_of_range::~out_of_range()
std::out_of_range::~out_of_range()
std::range_error::~range_error()
std::range_error::~range_error()
std::range_error::~range_error()
std::overflow_error::~overflow_error()
std::overflow_error::~overflow_error()
std::overflow_error::~overflow_error()
std::underflow_error::~underflow_error()
std::underflow_error::~underflow_error()
std::underflow_error::~underflow_error()
___clang_call_terminate
std::vector<GroundColor>::~vector()
set_point(int,int,int,MapData *,bool,int)
std::vector<ShadowQuad>::~vector()
boost::unordered::unordered_set<int,boost::hash<int>,std::equal_to<int>,std::allocator<int>>::~unordered_set()
color_block(int,int,int,MapData *)
std::vector<int *>::~vector()
std::_Rb_tree<int,std::pair<int const,StaticPointLight>,std::_Select1st<std::pair<int const,StaticPointLight>>,std::less<int>,std::allocator<std::pair<int const,StaticPointLight>>>::_M_erase(std::_Rb_tree_node<std::pair<int const,StaticPointLight>> *)
std::_Rb_tree<int,std::pair<int const,StaticPointLight>,std::_Select1st<std::pair<int const,StaticPointLight>>,std::less<int>,std::allocator<std::pair<int const,StaticPointLight>>>::_M_copy(std::_Rb_tree_node<std::pair<int const,StaticPointLight>> const*,std::_Rb_tree_node<std::pair<int const,StaticPointLight>>*)
boost::unordered::detail::table<boost::unordered::detail::map<std::allocator<std::pair<int const,BlockData>>,int,BlockData,boost::hash<int>,std::equal_to<int>>>::table(boost::unordered::detail::table<boost::unordered::detail::map<std::allocator<std::pair<int const,BlockData>>,int,BlockData,boost::hash<int>,std::equal_to<int>>> const&,std::allocator<boost::unordered::detail::ptr_node<std::pair<int const,BlockData>>> const&)
boost::unordered::detail::table_impl<boost::unordered::detail::map<std::allocator<std::pair<int const,BlockData>>,int,BlockData,boost::hash<int>,std::equal_to<int>>>::copy_buckets_to(boost::unordered::detail::buckets<std::allocator<std::pair<int const,BlockData>>,boost::unordered::detail::ptr_bucket,boost::unordered::detail::ptr_node<std::pair<int const,BlockData>>> const&,boost::unordered::detail::buckets<std::allocator<std::pair<int const,BlockData>>,boost::unordered::detail::ptr_bucket,boost::unordered::detail::ptr_node<std::pair<int const,BlockData>>>&)
std::vector<Quad>::_M_insert_aux(__gnu_cxx::__normal_iterator<Quad*,std::vector<Quad>>,Quad const&)
std::vector<Quad0>::_M_insert_aux(__gnu_cxx::__normal_iterator<Quad0*,std::vector<Quad0>>,Quad0 const&)
boost::unordered::detail::table_impl<boost::unordered::detail::map<std::allocator<std::pair<int const,int>>,int,int,boost::hash<int>,std::equal_to<int>>>::operator[](int const&)
boost::unordered::detail::table<boost::unordered::detail::map<std::allocator<std::pair<int const,int>>,int,int,boost::hash<int>,std::equal_to<int>>>::reserve_for_insert(ulong)
boost::unordered::detail::table_impl<boost::unordered::detail::map<std::allocator<std::pair<int const,int>>,int,int,boost::hash<int>,std::equal_to<int>>>::rehash_impl(ulong)
boost::unordered::detail::table_impl<boost::unordered::detail::set<std::allocator<int>,int,boost::hash<int>,std::equal_to<int>>>::emplace_impl<boost::unordered::detail::emplace_args1<int>>(int const&,boost::unordered::detail::emplace_args1<int> const&)
boost::unordered::detail::table<boost::unordered::detail::set<std::allocator<int>,int,boost::hash<int>,std::equal_to<int>>>::reserve_for_insert(ulong)
boost::unordered::detail::table_impl<boost::unordered::detail::set<std::allocator<int>,int,boost::hash<int>,std::equal_to<int>>>::rehash_impl(ulong)
boost::unordered::detail::table_impl<boost::unordered::detail::map<std::allocator<std::pair<int const,BlockData>>,int,BlockData,boost::hash<int>,std::equal_to<int>>>::erase_key(int const&)
std::_Rb_tree<int,std::pair<int const,StaticPointLight>,std::_Select1st<std::pair<int const,StaticPointLight>>,std::less<int>,std::allocator<std::pair<int const,StaticPointLight>>>::_M_insert_unique(std::_Rb_tree_iterator<std::pair<int const,StaticPointLight>>,std::pair<int const,StaticPointLight> const&)
std::_Rb_tree<int,std::pair<int const,StaticPointLight>,std::_Select1st<std::pair<int const,StaticPointLight>>,std::less<int>,std::allocator<std::pair<int const,StaticPointLight>>>::_M_insert_unique(std::pair<int const,StaticPointLight> const&)
std::vector<ShadowQuad>::_M_insert_aux(__gnu_cxx::__normal_iterator<ShadowQuad*,std::vector<ShadowQuad>>,ShadowQuad const&)
std::vector<GroundColor>::_M_insert_aux(__gnu_cxx::__normal_iterator<GroundColor*,std::vector<GroundColor>>,GroundColor const&)
boost::unordered::detail::table_impl<boost::unordered::detail::map<std::allocator<std::pair<int const,BlockData>>,int,BlockData,boost::hash<int>,std::equal_to<int>>>::operator[](int const&)
boost::unordered::detail::table<boost::unordered::detail::map<std::allocator<std::pair<int const,BlockData>>,int,BlockData,boost::hash<int>,std::equal_to<int>>>::reserve_for_insert(ulong)
boost::unordered::detail::table_impl<boost::unordered::detail::map<std::allocator<std::pair<int const,BlockData>>,int,BlockData,boost::hash<int>,std::equal_to<int>>>::rehash_impl(ulong)
std::vector<QuadKV6>::_M_insert_aux(__gnu_cxx::__normal_iterator<QuadKV6*,std::vector<QuadKV6>>,QuadKV6 const&)
std::vector<QuadNoColour>::_M_insert_aux(__gnu_cxx::__normal_iterator<QuadNoColour*,std::vector<QuadNoColour>>,QuadNoColour const&)
std::vector<QuadKV60>::_M_insert_aux(__gnu_cxx::__normal_iterator<QuadKV60*,std::vector<QuadKV60>>,QuadKV60 const&)
std::vector<QuadNoColour0>::_M_insert_aux(__gnu_cxx::__normal_iterator<QuadNoColour0*,std::vector<QuadNoColour0>>,QuadNoColour0 const&)
std::vector<BillboardQuad>::_M_insert_aux(__gnu_cxx::__normal_iterator<BillboardQuad*,std::vector<BillboardQuad>>,BillboardQuad const&)
check_only(int,int,int,MapData *)
Chunk::Chunk(void)
remove_point(int,int,int,MapData *)
UpdateThread::~UpdateThread()
UpdateThread::~UpdateThread()
UpdateThread::Run(void)
update_minimap(MapData *,bool)
std::vector<ChunkVBO *>::_M_insert_aux(__gnu_cxx::__normal_iterator<ChunkVBO **,std::vector<ChunkVBO *>>,ChunkVBO * const&)
std::vector<int *>::_M_insert_aux(__gnu_cxx::__normal_iterator<int **,std::vector<int *>>,int * const&)
MapData::MapData(void)
__GLOBAL__sub_I_vxl_cpp
_PyBuffer_Release	__stubs	000000000003FF8A	00000006			R	.	.	.	.	.	.	T	.	.
_PyCFunction_NewEx	__stubs	000000000003FF90	00000006			R	.	.	.	.	.	.	T	.	.
_PyCapsule_New	__stubs	000000000003FF96	00000006			R	.	.	.	.	.	.	T	.	.
_PyCode_New	__stubs	000000000003FF9C	00000006			R	.	.	.	.	.	.	T	.	.
_PyDict_GetItem	__stubs	000000000003FFA2	00000006			R	.	.	.	.	.	.	T	.	.
_PyDict_Items	__stubs	000000000003FFA8	00000006			R	.	.	.	.	.	.	T	.	.
_PyDict_New	__stubs	000000000003FFAE	00000006			R	.	.	.	.	.	.	T	.	.
_PyDict_Next	__stubs	000000000003FFB4	00000006			R	.	.	.	.	.	.	T	.	.
_PyDict_SetItem	__stubs	000000000003FFBA	00000006			R	.	.	.	.	.	.	T	.	.
_PyDict_SetItemString	__stubs	000000000003FFC0	00000006			R	.	.	.	.	.	.	T	.	.
_PyDict_Size	__stubs	000000000003FFC6	00000006			R	.	.	.	.	.	.	T	.	.
_PyErr_Clear	__stubs	000000000003FFCC	00000006			R	.	.	.	.	.	.	T	.	.
_PyErr_ExceptionMatches	__stubs	000000000003FFD2	00000006			R	.	.	.	.	.	.	T	.	.
_PyErr_Fetch	__stubs	000000000003FFD8	00000006			R	.	.	.	.	.	.	T	.	.
_PyErr_Format	__stubs	000000000003FFDE	00000006			R	.	.	.	.	.	.	T	.	.
_PyErr_NoMemory	__stubs	000000000003FFE4	00000006			R	.	.	.	.	.	.	T	.	.
_PyErr_NormalizeException	__stubs	000000000003FFEA	00000006			R	.	.	.	.	.	.	T	.	.
_PyErr_Occurred	__stubs	000000000003FFF0	00000006			R	.	.	.	.	.	.	T	.	.
_PyErr_Restore	__stubs	000000000003FFF6	00000006			R	.	.	.	.	.	.	T	.	.
_PyErr_SetNone	__stubs	000000000003FFFC	00000006			R	.	.	.	.	.	.	T	.	.
_PyErr_SetString	__stubs	0000000000040002	00000006			R	.	.	.	.	.	.	T	.	.
_PyErr_WarnEx	__stubs	0000000000040008	00000006			R	.	.	.	.	.	.	T	.	.
_PyErr_WriteUnraisable	__stubs	000000000004000E	00000006			R	.	.	.	.	.	.	T	.	.
_PyFile_SoftSpace	__stubs	0000000000040014	00000006			R	.	.	.	.	.	.	T	.	.
_PyFile_WriteObject	__stubs	000000000004001A	00000006			R	.	.	.	.	.	.	T	.	.
_PyFile_WriteString	__stubs	0000000000040020	00000006			R	.	.	.	.	.	.	T	.	.
_PyFloat_AsDouble	__stubs	0000000000040026	00000006			R	.	.	.	.	.	.	T	.	.
_PyFloat_FromDouble	__stubs	000000000004002C	00000006			R	.	.	.	.	.	.	T	.	.
_PyFrame_New	__stubs	0000000000040032	00000006			R	.	.	.	.	.	.	.	.	.
_PyGILState_Ensure	__stubs	0000000000040038	00000006			R	.	.	.	.	.	.	T	.	.
_PyGILState_Release	__stubs	000000000004003E	00000006			R	.	.	.	.	.	.	T	.	.
_PyImport_AddModule	__stubs	0000000000040044	00000006			R	.	.	.	.	.	.	T	.	.
_PyImport_Import	__stubs	000000000004004A	00000006			R	.	.	.	.	.	.	T	.	.
_PyInt_AsSsize_t	__stubs	0000000000040050	00000006			R	.	.	.	.	.	.	T	.	.
_PyInt_FromLong	__stubs	0000000000040056	00000006			R	.	.	.	.	.	.	T	.	.
_PyInt_FromSsize_t	__stubs	000000000004005C	00000006			R	.	.	.	.	.	.	T	.	.
_PyInt_FromString	__stubs	0000000000040062	00000006			R	.	.	.	.	.	.	T	.	.
_PyList_Append	__stubs	0000000000040068	00000006			R	.	.	.	.	.	.	T	.	.
_PyList_AsTuple	__stubs	000000000004006E	00000006			R	.	.	.	.	.	.	T	.	.
_PyList_GetItem	__stubs	0000000000040074	00000006			R	.	.	.	.	.	.	T	.	.
_PyList_New	__stubs	000000000004007A	00000006			R	.	.	.	.	.	.	T	.	.
_PyLong_AsLong	__stubs	0000000000040080	00000006			R	.	.	.	.	.	.	T	.	.
_PyLong_FromUnsignedLong	__stubs	0000000000040086	00000006			R	.	.	.	.	.	.	T	.	.
_PyMem_Malloc	__stubs	000000000004008C	00000006			R	.	.	.	.	.	.	T	.	.
_PyMem_Realloc	__stubs	0000000000040092	00000006			R	.	.	.	.	.	.	T	.	.
_PyModule_GetDict	__stubs	0000000000040098	00000006			R	.	.	.	.	.	.	T	.	.
_PyNumber_Add	__stubs	000000000004009E	00000006			R	.	.	.	.	.	.	T	.	.
_PyNumber_And	__stubs	00000000000400A4	00000006			R	.	.	.	.	.	.	T	.	.
_PyNumber_Divide	__stubs	00000000000400AA	00000006			R	.	.	.	.	.	.	T	.	.
_PyNumber_InPlaceMultiply	__stubs	00000000000400B0	00000006			R	.	.	.	.	.	.	T	.	.
_PyNumber_Index	__stubs	00000000000400B6	00000006			R	.	.	.	.	.	.	T	.	.
_PyNumber_Int	__stubs	00000000000400BC	00000006			R	.	.	.	.	.	.	T	.	.
_PyNumber_Long	__stubs	00000000000400C2	00000006			R	.	.	.	.	.	.	T	.	.
_PyNumber_Multiply	__stubs	00000000000400C8	00000006			R	.	.	.	.	.	.	T	.	.
_PyNumber_Remainder	__stubs	00000000000400CE	00000006			R	.	.	.	.	.	.	T	.	.
_PyNumber_Rshift	__stubs	00000000000400D4	00000006			R	.	.	.	.	.	.	T	.	.
_PyOS_snprintf	__stubs	00000000000400DA	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_Call	__stubs	00000000000400E0	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_CallFunctionObjArgs	__stubs	00000000000400E6	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_GC_Track	__stubs	00000000000400EC	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_GC_UnTrack	__stubs	00000000000400F2	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_GenericGetAttr	__stubs	00000000000400F8	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_GetAttr	__stubs	00000000000400FE	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_GetAttrString	__stubs	0000000000040104	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_GetBuffer	__stubs	000000000004010A	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_GetItem	__stubs	0000000000040110	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_GetIter	__stubs	0000000000040116	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_IsTrue	__stubs	000000000004011C	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_RichCompare	__stubs	0000000000040122	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_SetAttr	__stubs	0000000000040128	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_SetAttrString	__stubs	000000000004012E	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_SetItem	__stubs	0000000000040134	00000006			R	.	.	.	.	.	.	T	.	.
_PyObject_Size	__stubs	000000000004013A	00000006			R	.	.	.	.	.	.	T	.	.
_PySequence_GetItem	__stubs	0000000000040140	00000006			R	.	.	.	.	.	.	T	.	.
_PySequence_Tuple	__stubs	0000000000040146	00000006			R	.	.	.	.	.	.	T	.	.
_PyString_AsString	__stubs	000000000004014C	00000006			R	.	.	.	.	.	.	T	.	.
_PyString_AsStringAndSize	__stubs	0000000000040152	00000006			R	.	.	.	.	.	.	T	.	.
_PyString_FromFormat	__stubs	0000000000040158	00000006			R	.	.	.	.	.	.	T	.	.
_PyString_FromString	__stubs	000000000004015E	00000006			R	.	.	.	.	.	.	T	.	.
_PyString_FromStringAndSize	__stubs	0000000000040164	00000006			R	.	.	.	.	.	.	T	.	.
_PyString_InternFromString	__stubs	000000000004016A	00000006			R	.	.	.	.	.	.	T	.	.
_PySys_GetObject	__stubs	0000000000040170	00000006			R	.	.	.	.	.	.	T	.	.
_PyThread_allocate_lock	__stubs	0000000000040176	00000006			R	.	.	.	.	.	.	.	.	.
_PyThread_free_lock	__stubs	000000000004017C	00000006			R	.	.	.	.	.	.	.	.	.
_PyTraceBack_Here	__stubs	0000000000040182	00000006			R	.	.	.	.	.	.	T	.	.
_PyTuple_GetItem	__stubs	0000000000040188	00000006			R	.	.	.	.	.	.	T	.	.
_PyTuple_New	__stubs	000000000004018E	00000006			R	.	.	.	.	.	.	T	.	.
_PyTuple_Pack	__stubs	0000000000040194	00000006			R	.	.	.	.	.	.	T	.	.
_PyType_IsSubtype	__stubs	000000000004019A	00000006			R	.	.	.	.	.	.	T	.	.
_PyType_Modified	__stubs	00000000000401A0	00000006			R	.	.	.	.	.	.	T	.	.
_PyType_Ready	__stubs	00000000000401A6	00000006			R	.	.	.	.	.	.	T	.	.
_PyUnicodeUCS2_Compare	__stubs	00000000000401AC	00000006			R	.	.	.	.	.	.	T	.	.
_PyUnicodeUCS2_DecodeASCII	__stubs	00000000000401B2	00000006			R	.	.	.	.	.	.	T	.	.
_PyUnicodeUCS2_DecodeUTF8	__stubs	00000000000401B8	00000006			R	.	.	.	.	.	.	T	.	.
_PyUnicodeUCS2_FromUnicode	__stubs	00000000000401BE	00000006			R	.	.	.	.	.	.	T	.	.
_Py_FatalError	__stubs	00000000000401C4	00000006			.	.	.	.	.	.	.	T	.	.
_Py_GetVersion	__stubs	00000000000401CA	00000006			R	.	.	.	.	.	.	T	.	.
_Py_InitModule4_64	__stubs	00000000000401D0	00000006			R	.	.	.	.	.	.	T	.	.
__PyObject_CallMethod_SizeT	__stubs	00000000000401D6	00000006			R	.	.	.	.	.	.	T	.	.
__PyString_Eq	__stubs	00000000000401DC	00000006			R	.	.	.	.	.	.	T	.	.
check_only(int,int,int,MapData *)	__stubs	00000000000401E2	00000006	00000000		R	.	.	.	.	.	.	T	.	.
color_block(int,int,int,MapData *)	__stubs	00000000000401E8	00000006	00000000		R	.	.	.	.	.	.	T	.	.
remove_point(int,int,int,MapData *)	__stubs	00000000000401EE	00000006	00000000		R	.	.	.	.	.	.	T	.	.
update_minimap(MapData *,bool)	__stubs	00000000000401F4	00000006	00000000		R	.	.	.	.	.	.	T	.	.
set_point(int,int,int,MapData *,bool,int)	__stubs	00000000000401FA	00000006	00000000		R	.	.	.	.	.	.	T	.	.
Chunk::Chunk(void)	__stubs	0000000000040200	00000006	00000000		R	.	.	.	.	.	.	T	.	.
boost::unordered::detail::table_impl<boost::unordered::detail::map<std::allocator<std::pair<int const,BlockData>>,int,BlockData,boost::hash<int>,std::equal_to<int>>>::rehash_impl(ulong)	__stubs	0000000000040206	00000006	00000000		R	.	.	.	.	.	.	.	.	.
boost::unordered::detail::table_impl<boost::unordered::detail::map<std::allocator<std::pair<int const,BlockData>>,int,BlockData,boost::hash<int>,std::equal_to<int>>>::copy_buckets_to(boost::unordered::detail::buckets<std::allocator<std::pair<int const,BlockData>>,boost::unordered::detail::ptr_bucket,boost::unordered::detail::ptr_node<std::pair<int const,BlockData>>> const&,boost::unordered::detail::buckets<std::allocator<std::pair<int const,BlockData>>,boost::unordered::detail::ptr_bucket,boost::unordered::detail::ptr_node<std::pair<int const,BlockData>>>&)	__stubs	000000000004020C	00000006	00000000		R	.	.	.	.	.	.	.	.	.
boost::unordered::detail::table_impl<boost::unordered::detail::map<std::allocator<std::pair<int const,BlockData>>,int,BlockData,boost::hash<int>,std::equal_to<int>>>::erase_key(int const&)	__stubs	0000000000040212	00000006	00000000		R	.	.	.	.	.	.	.	.	.
boost::unordered::detail::table_impl<boost::unordered::detail::map<std::allocator<std::pair<int const,BlockData>>,int,BlockData,boost::hash<int>,std::equal_to<int>>>::operator[](int const&)	__stubs	0000000000040218	00000006	00000000		R	.	.	.	.	.	.	.	.	.
boost::unordered::detail::table_impl<boost::unordered::detail::map<std::allocator<std::pair<int const,int>>,int,int,boost::hash<int>,std::equal_to<int>>>::rehash_impl(ulong)	__stubs	000000000004021E	00000006	00000000		R	.	.	.	.	.	.	.	.	.
boost::unordered::detail::table_impl<boost::unordered::detail::map<std::allocator<std::pair<int const,int>>,int,int,boost::hash<int>,std::equal_to<int>>>::operator[](int const&)	__stubs	0000000000040224	00000006	00000000		R	.	.	.	.	.	.	.	.	.
boost::unordered::detail::table_impl<boost::unordered::detail::set<std::allocator<int>,int,boost::hash<int>,std::equal_to<int>>>::rehash_impl(ulong)	__stubs	000000000004022A	00000006	00000000		R	.	.	.	.	.	.	.	.	.
boost::unordered::detail::table_impl<boost::unordered::detail::set<std::allocator<int>,int,boost::hash<int>,std::equal_to<int>>>::emplace_impl<boost::unordered::detail::emplace_args1<int>>(int const&,boost::unordered::detail::emplace_args1<int> const&)	__stubs	0000000000040230	00000006	00000000		R	.	.	.	.	.	.	.	.	.
boost::unordered::detail::table<boost::unordered::detail::map<std::allocator<std::pair<int const,BlockData>>,int,BlockData,boost::hash<int>,std::equal_to<int>>>::reserve_for_insert(ulong)	__stubs	0000000000040236	00000006	00000000		R	.	.	.	.	.	.	.	.	.
boost::unordered::detail::table<boost::unordered::detail::map<std::allocator<std::pair<int const,BlockData>>,int,BlockData,boost::hash<int>,std::equal_to<int>>>::table(boost::unordered::detail::table<boost::unordered::detail::map<std::allocator<std::pair<int const,BlockData>>,int,BlockData,boost::hash<int>,std::equal_to<int>>> const&,std::allocator<boost::unordered::detail::ptr_node<std::pair<int const,BlockData>>> const&)	__stubs	000000000004023C	00000006	00000000		R	.	.	.	.	.	.	.	.	.
boost::unordered::detail::table<boost::unordered::detail::map<std::allocator<std::pair<int const,int>>,int,int,boost::hash<int>,std::equal_to<int>>>::reserve_for_insert(ulong)	__stubs	0000000000040242	00000006	00000000		R	.	.	.	.	.	.	.	.	.
boost::unordered::detail::table<boost::unordered::detail::set<std::allocator<int>,int,boost::hash<int>,std::equal_to<int>>>::reserve_for_insert(ulong)	__stubs	0000000000040248	00000006	00000000		R	.	.	.	.	.	.	.	.	.
MapData::MapData(void)	__stubs	000000000004024E	00000006	00000000		R	.	.	.	.	.	.	T	.	.
std::vector<ShadowQuad>::_M_insert_aux(__gnu_cxx::__normal_iterator<ShadowQuad*,std::vector<ShadowQuad>>,ShadowQuad const&)	__stubs	0000000000040254	00000006	00000000		R	.	.	.	.	.	.	.	.	.
std::vector<GroundColor>::_M_insert_aux(__gnu_cxx::__normal_iterator<GroundColor*,std::vector<GroundColor>>,GroundColor const&)	__stubs	000000000004025A	00000006	00000000		R	.	.	.	.	.	.	.	.	.
std::vector<QuadNoColour>::_M_insert_aux(__gnu_cxx::__normal_iterator<QuadNoColour*,std::vector<QuadNoColour>>,QuadNoColour const&)	__stubs	0000000000040260	00000006	00000000		R	.	.	.	.	.	.	.	.	.
std::vector<BillboardQuad>::_M_insert_aux(__gnu_cxx::__normal_iterator<BillboardQuad*,std::vector<BillboardQuad>>,BillboardQuad const&)	__stubs	0000000000040266	00000006	00000000		R	.	.	.	.	.	.	.	.	.
std::vector<QuadNoColour0>::_M_insert_aux(__gnu_cxx::__normal_iterator<QuadNoColour0*,std::vector<QuadNoColour0>>,QuadNoColour0 const&)	__stubs	000000000004026C	00000006	00000000		R	.	.	.	.	.	.	.	.	.
std::vector<Quad>::_M_insert_aux(__gnu_cxx::__normal_iterator<Quad*,std::vector<Quad>>,Quad const&)	__stubs	0000000000040272	00000006	00000000		R	.	.	.	.	.	.	.	.	.
std::vector<Quad0>::_M_insert_aux(__gnu_cxx::__normal_iterator<Quad0*,std::vector<Quad0>>,Quad0 const&)	__stubs	0000000000040278	00000006	00000000		R	.	.	.	.	.	.	.	.	.
std::vector<QuadKV6>::_M_insert_aux(__gnu_cxx::__normal_iterator<QuadKV6*,std::vector<QuadKV6>>,QuadKV6 const&)	__stubs	000000000004027E	00000006	00000000		R	.	.	.	.	.	.	.	.	.
std::vector<QuadKV60>::_M_insert_aux(__gnu_cxx::__normal_iterator<QuadKV60*,std::vector<QuadKV60>>,QuadKV60 const&)	__stubs	0000000000040284	00000006	00000000		R	.	.	.	.	.	.	.	.	.
std::vector<ChunkVBO *>::_M_insert_aux(__gnu_cxx::__normal_iterator<ChunkVBO **,std::vector<ChunkVBO *>>,ChunkVBO * const&)	__stubs	000000000004028A	00000006	00000000		R	.	.	.	.	.	.	.	.	.
std::vector<int *>::_M_insert_aux(__gnu_cxx::__normal_iterator<int **,std::vector<int *>>,int * const&)	__stubs	0000000000040290	00000006	00000000		R	.	.	.	.	.	.	.	.	.
std::_Rb_tree<int,std::pair<int const,StaticPointLight>,std::_Select1st<std::pair<int const,StaticPointLight>>,std::less<int>,std::allocator<std::pair<int const,StaticPointLight>>>::_M_insert_unique(std::pair<int const,StaticPointLight> const&)	__stubs	0000000000040296	00000006	00000000		R	.	.	.	.	.	.	.	.	.
std::_Rb_tree<int,std::pair<int const,StaticPointLight>,std::_Select1st<std::pair<int const,StaticPointLight>>,std::less<int>,std::allocator<std::pair<int const,StaticPointLight>>>::_M_insert_unique(std::_Rb_tree_iterator<std::pair<int const,StaticPointLight>>,std::pair<int const,StaticPointLight> const&)	__stubs	000000000004029C	00000006	00000000		R	.	.	.	.	.	.	.	.	.
std::_Rb_tree<int,std::pair<int const,StaticPointLight>,std::_Select1st<std::pair<int const,StaticPointLight>>,std::less<int>,std::allocator<std::pair<int const,StaticPointLight>>>::_M_copy(std::_Rb_tree_node<std::pair<int const,StaticPointLight>> const*,std::_Rb_tree_node<std::pair<int const,StaticPointLight>>*)	__stubs	00000000000402A2	00000006	00000000		R	.	.	.	.	.	.	.	.	.
std::_Rb_tree<int,std::pair<int const,StaticPointLight>,std::_Select1st<std::pair<int const,StaticPointLight>>,std::less<int>,std::allocator<std::pair<int const,StaticPointLight>>>::_M_erase(std::_Rb_tree_node<std::pair<int const,StaticPointLight>> *)	__stubs	00000000000402A8	00000006	00000000		R	.	.	.	.	.	.	.	.	.
_PHYSFS_close	__stubs	00000000000402AE	00000006			R	.	.	.	.	.	.	.	.	.
_PHYSFS_fileLength	__stubs	00000000000402B4	00000006			R	.	.	.	.	.	.	.	.	.
_PHYSFS_openRead	__stubs	00000000000402BA	00000006			R	.	.	.	.	.	.	.	.	.
_PHYSFS_read	__stubs	00000000000402C0	00000006			R	.	.	.	.	.	.	.	.	.
_glBindTexture	__stubs	00000000000402C6	00000006			R	.	.	.	.	.	.	T	.	.
_glColor3f	__stubs	00000000000402CC	00000006			R	.	.	.	.	.	.	T	.	.
_glColorPointer	__stubs	00000000000402D2	00000006			R	.	.	.	.	.	.	T	.	.
_glDeleteTextures	__stubs	00000000000402D8	00000006			R	.	.	.	.	.	.	T	.	.
_glDepthMask	__stubs	00000000000402DE	00000006			R	.	.	.	.	.	.	T	.	.
_glDisable	__stubs	00000000000402E4	00000006			R	.	.	.	.	.	.	T	.	.
_glDisableClientState	__stubs	00000000000402EA	00000006			R	.	.	.	.	.	.	T	.	.
_glDrawArrays	__stubs	00000000000402F0	00000006			R	.	.	.	.	.	.	T	.	.
_glEnable	__stubs	00000000000402F6	00000006			R	.	.	.	.	.	.	T	.	.
_glEnableClientState	__stubs	00000000000402FC	00000006			R	.	.	.	.	.	.	T	.	.
_glGenTextures	__stubs	0000000000040302	00000006			R	.	.	.	.	.	.	T	.	.
_glGetError	__stubs	0000000000040308	00000006			R	.	.	.	.	.	.	T	.	.
_glGetFloatv	__stubs	000000000004030E	00000006			R	.	.	.	.	.	.	T	.	.
_glNormalPointer	__stubs	0000000000040314	00000006			R	.	.	.	.	.	.	T	.	.
_glPixelStorei	__stubs	000000000004031A	00000006			R	.	.	.	.	.	.	T	.	.
_glPopMatrix	__stubs	0000000000040320	00000006			R	.	.	.	.	.	.	T	.	.
_glPushMatrix	__stubs	0000000000040326	00000006			R	.	.	.	.	.	.	T	.	.
_glTexCoordPointer	__stubs	000000000004032C	00000006			R	.	.	.	.	.	.	T	.	.
_glTexImage2D	__stubs	0000000000040332	00000006			R	.	.	.	.	.	.	T	.	.
_glTexParameteri	__stubs	0000000000040338	00000006			R	.	.	.	.	.	.	T	.	.
_glTexSubImage2D	__stubs	000000000004033E	00000006			R	.	.	.	.	.	.	T	.	.
_glTranslatef	__stubs	0000000000040344	00000006			R	.	.	.	.	.	.	T	.	.
_glVertexPointer	__stubs	000000000004034A	00000006			R	.	.	.	.	.	.	T	.	.
sf::Mutex::Lock(void)	__stubs	0000000000040350	00000006			R	.	.	.	.	.	.	T	.	.
sf::Mutex::Unlock(void)	__stubs	0000000000040356	00000006			R	.	.	.	.	.	.	T	.	.
sf::Mutex::Mutex(void)	__stubs	000000000004035C	00000006			R	.	.	.	.	.	.	T	.	.
sf::Mutex::~Mutex()	__stubs	0000000000040362	00000006			R	.	.	.	.	.	.	T	.	.
sf::Sleep(float)	__stubs	0000000000040368	00000006			R	.	.	.	.	.	.	T	.	.
sf::Thread::Wait(void)	__stubs	000000000004036E	00000006			R	.	.	.	.	.	.	T	.	.
sf::Thread::Launch(void)	__stubs	0000000000040374	00000006			R	.	.	.	.	.	.	T	.	.
sf::Thread::Thread(void)	__stubs	000000000004037A	00000006			R	.	.	.	.	.	.	T	.	.
sf::Thread::~Thread()	__stubs	0000000000040380	00000006			R	.	.	.	.	.	.	T	.	.
std::ios::widen(char)	__stubs	0000000000040386	00000006			R	.	.	.	.	.	.	.	.	.
std::ostream::put(char)	__stubs	000000000004038C	00000006			R	.	.	.	.	.	.	T	.	.
std::ostream::flush(void)	__stubs	0000000000040392	00000006			R	.	.	.	.	.	.	T	.	.
std::ostream::operator<<(int)	__stubs	0000000000040398	00000006			R	.	.	.	.	.	.	.	.	.
std::string::_M_leak_hard(void)	__stubs	000000000004039E	00000006			R	.	.	.	.	.	.	T	.	.
std::string::_Rep::_M_destroy(std::allocator<char> const&)	__stubs	00000000000403A4	00000006			R	.	.	.	.	.	.	.	.	.
std::string::append(char const*,ulong)	__stubs	00000000000403AA	00000006			R	.	.	.	.	.	.	T	.	.
std::string::string(char const*,std::allocator<char> const&)	__stubs	00000000000403B0	00000006			R	.	.	.	.	.	.	.	.	.
std::logic_error::~logic_error()	__stubs	00000000000403B6	00000006			R	.	.	.	.	.	.	T	.	.
std::runtime_error::~runtime_error()	__stubs	00000000000403BC	00000006			R	.	.	.	.	.	.	T	.	.
std::ios_base::Init::Init(void)	__stubs	00000000000403C2	00000006			R	.	.	.	.	.	.	T	.	.
std::__ostream_insert<char,std::char_traits<char>>(std::ostream &,char const*,long)	__stubs	00000000000403C8	00000006			R	.	.	.	.	.	.	.	.	.
std::__throw_bad_alloc(void)	__stubs	00000000000403CE	00000006			.	.	.	.	.	.	.	T	.	.
std::_Rb_tree_decrement(std::_Rb_tree_node_base *)	__stubs	00000000000403D4	00000006			R	.	.	.	.	.	.	.	.	.
std::_Rb_tree_increment(std::_Rb_tree_node_base *)	__stubs	00000000000403DA	00000006			R	.	.	.	.	.	.	.	.	.
std::__throw_length_error(char const*)	__stubs	00000000000403E0	00000006			.	.	.	.	.	.	.	T	.	.
std::_Rb_tree_rebalance_for_erase(std::_Rb_tree_node_base *,std::_Rb_tree_node_base&)	__stubs	00000000000403E6	00000006			R	.	.	.	.	.	.	.	.	.
std::_Rb_tree_insert_and_rebalance(bool,std::_Rb_tree_node_base *,std::_Rb_tree_node_base *,std::_Rb_tree_node_base&)	__stubs	00000000000403EC	00000006			R	.	.	.	.	.	.	.	.	.
std::terminate(void)	__stubs	00000000000403F2	00000006			.	.	.	.	.	.	.	T	.	.
operator delete[](void *)	__stubs	00000000000403F8	00000006			R	.	.	.	.	.	.	T	.	.
operator delete(void *)	__stubs	00000000000403FE	00000006			R	.	.	.	.	.	.	T	.	.
operator new[](ulong)	__stubs	0000000000040404	00000006			R	.	.	.	.	.	.	T	.	.
operator new(ulong)	__stubs	000000000004040A	00000006			R	.	.	.	.	.	.	T	.	.
___cxa_begin_catch	__stubs	0000000000040410	00000006			R	.	.	.	.	.	.	T	.	.
___cxa_end_catch	__stubs	0000000000040416	00000006			R	.	.	.	.	.	.	T	.	.
___cxa_rethrow	__stubs	000000000004041C	00000006			.	.	.	.	.	.	.	T	.	.
__Unwind_Resume	__stubs	0000000000040422	00000006			.	.	.	.	.	.	.	T	.	.
___bzero	__stubs	0000000000040428	00000006			R	.	.	.	.	.	.	.	.	.
___cxa_atexit	__stubs	000000000004042E	00000006			R	.	.	.	.	.	.	T	.	.
___stack_chk_fail	__stubs	0000000000040434	00000006			.	.	.	.	.	.	.	.	.	.
_ceil	__stubs	000000000004043A	00000006			R	.	.	.	.	.	.	T	.	.
_clock	__stubs	0000000000040440	00000006			R	.	.	.	.	.	.	T	.	.
_cos	__stubs	0000000000040446	00000006			R	.	.	.	.	.	.	T	.	.
_fclose	__stubs	000000000004044C	00000006			R	.	.	.	.	.	.	T	.	.
_floor	__stubs	0000000000040452	00000006			R	.	.	.	.	.	.	T	.	.
_floorf	__stubs	0000000000040458	00000006			R	.	.	.	.	.	.	T	.	.
_fopen$DARWIN_EXTSN	__stubs	000000000004045E	00000006			R	.	.	.	.	.	.	.	.	.
_fread	__stubs	0000000000040464	00000006			R	.	.	.	.	.	.	T	.	.
_free	__stubs	000000000004046A	00000006			R	.	.	.	.	.	.	T	.	.
_fwrite	__stubs	0000000000040470	00000006			R	.	.	.	.	.	.	T	.	.
_getcwd	__stubs	0000000000040476	00000006			R	.	.	.	.	.	.	T	.	.
_malloc	__stubs	000000000004047C	00000006			R	.	.	.	.	.	.	T	.	.
_memcpy	__stubs	0000000000040482	00000006			R	.	.	.	.	.	.	T	.	.
_memmove	__stubs	0000000000040488	00000006			R	.	.	.	.	.	.	T	.	.
_memset_pattern16	__stubs	000000000004048E	00000006			R	.	.	.	.	.	.	T	.	.
_printf	__stubs	0000000000040494	00000006			R	.	.	.	.	.	.	T	.	.
_puts	__stubs	000000000004049A	00000006			R	.	.	.	.	.	.	T	.	.
_qsort	__stubs	00000000000404A0	00000006			R	.	.	.	.	.	.	T	.	.
_rand	__stubs	00000000000404A6	00000006			R	.	.	.	.	.	.	T	.	.
_realloc	__stubs	00000000000404AC	00000006			R	.	.	.	.	.	.	T	.	.
_sin	__stubs	00000000000404B2	00000006			R	.	.	.	.	.	.	T	.	.
_strlen	__stubs	00000000000404B8	00000006			R	.	.	.	.	.	.	T	.	.
_vsnprintf	__stubs	00000000000404BE	00000006			R	.	.	.	.	.	.	T	.	.
'''
