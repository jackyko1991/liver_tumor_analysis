import os
import numpy as np
import SimpleITK as sitk
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tqdm import tqdm

def nomralize_series(series):
	series_out = [value - min(series) for value in series]

	return series_out

def main():
	src_dir = "./data/by_case"
	cases = ["WongMukChing"]

	# pbar = tqdm(cases)
	pbar = tqdm(os.listdir(src_dir))

	stages = ["pre","post"]
	phases = ["HA","PV"]

	for case in pbar:
		pbar.set_description(case)

		# merge labels
		reader = sitk.ImageFileReader()
		reader.SetFileName(os.path.join(src_dir,case,"label.nii.gz"))
		label_liver = reader.Execute()

		reader.SetFileName(os.path.join(src_dir,case,"pre","nii_reg","HA","tumor_original_space.nii.gz"))
		label_tumor = reader.Execute()
		multiplyFilter = sitk.MultiplyImageFilter()

		andFilter = sitk.AndImageFilter()
		label_liver = label_liver - andFilter.Execute(label_liver,label_tumor)
		label = label_liver + label_tumor*2

		# save label
		writer = sitk.ImageFileWriter()
		writer.SetFileName(os.path.join(src_dir,case,"label_merged.nii.gz"))
		writer.Execute(label)

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

					image.SetOrigin(label.GetOrigin())

					statFilter = sitk.LabelStatisticsImageFilter()
					statFilter.Execute(image,label)
					liver_value.append(statFilter.GetMean(1))
					tumor_value.append(statFilter.GetMean(2))

				x = np.arange(len(images))
				liver_value = nomralize_series(liver_value)
				tumor_value = nomralize_series(tumor_value)

				plt.plot(x, liver_value,"o--", label=phase+"_liver")
				plt.plot(x, tumor_value,"o--", label=phase+"_tumor")
				plt.xlim(0,9.5)
				plt.ylim(-10,800)
				plt.legend()
				plt.xlabel("time")
				plt.ylabel("HU value")

			if not os.path.exists(os.path.join(src_dir,case,"plot")):
				os.makedirs(os.path.join(src_dir,case,"plot"),exist_ok=True)

			if stage == "pre":
				plt.title("Pre-Treatment")
				plt.savefig(os.path.join(src_dir,case,"plot","perfusion_curve_pre.jpg"))
			else:
				plt.title("Post-Treatment")
				plt.savefig(os.path.join(src_dir,case,"plot","perfusion_curve_post.jpg"))
			# plt.show()			
			
			plt.clf()

		# plot tumor only perfusion
		for phase in phases:
			images_pre = []
			images_post = []

			tumor_pre_value = []
			tumor_post_value = []

			for time in range(1,11):
				if time < 10:
					filename_pre = os.path.join(src_dir,case,"pre","nii_reg",phase,"0"+str(time)+".nii.gz")
				else:
					filename_pre = os.path.join(src_dir,case,"pre","nii_reg",phase,str(time)+".nii.gz")
				if time < 10:
					filename_post = os.path.join(src_dir,case,"post","nii_reg_pre",phase,"0"+str(time)+".nii.gz")
				else:
					filename_post = os.path.join(src_dir,case,"post","nii_reg_pre",phase,str(time)+".nii.gz")

				if not (os.path.exists(filename_pre) and os.path.exists(filename_post)):
					continue

				reader.SetFileName(filename_pre)
				image_pre = reader.Execute()
				reader.SetFileName(filename_post)
				image_post = reader.Execute()

				images_pre.append(image_pre)
				images_post.append(image_post)
				image_pre.SetOrigin(label.GetOrigin())
				image_post.SetOrigin(label.GetOrigin())
				statFilter = sitk.LabelStatisticsImageFilter()
				statFilter.Execute(image_pre,label)
				tumor_pre_value.append(statFilter.GetMean(2))
				statFilter.Execute(image_post,label)
				tumor_post_value.append(statFilter.GetMean(2))

			x = np.arange(len(images_pre))
			tumor_pre_value = nomralize_series(tumor_pre_value)
			tumor_post_value = nomralize_series(tumor_post_value)

			plt.plot(x, tumor_pre_value,"o--", label="Pre_"+phase)
			plt.plot(x, tumor_post_value,"o--", label="Post_"+phase)
		plt.xlim(0,9.5)
		plt.ylim(-10,800)
		plt.legend()
		plt.xlabel("time")
		plt.ylabel("HU value")

		plt.title("Perfusion Curve")
		plt.savefig(os.path.join(src_dir,case,"plot","perfusion_curve.jpg"))
		plt.clf()
		
if __name__ == "__main__":
	main()