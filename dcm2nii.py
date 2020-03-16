import os

def dcm2nii():
	return

def main():
	working_dir = "./"
	for patient in os.listdir(working_dir):
		if os.path.isdir(os.path.join(working_dir, patient)):
			print("Working on",patient)
			for stage in os.listdir(os.path.join(working_dir, patient)):
				for phase in os.listdir(os.path.join(working_dir, patient,stage, "dicom")):
					for file in os.listdir(os.path.join(working_dir, patient,stage, "dicom",phase)):
						if os.path.splitext(file)[1] == ".gz":
							print(os.path.join(working_dir, patient,stage, "dicom", file))
							source_file = os.path.join(working_dir, patient,stage, "dicom", phase, file)
							target_file = os.path.join(working_dir, patient,stage, "nii", phase, file)
							print(source_file,target_file)
							os.makedirs(os.path.join(working_dir, patient,stage, "nii", phase), exist_ok=True)
							os.rename(source_file, target_file)


if __name__=="__main__":
	main()