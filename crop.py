import os
import SimpleITK as sitk
from tqdm import tqdm

def main():
	working_dir = "Z:/data/liver/by_case"

	reader = sitk.ImageFileReader()
	# cases = os.listdir(working_dir)
	cases = ["ChungWahKitFacchetti","LamMoChe","SitLeongWor","TamSunnyKing","WongNaiKeung","WongWaiLun","WongYiu","YauPoHing"]
	ignore = ["ChoySimWang","HuiSiuKuenMary","KowkMenYee","LeungKwokMan","WongMukChing","ChuKitPing"]

	pbar = tqdm(cases)
	for patient in pbar:
		if patient in ignore:
			continue

		if os.path.isdir(os.path.join(working_dir, patient)):
			pbar.set_description(patient)
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
						tqdm.write("Cropping: {} {} {}".format(stage,phase,"plain"))
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
						pbar2 = tqdm(os.listdir(os.path.join(working_dir,patient,stage,"nii",phase)))

						for file in pbar2:
							tqdm.write("Cropping: {} {} {}".format(stage,phase,file))
							reader.SetFileName(os.path.join(working_dir,patient, stage, "nii", phase, file))
							registerted = reader.Execute()

							cropped = resampler.Execute(registerted)

							writer.SetFileName(os.path.join(working_dir,patient, stage, "nii_crop", phase, file.split('.')[0][-2:] + ".nii.gz"))
							writer.Execute(cropped)
							# exit()

if __name__=="__main__":
	main()