"""Random Wallpaper Setter for Linux.

This module provides a set of functions to identify, choose, and set a wallpaper 
on Linux when provided with a directory containing wallpaper images.

Example:
	$ python3 random_wallpaper.py

Your wallpaper directory must be defined on line 18.
Allowed image file extensions are defined on line 16.

"""

import os, random

ALLOWED_FILETYPES = ['png', 'jpg', 'jpeg']

WALLPAPER_DIRECTORY = ''

def is_valid_directory(path):
	"""Validates that a given path is a valid directory.

	Args:
		path (str): the path to query

	Returns:
		true: if the path is a directory
		false: otherwise

	"""
	return os.path.isdir(path)

def is_valid_image(filename):
	"""Validates that a given file exists and is of a permitted type.

	Args:
		filename (str): the filename of the file to query

	Returns:
		true: if the file exists and is of a permitted type
		false: otherwise
		
	"""
	return os.path.isfile(os.path.join(WALLPAPER_DIRECTORY, filename)) and filename.split(".")[-1].lower() in ALLOWED_FILETYPES

def get_all_wallpaper_files():
	"""Creates a list of valid image files in the wallpaper directory.

	Returns:
		list (str): a list of filenames for valid image files
		
	"""
	return [file for file in os.listdir(WALLPAPER_DIRECTORY) if is_valid_image(file)]

def get_random_wallpaper_file(wallpaper_files):
	"""Chooses a random file from a list of files.

	Args:
		wallpaper_files (list of str): a list of valid image files to choose from

	Returns:
		None: if no wallpaper files are provided
		str: otherwise, a random file choice
		
	"""
	if len(wallpaper_files) > 0:
	    return random.choice(wallpaper_files)
	else:
		print('No Wallpaper Files Provided')
		return None

def set_wallpaper(filename):
	"""Sets the systems wallpaper to the image at a given filename.

	Args:
		filename (str): the filename of the file to set as the wallpaper

	"""
	if len(filename) > 0:
		os.system("gsettings set org.gnome.desktop.background picture-uri file://" + os.path.join(WALLPAPER_DIRECTORY, filename))
	else:
		print('No Wallpaper File Provided')

def set_random_wallpaper():
	"""Sets the systems wallpaper to a random image within a given wallpaper directory."""
	if is_valid_directory(WALLPAPER_DIRECTORY):
		wallpaper_files = get_all_wallpaper_files()
		new_wallpaper = get_random_wallpaper_file(wallpaper_files)
		set_wallpaper(new_wallpaper)
	else:
		print('Invalid Wallpaper Directory')

# set a random wallpaper for the system
set_random_wallpaper()