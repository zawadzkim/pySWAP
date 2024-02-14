# import os
# from .utils.utils import open_file
# print('Hello from pySWAP/__init__.py')
# project_dir = os.path.dirname(os.path.abspath(__file__))


# def _open_templates(template_dict) -> None:
#     """
#     Opens the template files specified in the swp_file dictionary and saves the contents in the corresponding
#     dictionary values.

#     Args:
#         None

#     Returns:
#         None

#     Raises:
#         None

#     For each key-value pair in the swp_file dictionary, the corresponding template file is opened and its contents
#     are saved in the 'section_text' value of the dictionary. An empty dictionary is also created and saved in the
#     'params' value of the dictionary.
#     """

#     for key, value in template_dict.items():
#         value['template_text'] = open_file(value['template_path'])
#         value['params'] = {}
#         value['tables'] = {}


# meteo_file_verbose = {
#     'template_path': project_dir + r'\data\templates\met_header.txt'
# }

# swp_file_verbose = {
#     'header': {'template_path': project_dir + r'/data/templates/swp_1_header.txt'},
#     'general': {'template_path': project_dir + r'/data/templates/swp_2_general.txt'},
#     'meteo': {'template_path': project_dir + r'/data/templates/swp_3_meteo.txt'},
#     'crop': {'template_path': project_dir + r'/data/templates/swp_4_crop.txt'},
#     'irrigation': {'template_path': project_dir + r'/data/templates/swp_41_irrigation.txt'},
#     'soil_water': {'template_path': project_dir + r'/data/templates/swp_5_soil-water.txt'},
#     'drainage': {'template_path': project_dir + r'/data/templates/swp_6_lateral-drainage.txt'},
#     'bott_bound': {'template_path': project_dir + r'/data/templates/swp_7_bottom-boundary.txt'},
#     'heat_flow': {'template_path': project_dir + r'/data/templates/swp_8_heat-flow.txt'},
#     'solute': {'template_path': project_dir + r'/data/templates/swp_9_solute.txt'},
#     'foot_line': {'template_path': project_dir + r'/data/templates/swp_10_endfile.txt'}
# }
