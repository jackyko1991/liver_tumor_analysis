import SimpleITK as sitk
import numpy as np
import os

def main():
	data_dir = "./data/by_case"

	stages = ["pre","post"]
	phases = ["HA","PV"]

	for case in os.listdir(data_dir)[5:]:
		print(case)
		images = []
		images_np = []
		for stage in stages:
			for phase in phases:
				if stage == "pre":
					filename = os.path.join(data_dir,case, stage,"nii_reg",phase,"label_tf.nii.gz")
				else:
					filename = os.path.join(data_dir,case, stage,"nii_reg_pre",phase,"label_tf.nii.gz")

				if not os.path.exists(filename):
					continue
				reader = sitk.ImageFileReader()
				reader.SetFileName(filename)
				castFilter = sitk.CastImageFilter()
				castFilter.SetOutputPixelType(sitk.sitkUInt8)
				images.append(castFilter.Execute(reader.Execute()))

		for image in images:
			image.SetOrigin(images[0].GetOrigin())

		votingFilter = sitk.LabelVotingImageFilter()
		votingFilter.SetLabelForUndecidedPixels(0)
		label = votingFilter.Execute(images)
		writer = sitk.ImageFileWriter()
		writer.SetFileName(os.path.join(data_dir,case, "label.nii.gz"))
		writer.Execute(label)

if __name__ == "__main__":
	main()