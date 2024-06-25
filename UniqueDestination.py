import os

#After every execution the image will be saved with its unique destination or name of image as per user info
def uniqueDestination(base_path,extension):
	count = 1
	new_path = f"{base_path}.{extension}"
	while os.path.exists(new_path):

		new_path = f"{base_path}_({count}).{extension}"
		count += 1
	return new_path