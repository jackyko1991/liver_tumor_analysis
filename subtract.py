import os
import SimpleITK as sitk

def main():
	working_dir = "./data"

	reader = sitk.ImageFileReader()

	for patient in os.listdir(working_dir):
		if os.path.isdir(os.path.join(working_dir, patient)):
			print("Working on",patient)
			for stage in os.listdir(os.path.join(working_dir, patient)):
				for phase in os.listdir(os.path.join(working_dir, patient,stage, "nii_reg")):
					if phase == "plain.nii.gz":
						continue
					else:
						os.makedirs(os.path.join(working_dir,patient,stage,"nii_subtract",phase),exist_ok=True)

						reader = sitk.ImageFileReader()
						# load plain image
						reader.SetFileName(os.path.join(working_dir,patient,stage,"nii_reg","plain.nii.gz"))
						plain = reader.Execute()

						# load contrast images
						contrast_list = []
						for file in os.listdir(os.path.join(working_dir,patient,stage,"nii_reg",phase)):
							if file == "plain.nii.gz":
								continue
							else:
								reader.SetFileName(os.path.join(working_dir,patient,stage,"nii_reg",phase,file))
								contrast = reader.Execute()
								contrast_list.append(contrast)


						# maximize the contrast images then subtract by plain image
						maxFilter = sitk.MaximumImageFilter()
						statFilter = sitk.StatisticsImageFilter()
						statFilter.Execute(plain)

						maxImage = sitk.Image(plain.GetSize()[0],plain.GetSize()[1],plain.GetSize()[2],sitk.sitkFloat32)
						addFilter = sitk.AddImageFilter()
						maxImage = addFilter.Execute(maxImage,statFilter.GetMinimum())

						maxImage.SetDirection(plain.GetDirection())
						maxImage.SetOrigin(plain.GetOrigin())
						maxImage.SetSpacing(plain.GetSpacing())
						for contrast in contrast_list:
							maxImage = maxFilter.Execute(maxImage,contrast)

						writer = sitk.ImageFileWriter()
						writer.SetFileName(os.path.join(working_dir,patient,stage,"nii_subtract",phase,"max.nii.gz"))
						writer.Execute(maxImage)

						subtractFilter = sitk.SubtractImageFilter()
						average_subtract = subtractFilter.Execute(maxImage,plain)
						writer.SetFileName(os.path.join(working_dir,patient,stage,"nii_subtract",phase,"max_subtract.nii.gz"))
						writer.Execute(average_subtract)


if __name__=="__main__":
	main()