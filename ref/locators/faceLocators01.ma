//Maya ASCII 2014 scene
//Name: faceLocators01.ma
//Last modified: Tue, Sep 29, 2015 10:57:17 AM
//Codeset: ANSI_X3.4-1968
requires maya "2014";
requires -nodeType "mentalrayFramebuffer" -nodeType "mentalrayOutputPass" -nodeType "mentalrayRenderPass"
		 -nodeType "mentalrayUserBuffer" -nodeType "mentalraySubdivApprox" -nodeType "mentalrayCurveApprox"
		 -nodeType "mentalraySurfaceApprox" -nodeType "mentalrayDisplaceApprox" -nodeType "mentalrayOptions"
		 -nodeType "mentalrayGlobals" -nodeType "mentalrayItemsList" -nodeType "mentalrayShader"
		 -nodeType "mentalrayUserData" -nodeType "mentalrayText" -nodeType "mentalrayTessellation"
		 -nodeType "mentalrayPhenomenon" -nodeType "mentalrayLightProfile" -nodeType "mentalrayVertexColors"
		 -nodeType "mentalrayIblShape" -nodeType "mapVizShape" -nodeType "mentalrayCCMeshProxy"
		 -nodeType "cylindricalLightLocator" -nodeType "discLightLocator" -nodeType "rectangularLightLocator"
		 -nodeType "sphericalLightLocator" -nodeType "abcimport" -nodeType "mia_physicalsun"
		 -nodeType "mia_physicalsky" -nodeType "mia_material" -nodeType "mia_material_x" -nodeType "mia_roundcorners"
		 -nodeType "mia_exposure_simple" -nodeType "mia_portal_light" -nodeType "mia_light_surface"
		 -nodeType "mia_exposure_photographic" -nodeType "mia_exposure_photographic_rev" -nodeType "mia_lens_bokeh"
		 -nodeType "mia_envblur" -nodeType "mia_ciesky" -nodeType "mia_photometric_light"
		 -nodeType "mib_texture_vector" -nodeType "mib_texture_remap" -nodeType "mib_texture_rotate"
		 -nodeType "mib_bump_basis" -nodeType "mib_bump_map" -nodeType "mib_passthrough_bump_map"
		 -nodeType "mib_bump_map2" -nodeType "mib_lookup_spherical" -nodeType "mib_lookup_cube1"
		 -nodeType "mib_lookup_cube6" -nodeType "mib_lookup_background" -nodeType "mib_lookup_cylindrical"
		 -nodeType "mib_texture_lookup" -nodeType "mib_texture_lookup2" -nodeType "mib_texture_filter_lookup"
		 -nodeType "mib_texture_checkerboard" -nodeType "mib_texture_polkadot" -nodeType "mib_texture_polkasphere"
		 -nodeType "mib_texture_turbulence" -nodeType "mib_texture_wave" -nodeType "mib_reflect"
		 -nodeType "mib_refract" -nodeType "mib_transparency" -nodeType "mib_continue" -nodeType "mib_opacity"
		 -nodeType "mib_twosided" -nodeType "mib_refraction_index" -nodeType "mib_dielectric"
		 -nodeType "mib_ray_marcher" -nodeType "mib_illum_lambert" -nodeType "mib_illum_phong"
		 -nodeType "mib_illum_ward" -nodeType "mib_illum_ward_deriv" -nodeType "mib_illum_blinn"
		 -nodeType "mib_illum_cooktorr" -nodeType "mib_illum_hair" -nodeType "mib_volume"
		 -nodeType "mib_color_alpha" -nodeType "mib_color_average" -nodeType "mib_color_intensity"
		 -nodeType "mib_color_interpolate" -nodeType "mib_color_mix" -nodeType "mib_color_spread"
		 -nodeType "mib_geo_cube" -nodeType "mib_geo_torus" -nodeType "mib_geo_sphere" -nodeType "mib_geo_cone"
		 -nodeType "mib_geo_cylinder" -nodeType "mib_geo_square" -nodeType "mib_geo_instance"
		 -nodeType "mib_geo_instance_mlist" -nodeType "mib_geo_add_uv_texsurf" -nodeType "mib_photon_basic"
		 -nodeType "mib_light_infinite" -nodeType "mib_light_point" -nodeType "mib_light_spot"
		 -nodeType "mib_light_photometric" -nodeType "mib_cie_d" -nodeType "mib_blackbody"
		 -nodeType "mib_shadow_transparency" -nodeType "mib_lens_stencil" -nodeType "mib_lens_clamp"
		 -nodeType "mib_lightmap_write" -nodeType "mib_lightmap_sample" -nodeType "mib_amb_occlusion"
		 -nodeType "mib_fast_occlusion" -nodeType "mib_map_get_scalar" -nodeType "mib_map_get_integer"
		 -nodeType "mib_map_get_vector" -nodeType "mib_map_get_color" -nodeType "mib_map_get_transform"
		 -nodeType "mib_map_get_scalar_array" -nodeType "mib_map_get_integer_array" -nodeType "mib_fg_occlusion"
		 -nodeType "mib_bent_normal_env" -nodeType "mib_glossy_reflection" -nodeType "mib_glossy_refraction"
		 -nodeType "builtin_bsdf_architectural" -nodeType "builtin_bsdf_architectural_comp"
		 -nodeType "builtin_bsdf_carpaint" -nodeType "builtin_bsdf_ashikhmin" -nodeType "builtin_bsdf_lambert"
		 -nodeType "builtin_bsdf_mirror" -nodeType "builtin_bsdf_phong" -nodeType "contour_store_function"
		 -nodeType "contour_store_function_simple" -nodeType "contour_contrast_function_levels"
		 -nodeType "contour_contrast_function_simple" -nodeType "contour_shader_simple" -nodeType "contour_shader_silhouette"
		 -nodeType "contour_shader_maxcolor" -nodeType "contour_shader_curvature" -nodeType "contour_shader_factorcolor"
		 -nodeType "contour_shader_depthfade" -nodeType "contour_shader_framefade" -nodeType "contour_shader_layerthinner"
		 -nodeType "contour_shader_widthfromcolor" -nodeType "contour_shader_widthfromlightdir"
		 -nodeType "contour_shader_widthfromlight" -nodeType "contour_shader_combi" -nodeType "contour_only"
		 -nodeType "contour_composite" -nodeType "contour_ps" -nodeType "mi_metallic_paint"
		 -nodeType "mi_metallic_paint_x" -nodeType "mi_bump_flakes" -nodeType "mi_car_paint_phen"
		 -nodeType "mi_metallic_paint_output_mixer" -nodeType "mi_car_paint_phen_x" -nodeType "physical_lens_dof"
		 -nodeType "physical_light" -nodeType "dgs_material" -nodeType "dgs_material_photon"
		 -nodeType "dielectric_material" -nodeType "dielectric_material_photon" -nodeType "oversampling_lens"
		 -nodeType "path_material" -nodeType "parti_volume" -nodeType "parti_volume_photon"
		 -nodeType "transmat" -nodeType "transmat_photon" -nodeType "mip_rayswitch" -nodeType "mip_rayswitch_advanced"
		 -nodeType "mip_rayswitch_environment" -nodeType "mip_card_opacity" -nodeType "mip_motionblur"
		 -nodeType "mip_motion_vector" -nodeType "mip_matteshadow" -nodeType "mip_cameramap"
		 -nodeType "mip_mirrorball" -nodeType "mip_grayball" -nodeType "mip_gamma_gain" -nodeType "mip_render_subset"
		 -nodeType "mip_matteshadow_mtl" -nodeType "mip_binaryproxy" -nodeType "mip_rayswitch_stage"
		 -nodeType "mip_fgshooter" -nodeType "mib_ptex_lookup" -nodeType "rnk_ao" -nodeType "rnk_assembly"
		 -nodeType "rnk_scalar_attribute" -nodeType "rnk_color_attribute" -nodeType "rnk_vector_attribute"
		 -nodeType "rnk_integer_attribute" -nodeType "rnk_matrix_attribute" -nodeType "rnk_brownian"
		 -nodeType "rnk_cellnoise" -nodeType "rnk_distort" -nodeType "rnk_worley" -nodeType "rnk_bump2d"
		 -nodeType "rnk_clip_lens" -nodeType "rnk_color_to_float" -nodeType "rnk_core3" -nodeType "rnk_diffuse"
		 -nodeType "rnk_displacement" -nodeType "rnk_displacement2" -nodeType "rnk_displacement_blender"
		 -nodeType "rnk_distributor_sampler_info" -nodeType "rnk_eyeball_base" -nodeType "rnk_eyeball"
		 -nodeType "rnk_eyeball2" -nodeType "rnk_eyeball3" -nodeType "rnk_eyeball4" -nodeType "rnk_fakefur"
		 -nodeType "rnk_scalar_fb_writer" -nodeType "rnk_color_fb_writer" -nodeType "rnk_vector_fb_writer"
		 -nodeType "rnk_fg" -nodeType "rnk_file" -nodeType "rnk_framebuffer" -nodeType "rnk_fur_sampler_info"
		 -nodeType "rnk_geomcache" -nodeType "rnk_hair" -nodeType "rnk_hair2" -nodeType "rnk_hair3"
		 -nodeType "rnk_hair_geo" -nodeType "rnk_hair_uv" -nodeType "rnk_indirect" -nodeType "rnk_indirect_translucency"
		 -nodeType "rnk_layered" -nodeType "rnk_layered_color" -nodeType "rnk_lens" -nodeType "rnk_light"
		 -nodeType "rnk_light_indirect" -nodeType "rnk_boolean_logic" -nodeType "rnk_mayabase"
		 -nodeType "rnk_mix" -nodeType "rnk_multitexture" -nodeType "rnk_multitexture2" -nodeType "normalDeriv"
		 -nodeType "rnk_normal_blender" -nodeType "rnk_normals" -nodeType "rnk_nullgeo" -nodeType "rnk_nullsurf"
		 -nodeType "rnk_obj_data" -nodeType "rnk_obj_color" -nodeType "rnk_particle" -nodeType "rnk_particle_sampler_info"
		 -nodeType "rnk_place2dtex" -nodeType "rnk_planar_cut" -nodeType "rnk_projected_eye_base"
		 -nodeType "rnk_projected_eye" -nodeType "rnk_projection" -nodeType "rnk_ray_distance"
		 -nodeType "rnk_reflection" -nodeType "rnk_reflection2" -nodeType "rnk_reflection3"
		 -nodeType "rnk_refraction" -nodeType "rnk_refraction2" -nodeType "rnk_rim" -nodeType "rnk_root"
		 -nodeType "rnk_rotblur" -nodeType "rnk_scalar_selector" -nodeType "rnk_color_selector"
		 -nodeType "rnk_boolean_selector" -nodeType "rnk_shadow" -nodeType "rnk_shave_color"
		 -nodeType "rnk_sparkles" -nodeType "rnk_specular" -nodeType "rnk_specular2" -nodeType "rnk_geomcache_data"
		 -nodeType "rnk_single_scalar_data" -nodeType "rnk_single_color_data" -nodeType "rnk_single_vector_data"
		 -nodeType "rnk_single_integer_data" -nodeType "rnk_single_boolean_data" -nodeType "rnk_single_string_data"
		 -nodeType "rnk_single_matrix_data" -nodeType "rnk_single_scalar_array_data" -nodeType "rnk_single_string_array_data"
		 -nodeType "rnk_particle_sampler_data" -nodeType "rnk_distributor_sampler_data" -nodeType "rnk_struct_adapter"
		 -nodeType "rnk_transition" -nodeType "rnk_translucency" -nodeType "rnk_traversal"
		 -nodeType "rnk_uvchooser" -nodeType "rnk_vertex_data" -nodeType "rnk_wireframe" -nodeType "misss_physical"
		 -nodeType "misss_physical_phen" -nodeType "misss_fast_shader" -nodeType "misss_fast_shader_x"
		 -nodeType "misss_skin_specular" -nodeType "misss_lightmap_write" -nodeType "misss_lambert_gamma"
		 -nodeType "misss_call_shader" -nodeType "misss_fast_simple_phen" -nodeType "misss_fast_skin_phen"
		 -nodeType "misss_fast_skin_phen_d" -nodeType "surfaceSampler" -nodeType "mib_data_bool"
		 -nodeType "mib_data_int" -nodeType "mib_data_scalar" -nodeType "mib_data_vector"
		 -nodeType "mib_data_color" -nodeType "mib_data_string" -nodeType "mib_data_texture"
		 -nodeType "mib_data_shader" -nodeType "mib_data_bool_array" -nodeType "mib_data_int_array"
		 -nodeType "mib_data_scalar_array" -nodeType "mib_data_vector_array" -nodeType "mib_data_color_array"
		 -nodeType "mib_data_string_array" -nodeType "mib_data_texture_array" -nodeType "mib_data_shader_array"
		 -nodeType "mib_data_get_bool" -nodeType "mib_data_get_int" -nodeType "mib_data_get_scalar"
		 -nodeType "mib_data_get_vector" -nodeType "mib_data_get_color" -nodeType "mib_data_get_string"
		 -nodeType "mib_data_get_texture" -nodeType "mib_data_get_shader" -nodeType "mib_data_get_shader_bool"
		 -nodeType "mib_data_get_shader_int" -nodeType "mib_data_get_shader_scalar" -nodeType "mib_data_get_shader_vector"
		 -nodeType "mib_data_get_shader_color" -nodeType "user_ibl_env" -nodeType "user_ibl_rect"
		 -nodeType "mia_material_x_passes" -nodeType "mi_metallic_paint_x_passes" -nodeType "mi_car_paint_phen_x_passes"
		 -nodeType "misss_fast_shader_x_passes" -nodeType "rnk_desaturate" -nodeType "rnk_hair_color_variation"
		 -nodeType "rnk_hair_scalar_variation" -nodeType "rnk_skin" -nodeType "rnk_skin2"
		 -nodeType "rnk_skin3" -nodeType "rnk_skin4" -nodeType "rnk_skin5" -nodeType "rnk_subsurface_lightmap"
		 -nodeType "rnk_subsurface" -nodeType "rnk_surface" -nodeType "rnk_surface2" -dataType "byteArray"
		 "Mayatomr" "2014.0 - 3.11.1.4 ";
requires "spMapInfoShader" "$Rev: 65400 $";
requires "spCmptAsmbNd" "1.0";
requires "shaveNode" "1.1";
requires "rivetConstraint" "1.0";
requires "pointToPoint" "1.5";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2014";
fileInfo "version" "2014";
fileInfo "cutIdentifier" "201310082342-890429";
fileInfo "osv" "Linux 2.6.32-358.6.2.el6.x86_64 #1 SMP Thu May 16 20:59:36 UTC 2013 x86_64";
createNode transform -n "faceLoc_grp";
createNode transform -n "headSkelPos" -p "faceLoc_grp";
	setAttr ".t" -type "double3" 0 44.06746926008659 2.7937704789850493 ;
createNode locator -n "headSkelPosShape" -p "headSkelPos";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
createNode nurbsCurve -n "headSkelPosTitleShape" -p "headSkelPos";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		2 23 0 no 3
		26 0 0 1 1 2 2 3 3 4 4 5
		 5 6 6 7 7 8 8 9 9 10 10 11
		 11 12 12
		25
		0 0.048818431621130129 0.15908254957945972
		0 0.33363104588083403 0.15908254957945978
		0 0.6184436601403942 0.15908254957945983
		0 0.6184436601403942 0.23063190972576825
		0 0.61844366014039409 0.30218126987206595
		0 0.51412007695932893 0.30218126987206595
		0 0.40979649377840766 0.30218126987206595
		0 0.40979649377840766 0.39934991703844325
		0 0.40979649377840766 0.49651856420482599
		0 0.51412007695932893 0.49651856420482599
		0 0.61844366014039409 0.4965185642048261
		0 0.61844366014039409 0.56806792435097464
		0 0.61844366014039409 0.63961728449725652
		0 0.33363104588083392 0.63961728449725641
		0 0.048818431621130018 0.63961728449725641
		0 0.048818431621130039 0.56806792435097453
		0 0.04881843162113006 0.49651856420482599
		0 0.17506843162123106 0.49651856420482599
		0 0.30131843162117999 0.49651856420482599
		0 0.30131843162117999 0.39934991703844325
		0 0.30131843162118005 0.30218126987206595
		0 0.17506843162123109 0.30218126987206595
		0 0.048818431621130101 0.30218126987206584
		0 0.048818431621130115 0.23063190972576814
		0 0.048818431621130129 0.15908254957945972
		;
createNode transform -n "lEarPos" -p "faceLoc_grp";
	setAttr ".t" -type "double3" 5.5580707224992851 48.282535552978516 3.924226166506549 ;
createNode locator -n "lEarPosShape" -p "lEarPos";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
createNode nurbsCurve -n "lEarPosTitleShape" -p "lEarPos";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		2 11 0 no 3
		14 0 0 1 1 2 2 3 3 4 4 5
		 5 6 6
		13
		0 -0.68079068406605558 -0.52649696058336892
		0 -0.62561639372144606 -0.52649696058336892
		0 -0.57044210337668244 -0.52649696058336892
		0 -0.57044210337668244 -0.4060526586819968
		0 -0.57044210337668244 -0.28560835678062901
		0 -0.33589267335819045 -0.28560835678062901
		0 -0.10134324333969304 -0.28560835678062901
		0 -0.10134324333969304 -0.21282525036849087
		0 -0.10134324333969304 -0.14004214395635484
		0 -0.39106696370295341 -0.14004214395635484
		0 -0.68079068406605558 -0.14004214395635484
		0 -0.68079068406605558 -0.33326955226986082
		0 -0.68079068406605558 -0.52649696058336892
		;
createNode transform -n "nosePos" -p "faceLoc_grp";
	setAttr ".t" -type "double3" 0 47.891735076904297 9.0105248203115877 ;
createNode locator -n "nosePosShape" -p "nosePos";
	setAttr -k off ".v";
createNode nurbsCurve -n "nosePosTitleShape" -p "nosePos";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8
		 9 10
		11
		4.7982373409884756e-17 0.78361162489122382 -0.78361162489122504
		-7.7417092079760399e-33 1.1081941875543879 1.2643170607829326e-16
		-4.7982373409884713e-17 0.78361162489122427 0.78361162489122427
		-6.7857323231109134e-17 3.2112695072372299e-16 1.1081941875543879
		-4.7982373409884725e-17 -0.78361162489122405 0.78361162489122449
		-2.0446735801084019e-32 -1.1081941875543881 3.3392053635905195e-16
		4.7982373409884682e-17 -0.78361162489122438 -0.78361162489122382
		6.7857323231109134e-17 -5.9521325992805852e-16 -1.1081941875543879
		4.7982373409884756e-17 0.78361162489122382 -0.78361162489122504
		-7.7417092079760399e-33 1.1081941875543879 1.2643170607829326e-16
		-4.7982373409884713e-17 0.78361162489122427 0.78361162489122427
		;
createNode transform -n "JawRigPos" -p "faceLoc_grp";
	setAttr ".t" -type "double3" -0.0098188164028004624 45.464587496391118 3.7013931329565519 ;
createNode locator -n "JawRigPosShape" -p "JawRigPos";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
createNode nurbsCurve -n "JawRigPosTitleShape" -p "JawRigPos";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		2 37 0 no 3
		40 0 0 1 1 2 2 3 3 4 4 5
		 5 6 6 7 7 8 8 9 9 10 10 11
		 11 12 12 13 13 14 14 15 15 16 16 17
		 17 18 18 19 19
		39
		0 0.25660958506949266 -0.45507140571491878
		0 0.4598996836825528 -0.45507140571491878
		0 0.66318978229561276 -0.45507140571491878
		0 0.66318978229561276 -0.31702578771599921
		0 0.66318978229561276 -0.17898016971708319
		0 0.61095630521492295 -0.17898016971708319
		0 0.55872282813423935 -0.17898016971708319
		0 0.55872282813424023 -0.24473838639908774
		0 0.55872282813424023 -0.31049660308095728
		0 0.44329252767434241 -0.31049660308095728
		0 0.32786222721443214 -0.31049660308095728
		0 0.29731497052885336 -0.31049660308095728
		0 0.27237144485262843 -0.30953107075480712
		0 0.24742791917640364 -0.30856553842884704
		0 0.22848162447638401 -0.29968992806558514
		0 0.20914911684593396 -0.29120053063263374
		0 0.19832058072122838 -0.2705563564459732
		0 0.18749204459651303 -0.24991218225943346
		0 0.18749204459651303 -0.21170625029313417
		0 0.18749204459651303 -0.18198971575980405
		0 0.19354028482768471 -0.16308349976010117
		0 0.19958852505884395 -0.14417728376037164
		0 0.20661322817070371 -0.1268122759641388
		0 0.20661322817070371 -0.12025029966518286
		0 0.20661322817070371 -0.11368832336618784
		0 0.14831693678600569 -0.11368832336618784
		0 0.090020645401312049 -0.11368832336618784
		0 0.084227451444963575 -0.13917837677415523
		0 0.081257984102553249 -0.17277525820278949
		0 0.078827757455450009 -0.20637213963146639
		0 0.078827757455450009 -0.24459993270704583
		0 0.078827757455450009 -0.29596625245333552
		0 0.091193858265430028 -0.33535632783836622
		0 0.1035599590754136 -0.37474640322324948
		0 0.12984429945348466 -0.40371237300497409
		0 0.15303164935174085 -0.42958135230710415
		0 0.18607471601222347 -0.44232637901092975
		0 0.21911778267270968 -0.45507140571491878
		0 0.25660958506949266 -0.45507140571491878
		;
createNode transform -n "lipZPos" -p "JawRigPos";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
createNode locator -n "lipZPosShape" -p "lipZPos";
	setAttr -k off ".v";
createNode nurbsCurve -n "lipZPosTitleShape" -p "lipZPos";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		2 19 0 no 3
		22 0 0 1 1 2 2 3 3 4 4 5
		 5 6 6 7 7 8 8 9 9 10 10
		21
		0 0.078928664813554816 0.58872398453197772
		0 0.078928664813554927 0.35214331858193171
		0 0.078928664813555066 0.1155626526318863
		0 0.14138802393923061 0.11556265263188631
		0 0.20384738306503719 0.11556265263188632
		0 0.20384738306503714 0.25109267529165519
		0 0.20384738306503714 0.38662269795142423
		0 0.2907980390386935 0.25109267529165519
		0 0.37774869501232966 0.11556265263188636
		0 0.4616232827252425 0.11556265263188638
		0 0.54549787043815556 0.11556265263188641
		0 0.54549787043815545 0.35214331858193182
		0 0.54549787043815545 0.58872398453197794
		0 0.48303851131233899 0.58872398453197794
		0 0.42057915218667319 0.58872398453197783
		0 0.42057915218667319 0.42380111475027477
		0 0.4205791521866733 0.25887824496857204
		0 0.31550659182886881 0.42380111475027471
		0 0.21043403147106418 0.58872398453197772
		0 0.1446813481423096 0.58872398453197772
		0 0.078928664813554816 0.58872398453197772
		;
createNode transform -n "lipYPos" -p "lipZPos";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".t" -type "double3" 0 0 2.11851161356579 ;
createNode locator -n "lipYPosShape" -p "lipYPos";
	setAttr -k off ".v";
createNode nurbsCurve -n "lipYTitle1Shape" -p "lipYPos";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		2 17 0 no 3
		20 0 0 1 1 2 2 3 3 4 4 5
		 5 6 6 7 7 8 8 9 9
		19
		0 0.6566890333488612 0.090417021955447652
		0 0.6566890333488612 0.17001592315254221
		0 0.6566890333488612 0.24961482434960836
		0 0.5541947590624311 0.30388035182628226
		0 0.45170048477585772 0.35814587930291086
		0 0.5541947590624311 0.41433269682906371
		0 0.6566890333488612 0.47051951435519879
		0 0.6566890333488612 0.55270924607352256
		0 0.6566890333488612 0.63489897779184368
		0 0.48569058013952759 0.53406036065020412
		0 0.31469212693019832 0.43322174350854237
		0 0.19831216546802999 0.43322174350854237
		0 0.081932204005702919 0.43322174350854237
		0 0.081932204005702919 0.36102781437713283
		0 0.081932204005702919 0.28883388524570552
		0 0.20198008283509933 0.28883388524570552
		0 0.3220279616644966 0.28883388524570552
		0 0.48935849750676275 0.18962545360058236
		0 0.6566890333488612 0.090417021955447652
		;
createNode transform -n "lipNPos" -p "lipYPos";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".t" -type "double3" 0 0.25934816652515019 3.9635317783103208 ;
createNode locator -n "lipNPosShape" -p "lipNPos";
	setAttr -k off ".v";
	setAttr ".ovc" 7;
createNode nurbsCurve -n "lipNTitleShape" -p "lipNPos";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		2 19 0 no 3
		22 0 0 1 1 2 2 3 3 4 4 5
		 5 6 6 7 7 8 8 9 9 10 10
		21
		0 0.091670640606031098 0.10496909333506635
		8.7071013884502477e-13 0.37954000296995061 0.10496909333506643
		8.7071013884502477e-13 0.66740936533386941 0.10496909333506652
		8.7071013884502477e-13 0.66740936533386941 0.1709877558544744
		8.7071013884502477e-13 0.66740936533386941 0.23700641837402087
		8.7071013884502477e-13 0.50249757489841063 0.23700641837402078
		8.7071013884502477e-13 0.33758578446295157 0.23700641837402078
		8.7071013884502477e-13 0.50249757489841063 0.32891203656993717
		8.7071013884502477e-13 0.66740936533386941 0.42081765476583227
		8.7071013884502477e-13 0.66740936533386941 0.50947191215312948
		8.7071013884502477e-13 0.66740936533386941 0.59812616954042674
		8.7071013884502477e-13 0.37954000296995027 0.59812616954042674
		0 0.091670640606030765 0.59812616954042674
		0 0.091670640606030765 0.53210750702086962
		0 0.091670640606031098 0.46608884450147242
		8.7071013884502477e-13 0.29234739993729092 0.46608884450147242
		8.7071013884502477e-13 0.49302415926855059 0.46608884450147242
		8.7071013884502477e-13 0.29234739993729092 0.35502862871612528
		0 0.091670640606031098 0.24396841293077809
		0 0.091670640606031098 0.17446875313292226
		0 0.091670640606031098 0.10496909333506635
		;
createNode transform -n "lipEPos" -p "lipYPos";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".t" -type "double3" 2.7929023630976273 -0.45692472333811196 2.9661941115430204 ;
createNode locator -n "lipEPosShape" -p "lipEPos";
	setAttr -k off ".v";
	setAttr ".ovc" 7;
createNode nurbsCurve -n "lipETitleShape" -p "lipEPos";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		2 23 0 no 3
		26 0 0 1 1 2 2 3 3 4 4 5
		 5 6 6 7 7 8 8 9 9 10 10 11
		 11 12 12
		25
		0 0.094191602857673529 0.48480994102814473
		0 0.094191602857673862 0.2902531758647926
		0 0.094191602857673862 0.095696410701440984
		0 0.14901275371303932 0.095696410701440984
		0 0.20383390456840472 0.095696410701440984
		0 0.20383390456840472 0.21840247602029234
		0 0.20383390456840472 0.34110854133914437
		0 0.27661773038488924 0.34110854133914437
		0 0.34940155620137503 0.34110854133914437
		0 0.34940155620137536 0.22796701723333396
		0 0.34940155620137536 0.11482549312769477
		0 0.40422270705674046 0.11482549312769477
		0 0.45904385791210622 0.11482549312769477
		0 0.45904385791210622 0.22796701723333396
		0 0.45904385791210622 0.34110854133914437
		0 0.5096659418934435 0.34110854133914437
		0 0.56028802587478088 0.34110854133914437
		0 0.56028802587478088 0.21840247602029234
		0 0.56028802587478088 0.095696410701440984
		0 0.61510917673014631 0.095696410701440984
		0 0.66993032758551174 0.095696410701440984
		0 0.66993032758551208 0.2902531758647926
		0 0.66993032758551208 0.48480994102814473
		0 0.38206096522159305 0.48480994102814473
		0 0.094191602857673529 0.48480994102814473
		;
createNode transform -n "lipSPos" -p "lipYPos";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".t" -type "double3" 0 -0.5829130710676651 3.9611537036395053 ;
createNode locator -n "lipSPosShape" -p "lipSPos";
	setAttr -k off ".v";
	setAttr ".ovc" 7;
createNode nurbsCurve -n "lipSTitleShape" -p "lipSPos";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".cc" -type "nurbsCurve" 
		2 71 0 no 3
		74 0 0 1 1 2 2 3 3 4 4 5
		 5 6 6 7 7 8 8 9 9 10 10 11
		 11 12 12 13 13 14 14 15 15 16 16 17
		 17 18 18 19 19 20 20 21 21 22 22 23
		 23 24 24 25 25 26 26 27 27 28 28 29
		 29 30 30 31 31 32 32 33 33 34 34 35
		 35 36 36
		73
		0 0.096972078887985091 0.35172956447741621
		0 0.096972078887985091 0.24119907234682719
		0 0.14721704151575432 0.17626188161678077
		0 0.19746200414351245 0.11132469088689845
		0 0.28008955028721694 0.11132469088689845
		0 0.3377771708783448 0.11132469088689845
		0 0.37295075113043685 0.13941370332300179
		0 0.40812433138255066 0.16750271575910511
		0 0.42896377367988281 0.22516225084839342
		0 0.4393834948284927 0.25455372842803614
		0 0.44534113188692892 0.28040994347521736
		0 0.45129876894523013 0.3062661585222537
		0 0.45762502821399309 0.33416910450927928
		0 0.46767261646457792 0.37732247794566726
		0 0.48014257924073656 0.39239034963365232
		0 0.49261254201700844 0.40745822132162796
		0 0.51382411721252019 0.40745822132162796
		0 0.52828112923742188 0.40745822132162796
		0 0.5399541659017042 0.39797234310609514
		0 0.55162720256583686 0.38848646489058331
		0 0.55755324343474877 0.37546883483028892
		0 0.56496781589627387 0.35948116296000876
		0 0.56756221412026342 0.34497500130696557
		0 0.57015661234426984 0.33046883965391283
		0 0.57015661234426984 0.31224134901917588
		0 0.57015661234426984 0.26538068935201969
		0 0.55191507895875835 0.22093538283532416
		0 0.53367354557310076 0.17649007631847854
		0 0.50724508842792426 0.14561708852160121
		0 0.50724508842792426 0.13948040638961789
		0 0.50724508842792426 0.13334372425762447
		0 0.57061651243534639 0.13334372425762447
		0 0.63398793644292972 0.13334372425762447
		0 0.65113413526027575 0.17205958841771737
		0 0.66119927694933978 0.22101261796516453
		0 0.67126441863839403 0.26996564751248114
		0 0.67126441863839403 0.31947336571946894
		0 0.67126441863839403 0.41812369061053783
		0 0.623066186950477 0.48401578839995374
		0 0.57486795526257017 0.5499078861892378
		0 0.49707813679500434 0.5499078861892378
		0 0.43939051620386849 0.5499078861892378
		0 0.40105380631748 0.52200494020221089
		0 0.36271709643091565 0.49410199421531675
		0 0.34001698964279736 0.42974406695897144
		0 0.33034153429050939 0.40184112097194452
		0 0.32363963143575525 0.36966215734369634
		0 0.31693772858115521 0.33748319371558877
		0 0.30949507061778148 0.30920811483040889
		0 0.30354094424717593 0.28651502941768142
		0 0.29051278212366194 0.27014469258616752
		0 0.27748462000013596 0.25377435575465102
		0 0.25664517770280204 0.25377435575465102
		0 0.2379964045419114 0.25377435575465102
		0 0.2266182656460809 0.26381141194187352
		0 0.21524012675025039 0.2738484681292353
		0 0.20889982473056623 0.28834760840675505
		0 0.20330378850719866 0.30024883977273115
		0 0.20069183684458736 0.31976475280008232
		0 0.1980798851819694 0.33928066582743288
		0 0.1980798851819694 0.35118189719326576
		0 0.1980798851819694 0.3983936256322605
		0 0.21715696224455749 0.44858241725663012
		0 0.23623403930713405 0.49877120888099979
		0 0.27177624176969717 0.54041498659832343
		0 0.27177624176969717 0.54673422449169407
		0 0.27177624176969717 0.55305346238507436
		0 0.20580690885057162 0.55305346238507436
		0 0.13983757593143942 0.55305346238507436
		0 0.1215679570441015 0.51174671068867483
		0 0.10927001796597136 0.46355550037614979
		0 0.096972078887985091 0.41536429006376957
		0 0.096972078887985091 0.35172956447741621
		;
createNode transform -n "lEyePos" -p "faceLoc_grp";
	setAttr ".t" -type "double3" 2.0489927585411345 49.496798381109869 7.3070995857812626 ;
	setAttr ".r" -type "double3" 0 6.0000000000000053 0 ;
createNode locator -n "lEyePosShape" -p "lEyePos";
	setAttr -k off ".v";
createNode transform -n "lowCheekPos" -p "faceLoc_grp";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".t" -type "double3" 3.1856955863196363 43.866761987027289 8.418693704743891 ;
createNode locator -n "lowCheekPosShape" -p "lowCheekPos";
	setAttr -k off ".v";
	setAttr ".ovc" 7;
createNode transform -n "squintPuffPos" -p "faceLoc_grp";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".t" -type "double3" 3.8777474531450764 47.941495343458612 8.0303367199143683 ;
	setAttr ".r" -type "double3" 10 0 0 ;
	setAttr ".s" -type "double3" 1 0.99999999999999989 0.99999999999999989 ;
createNode locator -n "squintPuffPosShape" -p "squintPuffPos";
	setAttr -k off ".v";
	setAttr ".ovc" 7;
createNode transform -n "cheekPos" -p "faceLoc_grp";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".t" -type "double3" 3.4901811835971994 46.06458749639112 8.4199047465223416 ;
	setAttr ".r" -type "double3" 10 0 0 ;
	setAttr ".s" -type "double3" 1 0.99999999999999989 0.99999999999999989 ;
createNode locator -n "cheekPosShape" -p "cheekPos";
	setAttr -k off ".v";
	setAttr ".ovc" 7;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1;
	setAttr ".unw" 1;
lockNode -l 1 ;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 24 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
lockNode -l 1 ;
select -ne :initialShadingGroup;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 16 ".dsm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -cb on ".mimt";
	setAttr -cb on ".miop";
	setAttr -k on ".mico";
	setAttr -cb on ".mise";
	setAttr -cb on ".mism";
	setAttr -cb on ".mice";
	setAttr -av -cb on ".micc";
	setAttr -k on ".micr";
	setAttr -k on ".micg";
	setAttr -k on ".micb";
	setAttr -cb on ".mica";
	setAttr -av -cb on ".micw";
	setAttr -cb on ".mirw";
lockNode -l 1 ;
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -cb on ".mimt";
	setAttr -cb on ".miop";
	setAttr -k on ".mico";
	setAttr -cb on ".mise";
	setAttr -cb on ".mism";
	setAttr -cb on ".mice";
	setAttr -av -cb on ".micc";
	setAttr -k on ".micr";
	setAttr -k on ".micg";
	setAttr -k on ".micb";
	setAttr -cb on ".mica";
	setAttr -av -cb on ".micw";
	setAttr -cb on ".mirw";
lockNode -l 1 ;
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 24 ".s";
lockNode -l 1 ;
select -ne :defaultTextureList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 9 ".tx";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
lockNode -l 1 ;
select -ne :defaultRenderUtilityList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 539 ".u";
select -ne :defaultRenderingList1;
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
lockNode -l 1 ;
select -ne :defaultRenderGlobals;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".macc";
	setAttr -k on ".macd";
	setAttr -k on ".macq";
	setAttr -k on ".mcfr";
	setAttr -k on ".ifg";
	setAttr -k on ".clip";
	setAttr -k on ".edm";
	setAttr -k on ".edl";
	setAttr -k on ".ren";
	setAttr -av -k on ".esr";
	setAttr -k on ".ors";
	setAttr -k on ".sdf";
	setAttr -k on ".outf";
	setAttr -k on ".imfkey";
	setAttr -k on ".gama";
	setAttr -k on ".an";
	setAttr -k on ".ar";
	setAttr -k on ".fs";
	setAttr -k on ".ef";
	setAttr -av -k on ".bfs";
	setAttr -k on ".me";
	setAttr -k on ".se";
	setAttr -k on ".be";
	setAttr -k on ".ep" 1;
	setAttr -k on ".fec";
	setAttr -k on ".ofc";
	setAttr -k on ".ofe";
	setAttr -k on ".efe";
	setAttr -k on ".oft";
	setAttr -k on ".umfn";
	setAttr -k on ".ufe";
	setAttr -k on ".pff";
	setAttr -k on ".peie";
	setAttr -k on ".ifp";
	setAttr -k on ".comp";
	setAttr -k on ".cth";
	setAttr -k on ".soll";
	setAttr -k on ".rd";
	setAttr -k on ".lp";
	setAttr -k on ".sp";
	setAttr -k on ".shs";
	setAttr -k on ".lpr";
	setAttr -k on ".gv";
	setAttr -k on ".sv";
	setAttr -k on ".mm";
	setAttr -k on ".npu";
	setAttr -k on ".itf";
	setAttr -k on ".shp";
	setAttr -k on ".isp";
	setAttr -k on ".uf";
	setAttr -k on ".oi";
	setAttr -k on ".rut";
	setAttr -k on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -k on ".afp";
	setAttr -k on ".pfb";
	setAttr -k on ".pram";
	setAttr -k on ".poam";
	setAttr -k on ".prlm";
	setAttr -k on ".polm";
	setAttr -k on ".prm";
	setAttr -k on ".pom";
	setAttr -k on ".pfrm";
	setAttr -k on ".pfom";
	setAttr -av -k on ".bll";
	setAttr -k on ".bls";
	setAttr -k on ".smv";
	setAttr -k on ".ubc";
	setAttr -k on ".mbc";
	setAttr -k on ".mbt";
	setAttr -k on ".udbx";
	setAttr -k on ".smc";
	setAttr -k on ".kmv";
	setAttr -k on ".isl";
	setAttr -k on ".ism";
	setAttr -k on ".imb";
	setAttr -k on ".rlen";
	setAttr -av -k on ".frts";
	setAttr -k on ".tlwd";
	setAttr -k on ".tlht";
	setAttr -k on ".jfc";
	setAttr -k on ".rsb";
	setAttr -k on ".ope";
	setAttr -k on ".oppf";
	setAttr -k on ".hbl" -type "string" "Face";
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w" 640;
	setAttr -av -k on ".h" 480;
	setAttr -av -k on ".pa";
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar" 1.3333332538604736;
	setAttr -av -k on ".ldar";
	setAttr -cb on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -cb on ".isu";
	setAttr -cb on ".pdu";
select -ne :defaultLightSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr -k on ".ro" yes;
lockNode -l 1 ;
select -ne :defaultObjectSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr ".ro" yes;
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k off -cb on ".ctrs" 256;
	setAttr -av -k off -cb on ".btrs" 512;
	setAttr -k off -cb on ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off -cb on ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -cb on ".hwcc";
	setAttr -cb on ".hwdp";
	setAttr -cb on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
select -ne :hardwareRenderingGlobals;
	setAttr ".cons" no;
	setAttr ".vac" 2;
select -ne :defaultHardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".rp";
	setAttr -k on ".cai";
	setAttr -k on ".coi";
	setAttr -cb on ".bc";
	setAttr -av -k on ".bcb";
	setAttr -av -k on ".bcg";
	setAttr -av -k on ".bcr";
	setAttr -k on ".ei";
	setAttr -av -k on ".ex";
	setAttr -av -k on ".es";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bf";
	setAttr -k on ".fii";
	setAttr -av -k on ".sf";
	setAttr -k on ".gr";
	setAttr -k on ".li";
	setAttr -k on ".ls";
	setAttr -av -k on ".mb";
	setAttr -k on ".ti";
	setAttr -k on ".txt";
	setAttr -k on ".mpr";
	setAttr -k on ".wzd";
	setAttr -k on ".fn" -type "string" "im";
	setAttr -k on ".if";
	setAttr -k on ".res" -type "string" "ntsc_4d 646 485 1.333";
	setAttr -k on ".as";
	setAttr -k on ".ds";
	setAttr -k on ".lm";
	setAttr -av -k on ".fir";
	setAttr -k on ".aap";
	setAttr -av -k on ".gh";
	setAttr -cb on ".sd";
lockNode -l 1 ;
select -ne :ikSystem;
	setAttr -s 4 ".sol";
dataStructure -fmt "raw" -as "name=externalContentTable:string=node:string=key:string=upath:uint32=upathcrc:string=rpath:string=roles";
applyMetadata -fmt "raw" -v "channel\nname externalContentTable\nstream\nname v1.0\nindexType numeric\nstructure externalContentTable\n0\n\"barbie_face_blends_chr_barbiearrivaloutfit_eye_iris_col_1\" \"fileTextureName\" \"N:/projects/willows/wl01/production/show/seq_visdev_chars/shot_chr_barbiearrivaloutfit/textures/image_ref_modeling/chr_barbiearrivaloutfit_eye_iris_col.iff\" 3192082429 \"N:/projects/willows/wl01/production/show/seq_visdev_chars/shot_chr_barbiearrivaloutfit/textures/image_ref_modeling/chr_barbiearrivaloutfit_eye_iris_col.iff\" \"sourceImages\"\n1\n\"barbie_face_blends_chr_barbiearrivaloutfit_eyebrow_msk_1\" \"fileTextureName\" \"N:/projects/willows/wl01/production/show/seq_visdev_chars/shot_chr_barbiearrivaloutfit/textures/image_ref_modeling/chr_barbiearrivaloutfit_eyebrow_msk.iff\" 1377110761 \"N:/projects/willows/wl01/production/show/seq_visdev_chars/shot_chr_barbiearrivaloutfit/textures/image_ref_modeling/chr_barbiearrivaloutfit_eyebrow_msk.iff\" \"sourceImages\"\n2\n\"barbie_face_blends_file2\" \"fileTextureName\" \"N:/projects/willows/wl01/production/show/seq_visdev_chars/shot_chr_barbiearrivaloutfit/textures/image_ref_modeling/chr_barbiearrivaloutfit_eyelash.iff\" 901187428 \"N:/projects/willows/wl01/production/show/seq_visdev_chars/shot_chr_barbiearrivaloutfit/textures/image_ref_modeling/chr_barbiearrivaloutfit_eyelash.iff\" \"sourceImages\"\n3\n\"export_blends_WIP2_from_maya_2015_file_v01a_chr_barbiearrivaloutfit_dif_1\" \"fileTextureName\" \"N:/projects/willows/wl01/production/show/seq_visdev_chars/shot_chr_barbiearrivaloutfit/textures/image_ref_modeling/chr_barbiearrivaloutfit_dif.1011.iff\" 4132619127 \"N:/projects/willows/wl01/production/show/seq_visdev_chars/shot_chr_barbiearrivaloutfit/textures/image_ref_modeling/chr_barbiearrivaloutfit_dif.1011.iff\" \"sourceImages\"\n4\n\"chr_barbiearrivaloutfit_mouth_gums_anim_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_gums_anim.iff\" 1433964940 \"textures/chr_barbiearrivaloutfit_mouth_gums_anim.iff\" \"sourceImages\"\n5\n\"chr_barbiemaster_eye_anim_1\" \"fileTextureName\" \"textures/chr_barbiemaster_eye_anim.iff\" 3577487496 \"textures/chr_barbiemaster_eye_anim.iff\" \"sourceImages\"\n6\n\"chr_barbiearrivaloutfit_eyelash_textures0_anim\" \"fileTextureName\" \"textures/chr_staciearrivaloutfit_eyelashes_anim.iff\" 3045810879 \"textures/chr_staciearrivaloutfit_eyelashes_anim.iff\" \"sourceImages\"\n7\n\"chr_barbiearrivaloutfit_eye_iris_anim_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_iris_anim.iff\" 1984759383 \"textures/chr_barbiearrivaloutfit_eye_iris_anim.iff\" \"sourceImages\"\n8\n\"chr_barbiearrivaloutfit_mouth_teeth_anim_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_teeth_anim.iff\" 3933055359 \"textures/chr_barbiearrivaloutfit_mouth_teeth_anim.iff\" \"sourceImages\"\n9\n\"chr_barbiearrivaloutfit_jeans_anim_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_jeans_anim.iff\" 1025939743 \"textures/chr_barbiearrivaloutfit_jeans_anim.iff\" \"sourceImages\"\n10\n\"chr_barbiearrivaloutfit_top_anim_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_top_anim.iff\" 2033991545 \"textures/chr_barbiearrivaloutfit_top_anim.iff\" \"sourceImages\"\n11\n\"chr_barbiearrivaloutfit_face_body_amim_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_face_body_amim.iff\" 4013283389 \"textures/chr_barbiearrivaloutfit_face_body_amim.iff\" \"sourceImages\"\n12\n\"chr_barbiearrivaloutfit_shoe_anim_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_shoe_anim.iff\" 1735287608 \"textures/chr_barbiearrivaloutfit_shoe_anim.iff\" \"sourceImages\"\n13\n\"chr_barbiearrivaloutfit_mouth_tongue_anim_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_tongue_anim.iff\" 2439093177 \"textures/chr_barbiearrivaloutfit_mouth_tongue_anim.iff\" \"sourceImages\"\n14\n\"chr_barbiearrivaloutfit_eye_lashes_trn_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_lashes_trn.iff\" 3435516613 \"textures/chr_barbiearrivaloutfit_eye_lashes_trn.iff\" \"sourceImages\"\n15\n\"chr_barbiearrivaloutfit_eyes_col_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_sclera_col.iff\" 152223901 \"textures/chr_barbiearrivaloutfit_eye_sclera_col.iff\" \"sourceImages\"\n16\n\"chr_barbiearrivaloutfit_eyes_trn_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_sclera_trn.iff\" 1860378872 \"textures/chr_barbiearrivaloutfit_eye_sclera_trn.iff\" \"sourceImages\"\n17\n\"chr_barbiearrivaloutfit_eye_afb_scp_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_afb_scp.iff\" 1896790746 \"textures/chr_barbiearrivaloutfit_eye_afb_scp.iff\" \"sourceImages\"\n18\n\"chr_barbiearrivaloutfit_jeans_bmp_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_jeans01_bmp.1001.iff\" 445435058 \"textures/chr_barbiearrivaloutfit_jeans01_bmp.1001.iff\" \"sourceImages\"\n19\n\"chr_barbiearrivaloutfit_jeans_col_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_jeans01_col.1001.iff\" 3839318138 \"textures/chr_barbiearrivaloutfit_jeans01_col.1001.iff\" \"sourceImages\"\n20\n\"chr_barbiearrivaloutfit_tongue_col\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_tongue_col.iff\" 1506732257 \"textures/chr_barbiearrivaloutfit_mouth_tongue_col.iff\" \"sourceImages\"\n21\n\"chr_barbiearrivaloutfit_tongue_bmp\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_tongue_bmp.iff\" 392247517 \"textures/chr_barbiearrivaloutfit_mouth_tongue_bmp.iff\" \"sourceImages\"\n22\n\"chr_barbiearrivaloutfit_tongue_gls\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_tongue_gls.iff\" 3383082511 \"textures/chr_barbiearrivaloutfit_mouth_tongue_gls.iff\" \"sourceImages\"\n23\n\"chr_barbiearrivaloutfit_tongue_sss\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_tongue_sss.iff\" 2830415516 \"textures/chr_barbiearrivaloutfit_mouth_tongue_sss.iff\" \"sourceImages\"\n24\n\"chr_barbiearrivaloutfit_iris_col_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_iris_col.iff\" 3447587311 \"textures/chr_barbiearrivaloutfit_eye_iris_col.iff\" \"sourceImages\"\n25\n\"chr_barbiearrivaloutfit_iris_bmp_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_iris_bmp.iff\" 2211566035 \"textures/chr_barbiearrivaloutfit_eye_iris_bmp.iff\" \"sourceImages\"\n26\n\"chr_barbiearrivaloutfit_body_scalp_mesh_afb_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_scalp_mesh_afb.iff\" 4277534374 \"textures/chr_barbiearrivaloutfit_body_scalp_mesh_afb.iff\" \"sourceImages\"\n27\n\"chr_barbiearrivaloutfit_skin_col_1001_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1001.iff\" 2100974105 \"textures/chr_barbiearrivaloutfit_body_rev.col.1001.iff\" \"sourceImages\"\n28\n\"chr_barbiearrivaloutfit_skin_col_1002_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1002.iff\" 983181513 \"textures/chr_barbiearrivaloutfit_body_rev.col.1002.iff\" \"sourceImages\"\n29\n\"chr_barbiearrivaloutfit_skin_col_1003_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1003.iff\" 133824889 \"textures/chr_barbiearrivaloutfit_body_rev.col.1003.iff\" \"sourceImages\"\n30\n\"chr_barbiearrivaloutfit_skin_col_1004_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1004.iff\" 3051019625 \"textures/chr_barbiearrivaloutfit_body_rev.col.1004.iff\" \"sourceImages\"\n31\n\"chr_barbiearrivaloutfit_skin_col_1005_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1005.iff\" 2293953753 \"textures/chr_barbiearrivaloutfit_body_rev.col.1005.iff\" \"sourceImages\"\n32\n\"chr_barbiearrivaloutfit_skin_col_1006_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1006.iff\" 3474624009 \"textures/chr_barbiearrivaloutfit_body_rev.col.1006.iff\" \"sourceImages\"\n33\n\"chr_barbiearrivaloutfit_skin_gls_default\" \"fileTextureName\" \"textures/chr_chelseaarrivaloutfit_nose_lip_gls.iff\" 2680993943 \"textures/chr_chelseaarrivaloutfit_nose_lip_gls.iff\" \"sourceImages\"\n34\n\"chr_barbiearrivaloutfit_skin_bmp_1001_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1001.iff\" 1616521540 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1001.iff\" \"sourceImages\"\n35\n\"chr_barbiearrivaloutfit_skin_bmp_1002_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1002.iff\" 670716820 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1002.iff\" \"sourceImages\"\n36\n\"chr_barbiearrivaloutfit_skin_bmp_1003_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1003.iff\" 446331428 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1003.iff\" \"sourceImages\"\n37\n\"chr_barbiearrivaloutfit_skin_bmp_1004_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1004.iff\" 2830804532 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1004.iff\" \"sourceImages\"\n38\n\"chr_barbiearrivaloutfit_skin_bmp_1005_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1005.iff\" 2514128772 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1005.iff\" \"sourceImages\"\n39\n\"chr_barbiearrivaloutfit_skin_bmp_1006_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1006.iff\" 3531273556 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1006.iff\" \"sourceImages\"\n40\n\"chr_barbiearrivaloutfit_skin_col_1006_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1006.iff\" 4050668571 \"textures/chr_barbiearrivaloutfit_body_afb.1006.iff\" \"sourceImages\"\n41\n\"chr_barbiearrivaloutfit_skin_col_1005_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1005.iff\" 3067098827 \"textures/chr_barbiearrivaloutfit_body_afb.1005.iff\" \"sourceImages\"\n42\n\"chr_barbiearrivaloutfit_skin_col_1004_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1004.iff\" 2343575419 \"textures/chr_barbiearrivaloutfit_body_afb.1004.iff\" \"sourceImages\"\n43\n\"chr_barbiearrivaloutfit_skin_col_1003_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1003.iff\" 965788523 \"textures/chr_barbiearrivaloutfit_body_afb.1003.iff\" \"sourceImages\"\n44\n\"chr_barbiearrivaloutfit_skin_col_1002_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1002.iff\" 82897627 \"textures/chr_barbiearrivaloutfit_body_afb.1002.iff\" \"sourceImages\"\n45\n\"chr_barbiearrivaloutfit_skin_col_1001_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1001.iff\" 1129353227 \"textures/chr_barbiearrivaloutfit_body_afb.1001.iff\" \"sourceImages\"\n46\n\"chr_barbiearrivaloutfit_body_inside_mouth_afb_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_inside_mouth_afb.iff\" 1938877603 \"textures/chr_barbiearrivaloutfit_body_inside_mouth_afb.iff\" \"sourceImages\"\n47\n\"chr_barbiearrivaloutfit_body_scalp_mesh_afb_2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_scalp_mesh_afb.iff\" 4277534374 \"textures/chr_barbiearrivaloutfit_body_scalp_mesh_afb.iff\" \"sourceImages\"\n48\n\"chr_barbiearrivaloutfit_top_col_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_top_col.iff\" 3166575526 \"textures/chr_barbiearrivaloutfit_top_col.iff\" \"sourceImages\"\n49\n\"chr_barbiearrivaloutfit_top_bmp_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_top_bmp.iff\" 4061252506 \"textures/chr_barbiearrivaloutfit_top_bmp.iff\" \"sourceImages\"\n50\n\"chr_barbiearrivaloutfit_gums_col_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_gums_col.iff\" 562980120 \"textures/chr_barbiearrivaloutfit_mouth_gums_col.iff\" \"sourceImages\"\n51\n\"chr_barbiearrivaloutfit_gums_bmp_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_gums_bmp.iff\" 1864480036 \"textures/chr_barbiearrivaloutfit_mouth_gums_bmp.iff\" \"sourceImages\"\n52\n\"chr_barbiearrivaloutfit_gums_gls_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_gums_gls.iff\" 2984588278 \"textures/chr_barbiearrivaloutfit_mouth_gums_gls.iff\" \"sourceImages\"\n53\n\"chr_barbiearrivaloutfit_gums_sss_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_gums_sss.iff\" 3505666917 \"textures/chr_barbiearrivaloutfit_mouth_gums_sss.iff\" \"sourceImages\"\n54\n\"chr_barbiearrivaloutfit_shoe_stitch_msk_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_shoe_stitch_msk.iff\" 1724424304 \"textures/chr_barbiearrivaloutfit_shoe_stitch_msk.iff\" \"sourceImages\"\n55\n\"chr_barbiearrivaloutfit_shoe_col_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_shoe_col.iff\" 4010816052 \"textures/chr_barbiearrivaloutfit_shoe_col.iff\" \"sourceImages\"\n56\n\"chr_barbiearrivaloutfit_shoe_bmp_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_shoe_bmp.iff\" 2713707016 \"textures/chr_barbiearrivaloutfit_shoe_bmp.iff\" \"sourceImages\"\n57\n\"chr_barbiearrivaloutfit_shoe_gls_msk_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_shoe_gls_msk.iff\" 1054283300 \"textures/chr_barbiearrivaloutfit_shoe_gls_msk.iff\" \"sourceImages\"\n58\n\"chr_barbiearrivaloutfit_teeth_col_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_teeth_col.iff\" 3839328299 \"textures/chr_barbiearrivaloutfit_mouth_teeth_col.iff\" \"sourceImages\"\n59\n\"chr_barbiearrivaloutfit_teeth_bmp_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_teeth_bmp.iff\" 2860011543 \"textures/chr_barbiearrivaloutfit_mouth_teeth_bmp.iff\" \"sourceImages\"\n60\n\"chr_barbiearrivaloutfit_teeth_gls_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_teeth_gls.iff\" 1958532805 \"textures/chr_barbiearrivaloutfit_mouth_teeth_gls.iff\" \"sourceImages\"\n61\n\"chr_barbiearrivaloutfit_teeth_sss_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_teeth_sss.iff\" 363716182 \"textures/chr_barbiearrivaloutfit_mouth_teeth_sss.iff\" \"sourceImages\"\n62\n\"default_bin_chr_barbiearrivaloutfit_eye_lashes_trn_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_lashes_trn.iff\" 3435516613 \"textures/chr_barbiearrivaloutfit_eye_lashes_trn.iff\" \"sourceImages\"\n63\n\"default_bin_chr_barbiearrivaloutfit_eyes_col_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_sclera_col.iff\" 152223901 \"textures/chr_barbiearrivaloutfit_eye_sclera_col.iff\" \"sourceImages\"\n64\n\"default_bin_chr_barbiearrivaloutfit_eyes_trn_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_sclera_trn.iff\" 1860378872 \"textures/chr_barbiearrivaloutfit_eye_sclera_trn.iff\" \"sourceImages\"\n65\n\"default_bin_chr_barbiearrivaloutfit_eye_afb_scp_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_afb_scp.iff\" 1896790746 \"textures/chr_barbiearrivaloutfit_eye_afb_scp.iff\" \"sourceImages\"\n66\n\"default_bin_chr_barbiearrivaloutfit_jeans_bmp_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_jeans01_bmp.1001.iff\" 445435058 \"textures/chr_barbiearrivaloutfit_jeans01_bmp.1001.iff\" \"sourceImages\"\n67\n\"default_bin_chr_barbiearrivaloutfit_jeans_col_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_jeans01_col.1001.iff\" 3839318138 \"textures/chr_barbiearrivaloutfit_jeans01_col.1001.iff\" \"sourceImages\"\n68\n\"default_bin_chr_barbiearrivaloutfit_tongue_col\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_tongue_col.iff\" 1506732257 \"textures/chr_barbiearrivaloutfit_mouth_tongue_col.iff\" \"sourceImages\"\n69\n\"default_bin_chr_barbiearrivaloutfit_tongue_bmp\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_tongue_bmp.iff\" 392247517 \"textures/chr_barbiearrivaloutfit_mouth_tongue_bmp.iff\" \"sourceImages\"\n70\n\"default_bin_chr_barbiearrivaloutfit_tongue_gls\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_tongue_gls.iff\" 3383082511 \"textures/chr_barbiearrivaloutfit_mouth_tongue_gls.iff\" \"sourceImages\"\n71\n\"default_bin_chr_barbiearrivaloutfit_tongue_sss\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_tongue_sss.iff\" 2830415516 \"textures/chr_barbiearrivaloutfit_mouth_tongue_sss.iff\" \"sourceImages\"\n72\n\"default_bin_chr_barbiearrivaloutfit_iris_col_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_iris_col.iff\" 3447587311 \"textures/chr_barbiearrivaloutfit_eye_iris_col.iff\" \"sourceImages\"\n73\n\"default_bin_chr_barbiearrivaloutfit_iris_bmp_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_iris_bmp.iff\" 2211566035 \"textures/chr_barbiearrivaloutfit_eye_iris_bmp.iff\" \"sourceImages\"\n74\n\"default_bin_chr_barbiearrivaloutfit_body_scalp_mesh_afb_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_scalp_mesh_afb.iff\" 4277534374 \"textures/chr_barbiearrivaloutfit_body_scalp_mesh_afb.iff\" \"sourceImages\"\n75\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1001_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1001.iff\" 2100974105 \"textures/chr_barbiearrivaloutfit_body_rev.col.1001.iff\" \"sourceImages\"\n76\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1002_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1002.iff\" 983181513 \"textures/chr_barbiearrivaloutfit_body_rev.col.1002.iff\" \"sourceImages\"\n77\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1003_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1003.iff\" 133824889 \"textures/chr_barbiearrivaloutfit_body_rev.col.1003.iff\" \"sourceImages\"\n78\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1004_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1004.iff\" 3051019625 \"textures/chr_barbiearrivaloutfit_body_rev.col.1004.iff\" \"sourceImages\"\n79\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1005_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1005.iff\" 2293953753 \"textures/chr_barbiearrivaloutfit_body_rev.col.1005.iff\" \"sourceImages\"\n80\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1006_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1006.iff\" 3474624009 \"textures/chr_barbiearrivaloutfit_body_rev.col.1006.iff\" \"sourceImages\"\n81\n\"default_bin_chr_barbiearrivaloutfit_skin_gls_default\" \"fileTextureName\" \"textures/chr_chelseaarrivaloutfit_nose_lip_gls.iff\" 2680993943 \"textures/chr_chelseaarrivaloutfit_nose_lip_gls.iff\" \"sourceImages\"\n82\n\"default_bin_chr_barbiearrivaloutfit_skin_bmp_1001_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1001.iff\" 1616521540 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1001.iff\" \"sourceImages\"\n83\n\"default_bin_chr_barbiearrivaloutfit_skin_bmp_1002_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1002.iff\" 670716820 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1002.iff\" \"sourceImages\"\n84\n\"default_bin_chr_barbiearrivaloutfit_skin_bmp_1003_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1003.iff\" 446331428 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1003.iff\" \"sourceImages\"\n85\n\"default_bin_chr_barbiearrivaloutfit_skin_bmp_1004_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1004.iff\" 2830804532 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1004.iff\" \"sourceImages\"\n86\n\"default_bin_chr_barbiearrivaloutfit_skin_bmp_1005_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1005.iff\" 2514128772 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1005.iff\" \"sourceImages\"\n87\n\"default_bin_chr_barbiearrivaloutfit_skin_bmp_1006_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1006.iff\" 3531273556 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1006.iff\" \"sourceImages\"\n88\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1006_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1006.iff\" 4050668571 \"textures/chr_barbiearrivaloutfit_body_afb.1006.iff\" \"sourceImages\"\n89\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1005_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1005.iff\" 3067098827 \"textures/chr_barbiearrivaloutfit_body_afb.1005.iff\" \"sourceImages\"\n90\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1004_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1004.iff\" 2343575419 \"textures/chr_barbiearrivaloutfit_body_afb.1004.iff\" \"sourceImages\"\n91\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1003_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1003.iff\" 965788523 \"textures/chr_barbiearrivaloutfit_body_afb.1003.iff\" \"sourceImages\"\n92\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1002_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1002.iff\" 82897627 \"textures/chr_barbiearrivaloutfit_body_afb.1002.iff\" \"sourceImages\"\n93\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1001_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1001.iff\" 1129353227 \"textures/chr_barbiearrivaloutfit_body_afb.1001.iff\" \"sourceImages\"\n94\n\"default_bin_chr_barbiearrivaloutfit_body_inside_mouth_afb_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_inside_mouth_afb.iff\" 1938877603 \"textures/chr_barbiearrivaloutfit_body_inside_mouth_afb.iff\" \"sourceImages\"\n95\n\"default_bin_chr_barbiearrivaloutfit_body_scalp_mesh_afb_2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_scalp_mesh_afb.iff\" 4277534374 \"textures/chr_barbiearrivaloutfit_body_scalp_mesh_afb.iff\" \"sourceImages\"\n96\n\"default_bin_chr_barbiearrivaloutfit_top_col_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_top_col.iff\" 3166575526 \"textures/chr_barbiearrivaloutfit_top_col.iff\" \"sourceImages\"\n97\n\"default_bin_chr_barbiearrivaloutfit_top_bmp_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_top_bmp.iff\" 4061252506 \"textures/chr_barbiearrivaloutfit_top_bmp.iff\" \"sourceImages\"\n98\n\"default_bin_chr_barbiearrivaloutfit_gums_col_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_gums_col.iff\" 562980120 \"textures/chr_barbiearrivaloutfit_mouth_gums_col.iff\" \"sourceImages\"\n99\n\"default_bin_chr_barbiearrivaloutfit_gums_bmp_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_gums_bmp.iff\" 1864480036 \"textures/chr_barbiearrivaloutfit_mouth_gums_bmp.iff\" \"sourceImages\"\n100\n\"default_bin_chr_barbiearrivaloutfit_gums_gls_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_gums_gls.iff\" 2984588278 \"textures/chr_barbiearrivaloutfit_mouth_gums_gls.iff\" \"sourceImages\"\n101\n\"default_bin_chr_barbiearrivaloutfit_gums_sss_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_gums_sss.iff\" 3505666917 \"textures/chr_barbiearrivaloutfit_mouth_gums_sss.iff\" \"sourceImages\"\n102\n\"default_bin_chr_barbiearrivaloutfit_shoe_stitch_msk_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_shoe_stitch_msk.iff\" 1724424304 \"textures/chr_barbiearrivaloutfit_shoe_stitch_msk.iff\" \"sourceImages\"\n103\n\"default_bin_chr_barbiearrivaloutfit_shoe_col_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_shoe_col.iff\" 4010816052 \"textures/chr_barbiearrivaloutfit_shoe_col.iff\" \"sourceImages\"\n104\n\"default_bin_chr_barbiearrivaloutfit_shoe_bmp_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_shoe_bmp.iff\" 2713707016 \"textures/chr_barbiearrivaloutfit_shoe_bmp.iff\" \"sourceImages\"\n105\n\"default_bin_chr_barbiearrivaloutfit_shoe_gls_msk_1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_shoe_gls_msk.iff\" 1054283300 \"textures/chr_barbiearrivaloutfit_shoe_gls_msk.iff\" \"sourceImages\"\n106\n\"default_bin_chr_barbiearrivaloutfit_teeth_col_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_teeth_col.iff\" 3839328299 \"textures/chr_barbiearrivaloutfit_mouth_teeth_col.iff\" \"sourceImages\"\n107\n\"default_bin_chr_barbiearrivaloutfit_teeth_bmp_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_teeth_bmp.iff\" 2860011543 \"textures/chr_barbiearrivaloutfit_mouth_teeth_bmp.iff\" \"sourceImages\"\n108\n\"default_bin_chr_barbiearrivaloutfit_teeth_gls_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_teeth_gls.iff\" 1958532805 \"textures/chr_barbiearrivaloutfit_mouth_teeth_gls.iff\" \"sourceImages\"\n109\n\"default_bin_chr_barbiearrivaloutfit_teeth_sss_default\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_teeth_sss.iff\" 363716182 \"textures/chr_barbiearrivaloutfit_mouth_teeth_sss.iff\" \"sourceImages\"\n110\n\"default_bin_chr_barbiearrivaloutfit_eye_lashes_trn_2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_lashes_trn.iff\" 3435516613 \"textures/chr_barbiearrivaloutfit_eye_lashes_trn.iff\" \"sourceImages\"\n111\n\"default_bin_chr_barbiearrivaloutfit_eyes_col_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_sclera_col.iff\" 152223901 \"textures/chr_barbiearrivaloutfit_eye_sclera_col.iff\" \"sourceImages\"\n112\n\"default_bin_chr_barbiearrivaloutfit_eyes_trn_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_sclera_trn.iff\" 1860378872 \"textures/chr_barbiearrivaloutfit_eye_sclera_trn.iff\" \"sourceImages\"\n113\n\"default_bin_chr_barbiearrivaloutfit_eye_afb_scp_2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_afb_scp.iff\" 1896790746 \"textures/chr_barbiearrivaloutfit_eye_afb_scp.iff\" \"sourceImages\"\n114\n\"default_bin_chr_barbiearrivaloutfit_jeans_bmp_2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_jeans01_bmp.1001.iff\" 445435058 \"textures/chr_barbiearrivaloutfit_jeans01_bmp.1001.iff\" \"sourceImages\"\n115\n\"default_bin_chr_barbiearrivaloutfit_jeans_col_2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_jeans01_col.1001.iff\" 3839318138 \"textures/chr_barbiearrivaloutfit_jeans01_col.1001.iff\" \"sourceImages\"\n116\n\"default_bin_chr_barbiearrivaloutfit_tongue_col1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_tongue_col.iff\" 1506732257 \"textures/chr_barbiearrivaloutfit_mouth_tongue_col.iff\" \"sourceImages\"\n117\n\"default_bin_chr_barbiearrivaloutfit_tongue_bmp1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_tongue_bmp.iff\" 392247517 \"textures/chr_barbiearrivaloutfit_mouth_tongue_bmp.iff\" \"sourceImages\"\n118\n\"default_bin_chr_barbiearrivaloutfit_tongue_gls1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_tongue_gls.iff\" 3383082511 \"textures/chr_barbiearrivaloutfit_mouth_tongue_gls.iff\" \"sourceImages\"\n119\n\"default_bin_chr_barbiearrivaloutfit_tongue_sss1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_tongue_sss.iff\" 2830415516 \"textures/chr_barbiearrivaloutfit_mouth_tongue_sss.iff\" \"sourceImages\"\n120\n\"default_bin_chr_barbiearrivaloutfit_iris_col_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_iris_col.iff\" 3447587311 \"textures/chr_barbiearrivaloutfit_eye_iris_col.iff\" \"sourceImages\"\n121\n\"default_bin_chr_barbiearrivaloutfit_iris_bmp_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_eye_iris_bmp.iff\" 2211566035 \"textures/chr_barbiearrivaloutfit_eye_iris_bmp.iff\" \"sourceImages\"\n122\n\"default_bin_chr_barbiearrivaloutfit_body_scalp_mesh_afb_3\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_scalp_mesh_afb.iff\" 4277534374 \"textures/chr_barbiearrivaloutfit_body_scalp_mesh_afb.iff\" \"sourceImages\"\n123\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1001_default2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1001.iff\" 2100974105 \"textures/chr_barbiearrivaloutfit_body_rev.col.1001.iff\" \"sourceImages\"\n124\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1002_default2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1002.iff\" 983181513 \"textures/chr_barbiearrivaloutfit_body_rev.col.1002.iff\" \"sourceImages\"\n125\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1003_default2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1003.iff\" 133824889 \"textures/chr_barbiearrivaloutfit_body_rev.col.1003.iff\" \"sourceImages\"\n126\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1004_default2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1004.iff\" 3051019625 \"textures/chr_barbiearrivaloutfit_body_rev.col.1004.iff\" \"sourceImages\"\n127\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1005_default2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1005.iff\" 2293953753 \"textures/chr_barbiearrivaloutfit_body_rev.col.1005.iff\" \"sourceImages\"\n128\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1006_default2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_rev.col.1006.iff\" 3474624009 \"textures/chr_barbiearrivaloutfit_body_rev.col.1006.iff\" \"sourceImages\"\n129\n\"default_bin_chr_barbiearrivaloutfit_skin_gls_default1\" \"fileTextureName\" \"textures/chr_chelseaarrivaloutfit_nose_lip_gls.iff\" 2680993943 \"textures/chr_chelseaarrivaloutfit_nose_lip_gls.iff\" \"sourceImages\"\n130\n\"default_bin_chr_barbiearrivaloutfit_skin_bmp_1001_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1001.iff\" 1616521540 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1001.iff\" \"sourceImages\"\n131\n\"default_bin_chr_barbiearrivaloutfit_skin_bmp_1002_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1002.iff\" 670716820 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1002.iff\" \"sourceImages\"\n132\n\"default_bin_chr_barbiearrivaloutfit_skin_bmp_1003_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1003.iff\" 446331428 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1003.iff\" \"sourceImages\"\n133\n\"default_bin_chr_barbiearrivaloutfit_skin_bmp_1004_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1004.iff\" 2830804532 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1004.iff\" \"sourceImages\"\n134\n\"default_bin_chr_barbiearrivaloutfit_skin_bmp_1005_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1005.iff\" 2514128772 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1005.iff\" \"sourceImages\"\n135\n\"default_bin_chr_barbiearrivaloutfit_skin_bmp_1006_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_bmp.flattened.1006.iff\" 3531273556 \"textures/chr_barbiearrivaloutfit_bmp.flattened.1006.iff\" \"sourceImages\"\n136\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1006_default3\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1006.iff\" 4050668571 \"textures/chr_barbiearrivaloutfit_body_afb.1006.iff\" \"sourceImages\"\n137\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1005_default3\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1005.iff\" 3067098827 \"textures/chr_barbiearrivaloutfit_body_afb.1005.iff\" \"sourceImages\"\n138\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1004_default3\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1004.iff\" 2343575419 \"textures/chr_barbiearrivaloutfit_body_afb.1004.iff\" \"sourceImages\"\n139\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1003_default3\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1003.iff\" 965788523 \"textures/chr_barbiearrivaloutfit_body_afb.1003.iff\" \"sourceImages\"\n140\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1002_default3\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1002.iff\" 82897627 \"textures/chr_barbiearrivaloutfit_body_afb.1002.iff\" \"sourceImages\"\n141\n\"default_bin_chr_barbiearrivaloutfit_skin_col_1001_default3\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_afb.1001.iff\" 1129353227 \"textures/chr_barbiearrivaloutfit_body_afb.1001.iff\" \"sourceImages\"\n142\n\"default_bin_chr_barbiearrivaloutfit_body_inside_mouth_afb_2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_inside_mouth_afb.iff\" 1938877603 \"textures/chr_barbiearrivaloutfit_body_inside_mouth_afb.iff\" \"sourceImages\"\n143\n\"default_bin_chr_barbiearrivaloutfit_body_scalp_mesh_afb_4\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_body_scalp_mesh_afb.iff\" 4277534374 \"textures/chr_barbiearrivaloutfit_body_scalp_mesh_afb.iff\" \"sourceImages\"\n144\n\"default_bin_chr_barbiearrivaloutfit_top_col_2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_top_col.iff\" 3166575526 \"textures/chr_barbiearrivaloutfit_top_col.iff\" \"sourceImages\"\n145\n\"default_bin_chr_barbiearrivaloutfit_top_bmp_2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_top_bmp.iff\" 4061252506 \"textures/chr_barbiearrivaloutfit_top_bmp.iff\" \"sourceImages\"\n146\n\"default_bin_chr_barbiearrivaloutfit_gums_col_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_gums_col.iff\" 562980120 \"textures/chr_barbiearrivaloutfit_mouth_gums_col.iff\" \"sourceImages\"\n147\n\"default_bin_chr_barbiearrivaloutfit_gums_bmp_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_gums_bmp.iff\" 1864480036 \"textures/chr_barbiearrivaloutfit_mouth_gums_bmp.iff\" \"sourceImages\"\n148\n\"default_bin_chr_barbiearrivaloutfit_gums_gls_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_gums_gls.iff\" 2984588278 \"textures/chr_barbiearrivaloutfit_mouth_gums_gls.iff\" \"sourceImages\"\n149\n\"default_bin_chr_barbiearrivaloutfit_gums_sss_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_gums_sss.iff\" 3505666917 \"textures/chr_barbiearrivaloutfit_mouth_gums_sss.iff\" \"sourceImages\"\n150\n\"default_bin_chr_barbiearrivaloutfit_shoe_stitch_msk_2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_shoe_stitch_msk.iff\" 1724424304 \"textures/chr_barbiearrivaloutfit_shoe_stitch_msk.iff\" \"sourceImages\"\n151\n\"default_bin_chr_barbiearrivaloutfit_shoe_col_2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_shoe_col.iff\" 4010816052 \"textures/chr_barbiearrivaloutfit_shoe_col.iff\" \"sourceImages\"\n152\n\"default_bin_chr_barbiearrivaloutfit_shoe_bmp_2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_shoe_bmp.iff\" 2713707016 \"textures/chr_barbiearrivaloutfit_shoe_bmp.iff\" \"sourceImages\"\n153\n\"default_bin_chr_barbiearrivaloutfit_shoe_gls_msk_2\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_shoe_gls_msk.iff\" 1054283300 \"textures/chr_barbiearrivaloutfit_shoe_gls_msk.iff\" \"sourceImages\"\n154\n\"default_bin_chr_barbiearrivaloutfit_teeth_col_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_teeth_col.iff\" 3839328299 \"textures/chr_barbiearrivaloutfit_mouth_teeth_col.iff\" \"sourceImages\"\n155\n\"default_bin_chr_barbiearrivaloutfit_teeth_bmp_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_teeth_bmp.iff\" 2860011543 \"textures/chr_barbiearrivaloutfit_mouth_teeth_bmp.iff\" \"sourceImages\"\n156\n\"default_bin_chr_barbiearrivaloutfit_teeth_gls_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_teeth_gls.iff\" 1958532805 \"textures/chr_barbiearrivaloutfit_mouth_teeth_gls.iff\" \"sourceImages\"\n157\n\"default_bin_chr_barbiearrivaloutfit_teeth_sss_default1\" \"fileTextureName\" \"textures/chr_barbiearrivaloutfit_mouth_teeth_sss.iff\" 363716182 \"textures/chr_barbiearrivaloutfit_mouth_teeth_sss.iff\" \"sourceImages\"\nendStream\nendChannel\nendAssociations\n" 
		-scn;
// End of faceLocators01.ma
