import os
import numpy as np
import SimpleITK as sitk
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tqdm import tqdm

def main():
	src_dir = "./data/by_case"

	pbar = tqdm(os.listdir(src_dir))

	stages = ["pre","post"]
	phases = ["HA","PV"]

	for case in pbar:
		pbar.set_description(case)

		# # merge labels
		reader = sitk.ImageFileReader()
		reader.SetFileName(os.path.join(src_dir,case,"label.nii.gz"))
		label_liver = reader.Execute()

		reader.SetFileName(os.path.join(src_dir,case,"pre","nii_reg","HA","tumor_original_space.nii.gz"))
		label_tumor = reader.Execute()
		multiplyFilter = sitk.MultiplyImageFilter()

		andFilter = sitk.AndImageFilter()
		label_liver = label_liver - andFilter.Execute(label_liver,label_tumor)
		label = label_liver + label_tumor*2

		# # save label
		# writer = sitk.ImageFileWriter()
		# writer.SetFileName(os.path.join(src_dir,case,"label_merged.nii.gz"))
		# writer.Execute(label)

		for stage in stages:
			for phase in phases:
				images = []
				images_np = []

				liver_value = []
				tumor_value = []

				for time in range(1,11):
					if stage == "pre":
						if time < 10:
							filename = os.path.join(src_dir,case,stage,"nii_reg",phase,"0"+str(time)+".nii.gz")
						else:
							filename = os.path.join(src_dir,case,stage,"nii_reg",phase,str(time)+".nii.gz")
					else:
						if time < 10:
							filename = os.path.join(src_dir,case,stage,"nii_reg_pre",phase,"0"+str(time)+".nii.gz")
						else:
							filename = os.path.join(src_dir,case,stage,"nii_reg_pre",phase,str(time)+".nii.gz")

					if not os.path.exists(filename):
						continue

					reader.SetFileName(filename)
					image = reader.Execute()
					images.append(image)

					statFilter = sitk.LabelStatisticsImageFilter()
					statFilter.Execute(image,label)
					liver_value.append(statFilter.GetMean(1))
					tumor_value.append(statFilter.GetMean(2))

				x = np.arange(len(images))
				plt.plot(x, liver_value,"o--", label=phase+"_liver")
				plt.plot(x, tumor_value,"o--", label=phase+"_tumor")
				plt.xlim(-0.5,9.5)
				plt.ylim(0,800)
				plt.legend()
				plt.xlabel("time")
				plt.ylabel("HU value")
			if stage == "pre":
				plt.title("Pre-Treatment")
				plt.savefig(os.path.join(src_dir,case,"plot","perfusion_curve_pre.jpg"))
			else:
				plt.title("Post-Treatment")
				plt.savefig(os.path.join(src_dir,case,"plot","perfusion_curve_post.jpg"))
			# plt.show()			
			
			plt.clf()

		# exit()

if __name__ == "__main__":
	main()