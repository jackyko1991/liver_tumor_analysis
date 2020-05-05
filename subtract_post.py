import SimpleITK as sitk
import os
from tqdm import tqdm

def subtract_image(image1_path, image2_path, image_out_path):
	reader = sitk.ImageFileReader()
	reader.SetFileName(image1_path)
	image1 = reader.Execute()
	reader.SetFileName(image2_path)
	image2 = reader.Execute()

	image_out = image1 - image2

	thresholdImageFilter = sitk.ThresholdImageFilter()
	thresholdImageFilter.SetUpper(9999)
	thresholdImageFilter.SetLower(0)
	image_out = thresholdImageFilter.Execute(image_out)

	writer = sitk.ImageFileWriter()
	writer.SetFileName(image_out_path)
	writer.Execute(image_out)

def main():
	data_dir = "./data/by_case"

	pbar = tqdm(os.listdir(data_dir))

	for case in pbar:
		pbar.set_description(case)

		if not (os.path.exists(os.path.join(data_dir,case,"post","nii_reg_pre", "HA", "temporal_mIP.nii.gz")) and 
			os.path.exists(os.path.join(data_dir,case,"post","nii_reg_pre", "HA", "01.nii.gz"))):
			continue

		subtract_image(
			os.path.join(data_dir,case,"post","nii_reg_pre", "HA", "temporal_mIP.nii.gz"),
			os.path.join(data_dir,case,"post","nii_reg_pre", "HA", "01.nii.gz"),
			os.path.join(data_dir,case,"post","nii_reg_pre", "HA", "temporal_mIP_subtract_baseline.nii.gz")
			)

if __name__ == "__main__":
	main()