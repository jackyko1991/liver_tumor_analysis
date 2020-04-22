import os
from tqdm import tqdm
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

def plot(plain_path, pre_HA_path, pre_PV_path, post_PV_path,output_dir):
	reader = sitk.ImageFileReader()
	reader.SetFileName(plain_path)
	plain = reader.Execute()
	reader.SetFileName(pre_HA_path)
	pre_HA = reader.Execute()
	reader.SetFileName(pre_PV_path)
	pre_PV = reader.Execute()
	reader.SetFileName(post_PV_path)
	post_PV = reader.Execute()

	intensityWindowingFilter = sitk.IntensityWindowingImageFilter()
	intensityWindowingFilter.SetOutputMaximum(255)
	intensityWindowingFilter.SetOutputMinimum(0)
	intensityWindowingFilter.SetWindowMaximum(300);
	intensityWindowingFilter.SetWindowMinimum(0);
	plain = intensityWindowingFilter.Execute(plain)

	plain_np = sitk.GetArrayFromImage(plain)
	pre_HA_np = sitk.GetArrayFromImage(pre_HA)
	pre_PV_np = sitk.GetArrayFromImage(pre_PV)
	post_PV_np = sitk.GetArrayFromImage(post_PV)

	for z in range(plain_np.shape[0]):
		# if not (z == 32):
		# 	continue

		plain_slice = plain_np[z,:,:]
		pre_HA_slice = pre_HA_np[z,:,:]
		pre_PV_slice = pre_PV_np[z,:,:]
		post_PV_slice = post_PV_np[z,:,:]

		dpi = 100
		shape=np.shape(plain_slice)[0:2][::-1]
		size = [float(i)/dpi for i in shape]

		fig = plt.figure()
		fig.set_size_inches(size)
		ax = plt.Axes(fig,[0,0,1,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(plain_slice,cmap="gray",origin='lower')
		ax.contour(pre_HA_slice,[0,1], colors='r',origin='lower',linewidths=1)
		ax.contour(pre_PV_slice,[0,1], colors='lawngreen',origin='lower',linewidths=1)
		ax.contour(post_PV_slice,[0,1], colors='dodgerblue',origin='lower',linewidths=1)

		if z < 9:
			fig.savefig(os.path.join(output_dir,"0" + str(z+1) + ".jpg"),dpi=dpi)
		else:
			fig.savefig(os.path.join(output_dir,str(z+1) + ".jpg"),dpi=dpi)

		plt.close(fig)

def main():
	data_dir = "./data/by_case"

	pbar = tqdm(os.listdir(data_dir))

	for case in pbar:
		pbar.set_description(case)
		plain_path = os.path.join(data_dir,case,"pre","nii_reg","HA","plain.nii.gz")
		pre_HA_path = os.path.join(data_dir,case,"pre","nii_reg","HA","tumor_original_space.nii.gz")
		pre_PV_path = os.path.join(data_dir,case,"pre","nii_reg","PV","tumor_original_space.nii.gz")
		post_PV_path = os.path.join(data_dir,case,"post","nii_reg_pre","PV","tumor_original_space.nii.gz")
		output_dir = os.path.join(data_dir,case,"plot","boundary")

		if not (os.path.exists(plain_path) and os.path.exists(pre_HA_path) and os.path.exists(pre_PV_path) and os.path.exists(post_PV_path)):
			continue

		if not os.path.exists(output_dir):
			os.makedirs(output_dir,exist_ok=True)

		plot(plain_path, pre_HA_path, pre_PV_path, post_PV_path,output_dir)


if __name__=="__main__":
	main()