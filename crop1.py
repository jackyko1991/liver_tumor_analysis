import os
import SimpleITK as sitk

def main():
	working_dir = "./data/by_case"

	reader = sitk.ImageFileReader()
	ignore = ["ChoySimWang","HuiSiuKuenMary","KowkMenYee","LeungKwokMan","WongMukChing","ChuKitPing"]

	for patient in os.listdir(working_dir):
		if patient in ignore:
			continue

		if os.path.isdir(os.path.join(working_dir, patient)):
			print("Working on",patient)
			for stage in os.listdir(os.path.join(working_dir, patient)):
				for phase in os.listdir(os.path.join(working_dir, patient,stage, "nii")):
					# os.makedirs(os.path.join(working_dir,patient,stage,"nii_reg",phase),exist_ok=True)
					
					if phase == "plain":
						continue
					else:
						os.makedirs(os.path.join(working_dir,patient,stage,"nii_crop",phase),exist_ok=True)

						# load reference data
						for file in os.listdir(os.path.join(working_dir,patient,stage,"nii",phase)):
							if file.split('.')[0][-2:] == "01":
								reader.SetFileName(os.path.join(working_dir,patient, stage, "nii", phase, file))
								reference = reader.Execute()

						# crop plain image
						print(stage,phase,"plain")
						plainFilename = os.listdir(os.path.join(working_dir,patient, stage, "nii", "plain"))[0]

						reader.SetFileName(os.path.join(working_dir,patient, stage, "nii", "plain",plainFilename))
						plain = reader.Execute()

						resampler = sitk.ResampleImageFilter()
						resampler.SetOutputSpacing(reference.GetSpacing())
						resampler.SetSize(reference.GetSize())
						resampler.SetInterpolator(2)
						resampler.SetOutputOrigin(reference.GetOrigin())
						resampler.SetOutputDirection(reference.GetDirection())

						# resample on plain image
						resampler.SetInterpolator(2)
						resampler.SetOutputOrigin(reference.GetOrigin())
						resampler.SetOutputDirection(reference.GetDirection())
						cropped = resampler.Execute(plain)

						writer = sitk.ImageFileWriter()
						writer.SetFileName(os.path.join(working_dir,patient, stage, "nii_crop", phase, "plain.nii.gz"))
						writer.Execute(cropped)
								
						# # load registered contrast image
						# for file in os.listdir(os.path.join(working_dir,patient,stage,"nii_reg",phase)):
						# 	print(stage,phase,file)
						# 	reader.SetFileName(os.path.join(working_dir,patient, stage, "nii_reg", phase, file))
						# 	registerted = reader.Execute()

						# 	cropped = resampler.Execute(registerted)

						# 	writer.SetFileName(os.path.join(working_dir,patient, stage, "nii_crop", phase, file))
						# 	writer.Execute(cropped)
						# 	# exit()
						
						# load time phase image
						for file in os.listdir(os.path.join(working_dir,patient,stage,"nii",phase)):
							print(stage,phase,file)
							reader.SetFileName(os.path.join(working_dir,patient, stage, "nii", phase, file))
							registerted = reader.Execute()

							cropped = resampler.Execute(registerted)

							writer.SetFileName(os.path.join(working_dir,patient, stage, "nii_crop", phase, file.split('.')[0][-2:] + ".nii.gz"))
							writer.Execute(cropped)
							# exit()

if __name__=="__main__":
	main()