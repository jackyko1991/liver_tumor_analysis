import os
from tqdm import tqdm
import SimpleITK as sitk
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_HA(plain_path, pre_HA_path, post_HA_path,output_dir):
	reader = sitk.ImageFileReader()
	reader.SetFileName(plain_path)
	plain = reader.Execute()
	reader.SetFileName(pre_HA_path)
	pre_HA = reader.Execute()
	reader.SetFileName(post_HA_path)
	post_HA = reader.Execute()

	intensityWindowingFilter = sitk.IntensityWindowingImageFilter()
	intensityWindowingFilter.SetOutputMaximum(255)
	intensityWindowingFilter.SetOutputMinimum(0)
	intensityWindowingFilter.SetWindowMaximum(300);
	intensityWindowingFilter.SetWindowMinimum(0);
	plain = intensityWindowingFilter.Execute(plain)

	plain_np = sitk.GetArrayFromImage(plain)
	pre_HA_np = sitk.GetArrayFromImage(pre_HA)
	post_HA_np = sitk.GetArrayFromImage(post_HA)

	for z in tqdm(range(plain_np.shape[0])):
		plain_slice = plain_np[z,:,:]
		pre_HA_slice = pre_HA_np[z,:,:]
		post_HA_slice = post_HA_np[z,:,:]

		dpi = 100
		shape=np.shape(plain_slice)[0:2][::-1]
		size = [float(i)/dpi for i in shape]

		fig = plt.figure()
		fig.set_size_inches(size)
		ax = plt.Axes(fig,[0,0,1,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(plain_slice,cmap="gray",origin='lower')
		CS_pre_HA = ax.contour(pre_HA_slice,[0,1], colors='r',origin='lower',linewidths=1)
		CS_post_HA = ax.contour(post_HA_slice,[0,1], colors='lawngreen',origin='lower',linewidths=1)

		CS_pre_HA.collections[0].set_label("Pre HA")
		CS_post_HA.collections[0].set_label("Post HA")

		leg = ax.legend(loc='upper right',frameon=False)
		for text in leg.get_texts():
			plt.setp(text, color = 'w')

		if z < 9:
			fig.savefig(os.path.join(output_dir,"0" + str(z+1) + ".jpg"),dpi=dpi)
		else:
			fig.savefig(os.path.join(output_dir,str(z+1) + ".jpg"),dpi=dpi)

		plt.close(fig)

def plot_PV(plain_path, pre_HA_path, pre_PV_path, post_PV_path,output_dir):
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

	for z in tqdm(range(plain_np.shape[0])):
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
		CS_pre_HA = ax.contour(pre_HA_slice,[0,1], colors='r',origin='lower',linewidths=1)
		CS_pre_PV = ax.contour(pre_PV_slice,[0,1], colors='lawngreen',origin='lower',linewidths=1)
		CS_post_PV = ax.contour(post_PV_slice,[0,1], colors='dodgerblue',origin='lower',linewidths=1)

		CS_pre_HA.collections[0].set_label("Pre HA")
		CS_pre_PV.collections[0].set_label("Pre PV")
		CS_post_PV.collections[0].set_label("Post PV")

		leg = ax.legend(loc='upper right',frameon=False)
		for text in leg.get_texts():
			plt.setp(text, color = 'w')

		if z < 9:
			fig.savefig(os.path.join(output_dir,"0" + str(z+1) + ".jpg"),dpi=dpi)
		else:
			fig.savefig(os.path.join(output_dir,str(z+1) + ".jpg"),dpi=dpi)

		plt.close(fig)

def main():
	data_dir = "Z:/data/liver/by_case"

	pbar = tqdm(os.listdir(data_dir))

	for case in pbar:
		pbar.set_description(case)
		plain_path = os.path.join(data_dir,case,"pre","nii_reg","HA","plain.nii.gz")
		pre_HA_path = os.path.join(data_dir,case,"pre","nii_reg","HA","tumor_original_space.nii.gz")
		pre_PV_path = os.path.join(data_dir,case,"pre","nii_reg","PV","tumor_original_space.nii.gz")
		post_HA_path = os.path.join(data_dir,case,"post","nii_reg_pre","HA","tumor_original_space.nii.gz")
		post_PV_path = os.path.join(data_dir,case,"post","nii_reg_pre","PV","tumor_original_space.nii.gz")
		
		if not (os.path.exists(plain_path) and os.path.exists(pre_HA_path) and os.path.exists(pre_PV_path) and os.path.exists(post_HA_path) and os.path.exists(post_PV_path)):
			continue

		output_dir = os.path.join(data_dir,case,"plot","boundary_PV")
		if not os.path.exists(output_dir):
			os.makedirs(output_dir,exist_ok=True)
		plot_PV(plain_path, pre_HA_path, pre_PV_path, post_PV_path,output_dir)

		output_dir = os.path.join(data_dir,case,"plot","boundary_HA")
		if not os.path.exists(output_dir):
			os.makedirs(output_dir,exist_ok=True)
		plot_HA(plain_path, pre_HA_path, post_HA_path, output_dir)

		exit()

if __name__=="__main__":
	main()