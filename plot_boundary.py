import os
from tqdm import tqdm
import SimpleITK as sitk
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_all(
		plain_path, 
		pre_HA_path, 
		pre_PV_path, 
		post_HA_path, 
		post_PV_path, 
		pre_HA_label_path, 
		pre_PV_label_path, 
		post_HA_label_path, 
		post_PV_label_path, 
		output_dir):
	reader = sitk.ImageFileReader()
	reader.SetFileName(plain_path)
	plain = reader.Execute()
	reader.SetFileName(pre_HA_path)
	pre_HA = reader.Execute()
	reader.SetFileName(pre_PV_path)
	pre_PV = reader.Execute()
	reader.SetFileName(post_HA_path)
	post_HA = reader.Execute()
	reader.SetFileName(post_PV_path)
	post_PV = reader.Execute()
	reader.SetFileName(pre_HA_label_path)
	pre_HA_label = reader.Execute()
	reader.SetFileName(pre_PV_label_path)
	pre_PV_label = reader.Execute()
	reader.SetFileName(post_HA_label_path)
	post_HA_label = reader.Execute()
	reader.SetFileName(post_PV_label_path)
	post_PV_label = reader.Execute()

	intensityWindowingFilter = sitk.IntensityWindowingImageFilter()
	intensityWindowingFilter.SetOutputMaximum(255)
	intensityWindowingFilter.SetOutputMinimum(0)
	intensityWindowingFilter.SetWindowMaximum(300);
	intensityWindowingFilter.SetWindowMinimum(0);
	plain = intensityWindowingFilter.Execute(plain)
	pre_HA = intensityWindowingFilter.Execute(pre_HA)
	pre_PV = intensityWindowingFilter.Execute(pre_PV)
	post_HA = intensityWindowingFilter.Execute(post_HA)
	post_PV = intensityWindowingFilter.Execute(post_PV)

	plain_np = sitk.GetArrayFromImage(plain)
	pre_HA_np = sitk.GetArrayFromImage(pre_HA)
	pre_PV_np = sitk.GetArrayFromImage(pre_PV)
	post_HA_np = sitk.GetArrayFromImage(post_HA)
	post_PV_np = sitk.GetArrayFromImage(post_PV)

	pre_HA_label_np = sitk.GetArrayFromImage(pre_HA_label)
	pre_PV_label_np = sitk.GetArrayFromImage(pre_PV_label)
	post_HA_label_np = sitk.GetArrayFromImage(post_HA_label)
	post_PV_label_np = sitk.GetArrayFromImage(post_PV_label)

	for z in tqdm(range(plain_np.shape[0])):
		# if not (z == 32):
		# 	continue

		plain_slice = plain_np[z,:,:]
		pre_HA_slice = pre_HA_np[z,:,:]
		pre_PV_slice = pre_PV_np[z,:,:]
		post_HA_slice = post_HA_np[z,:,:]
		post_PV_slice = post_PV_np[z,:,:]

		pre_HA_label_slice = pre_HA_label_np[z,:,:]
		pre_PV_label_slice = pre_PV_label_np[z,:,:]
		post_HA_label_slice = post_HA_label_np[z,:,:]
		post_PV_label_slice = post_PV_label_np[z,:,:]

		dpi = 100
		shape=np.shape(plain_slice)[0:2][::-1]
		size = [float(i)/dpi for i in shape]
		size[0] = size[0]*5

		fig = plt.figure()
		fig.set_size_inches(size)

		ax = plt.Axes(fig,[0,0,0.2,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(plain_slice,cmap="gray",origin='lower')
		CS_pre_HA = ax.contour(pre_HA_label_slice,[0,1], colors='r',origin='lower',linewidths=1)
		CS_pre_PV = ax.contour(pre_PV_label_slice,[0,1], colors='lawngreen',origin='lower',linewidths=1)
		CS_post_HA = ax.contour(post_HA_label_slice,[0,1], colors='dodgerblue',origin='lower',linewidths=1)
		CS_post_PV = ax.contour(post_PV_label_slice,[0,1], colors='yellow',origin='lower',linewidths=1)

		CS_pre_HA.collections[0].set_label("Pre HA")
		CS_pre_PV.collections[0].set_label("Pre PV")
		CS_post_HA.collections[0].set_label("Post HA")
		CS_post_PV.collections[0].set_label("Post PV")

		leg = ax.legend(loc='upper right',frameon=False)
		for text in leg.get_texts():
			plt.setp(text, color = 'w')

		ax = plt.Axes(fig,[0.2,0,0.2,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(pre_HA_slice,cmap="gray",origin='lower')
		CS_pre_HA = ax.contour(pre_HA_label_slice,[0,1], colors='r',origin='lower',linewidths=1)

		ax = plt.Axes(fig,[0.4,0,0.2,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(pre_PV_slice,cmap="gray",origin='lower')
		CS_pre_PV = ax.contour(pre_PV_label_slice,[0,1], colors='lawngreen',origin='lower',linewidths=1)

		ax = plt.Axes(fig,[0.6,0,0.2,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(post_HA_slice,cmap="gray",origin='lower')
		CS_post_HA = ax.contour(post_HA_label_slice,[0,1], colors='dodgerblue',origin='lower',linewidths=1)

		ax = plt.Axes(fig,[0.8,0,0.2,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(post_PV_slice,cmap="gray",origin='lower')
		CS_post_PV = ax.contour(post_PV_label_slice,[0,1], colors='yellow',origin='lower',linewidths=1)

		if z < 9:
			fig.savefig(os.path.join(output_dir,"0" + str(z+1) + ".jpg"),dpi=dpi)
		else:
			fig.savefig(os.path.join(output_dir,str(z+1) + ".jpg"),dpi=dpi)

		plt.close(fig)


def plot_HA(plain_path, pre_HA_path, post_HA_path, pre_HA_label_path, post_HA_label_path, output_dir):
	reader = sitk.ImageFileReader()
	reader.SetFileName(plain_path)
	plain = reader.Execute()
	reader.SetFileName(pre_HA_path)
	pre_HA = reader.Execute()
	reader.SetFileName(post_HA_path)
	post_HA = reader.Execute()
	reader.SetFileName(pre_HA_label_path)
	pre_HA_label = reader.Execute()
	reader.SetFileName(post_HA_label_path)
	post_HA_label = reader.Execute()


	intensityWindowingFilter = sitk.IntensityWindowingImageFilter()
	intensityWindowingFilter.SetOutputMaximum(255)
	intensityWindowingFilter.SetOutputMinimum(0)
	intensityWindowingFilter.SetWindowMaximum(300);
	intensityWindowingFilter.SetWindowMinimum(0);
	plain = intensityWindowingFilter.Execute(plain)
	pre_HA = intensityWindowingFilter.Execute(pre_HA)
	post_HA = intensityWindowingFilter.Execute(post_HA)

	plain_np = sitk.GetArrayFromImage(plain)
	pre_HA_np = sitk.GetArrayFromImage(pre_HA)
	post_HA_np = sitk.GetArrayFromImage(post_HA)

	pre_HA_label_np = sitk.GetArrayFromImage(pre_HA_label)
	post_HA_label_np = sitk.GetArrayFromImage(post_HA_label)

	for z in tqdm(range(plain_np.shape[0])):
		plain_slice = plain_np[z,:,:]
		pre_HA_slice = pre_HA_np[z,:,:]
		post_HA_slice = post_HA_np[z,:,:]
		pre_HA_label_slice = pre_HA_label_np[z,:,:]
		post_HA_label_slice = post_HA_label_np[z,:,:]

		dpi = 100
		shape=np.shape(plain_slice)[0:2][::-1]
		size = [float(i)/dpi for i in shape]
		size[0] = size[0]*3

		fig = plt.figure()
		fig.set_size_inches(size)
		ax = plt.Axes(fig,[0,0,0.333,1])
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

		ax = plt.Axes(fig,[0.333,0,0.333,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(pre_HA_slice,cmap="gray",origin='lower')
		CS_pre_HA = ax.contour(pre_HA_label_slice,[0,1], colors='r',origin='lower',linewidths=1)

		ax = plt.Axes(fig,[0.666,0,0.333,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(post_HA_slice,cmap="gray",origin='lower')
		CS_pre_HA = ax.contour(post_HA_label_slice,[0,1], colors='r',origin='lower',linewidths=1)

		if z < 9:
			fig.savefig(os.path.join(output_dir,"0" + str(z+1) + ".jpg"),dpi=dpi)
		else:
			fig.savefig(os.path.join(output_dir,str(z+1) + ".jpg"),dpi=dpi)

		plt.close(fig)

def plot_PV(plain_path, pre_HA_path, pre_PV_path, post_PV_path, pre_HA_label_path, pre_PV_label_path, post_PV_label_path, output_dir):
	reader = sitk.ImageFileReader()
	reader.SetFileName(plain_path)
	plain = reader.Execute()
	reader.SetFileName(pre_HA_path)
	pre_HA = reader.Execute()
	reader.SetFileName(pre_PV_path)
	pre_PV = reader.Execute()
	reader.SetFileName(post_PV_path)
	post_PV = reader.Execute()
	reader.SetFileName(pre_HA_label_path)
	pre_HA_label = reader.Execute()
	reader.SetFileName(pre_PV_label_path)
	pre_PV_label = reader.Execute()
	reader.SetFileName(post_PV_label_path)
	post_PV_label = reader.Execute()

	intensityWindowingFilter = sitk.IntensityWindowingImageFilter()
	intensityWindowingFilter.SetOutputMaximum(255)
	intensityWindowingFilter.SetOutputMinimum(0)
	intensityWindowingFilter.SetWindowMaximum(300);
	intensityWindowingFilter.SetWindowMinimum(0);
	plain = intensityWindowingFilter.Execute(plain)
	pre_HA = intensityWindowingFilter.Execute(pre_HA)
	pre_PV = intensityWindowingFilter.Execute(pre_PV)
	post_PV = intensityWindowingFilter.Execute(post_PV)

	plain_np = sitk.GetArrayFromImage(plain)
	pre_HA_np = sitk.GetArrayFromImage(pre_HA)
	pre_PV_np = sitk.GetArrayFromImage(pre_PV)
	post_PV_np = sitk.GetArrayFromImage(post_PV)

	pre_HA_label_np = sitk.GetArrayFromImage(pre_HA_label)
	pre_PV_label_np = sitk.GetArrayFromImage(pre_PV_label)
	post_PV_label_np = sitk.GetArrayFromImage(post_PV_label)

	for z in tqdm(range(plain_np.shape[0])):
		# if not (z == 32):
		# 	continue

		plain_slice = plain_np[z,:,:]
		pre_HA_slice = pre_HA_np[z,:,:]
		pre_PV_slice = pre_PV_np[z,:,:]
		post_PV_slice = post_PV_np[z,:,:]

		pre_HA_label_slice = pre_HA_label_np[z,:,:]
		pre_PV_label_slice = pre_PV_label_np[z,:,:]
		post_PV_label_slice = post_PV_label_np[z,:,:]

		dpi = 100
		shape=np.shape(plain_slice)[0:2][::-1]
		size = [float(i)/dpi for i in shape]
		size[0] = size[0]*4

		fig = plt.figure()
		fig.set_size_inches(size)

		ax = plt.Axes(fig,[0,0,0.25,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(plain_slice,cmap="gray",origin='lower')
		CS_pre_HA = ax.contour(pre_HA_label_slice,[0,1], colors='r',origin='lower',linewidths=1)
		CS_pre_PV = ax.contour(pre_PV_label_slice,[0,1], colors='lawngreen',origin='lower',linewidths=1)
		CS_post_PV = ax.contour(post_PV_label_slice,[0,1], colors='dodgerblue',origin='lower',linewidths=1)

		CS_pre_HA.collections[0].set_label("Pre HA")
		CS_pre_PV.collections[0].set_label("Pre PV")
		CS_post_PV.collections[0].set_label("Post PV")

		leg = ax.legend(loc='upper right',frameon=False)
		for text in leg.get_texts():
			plt.setp(text, color = 'w')

		ax = plt.Axes(fig,[0.25,0,0.25,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(pre_HA_slice,cmap="gray",origin='lower')
		CS_pre_HA = ax.contour(pre_HA_label_slice,[0,1], colors='r',origin='lower',linewidths=1)

		ax = plt.Axes(fig,[0.5,0,0.25,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(pre_PV_slice,cmap="gray",origin='lower')
		CS_pre_PV = ax.contour(pre_PV_label_slice,[0,1], colors='lawngreen',origin='lower',linewidths=1)

		ax = plt.Axes(fig,[0.75,0,0.25,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(post_PV_slice,cmap="gray",origin='lower')
		CS_post_PV = ax.contour(post_PV_label_slice,[0,1], colors='dodgerblue',origin='lower',linewidths=1)

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
		pre_HA_path = os.path.join(data_dir,case,"pre","nii_reg","HA","temporal_mIP.nii.gz")
		pre_PV_path = os.path.join(data_dir,case,"pre","nii_reg","PV","temporal_mIP.nii.gz")
		post_HA_path = os.path.join(data_dir,case,"post","nii_reg_pre","HA","temporal_mIP.nii.gz")
		post_PV_path = os.path.join(data_dir,case,"post","nii_reg_pre","PV","temporal_mIP.nii.gz")
		pre_HA_label_path = os.path.join(data_dir,case,"pre","nii_reg","HA","tumor_original_space.nii.gz")
		pre_PV_label_path = os.path.join(data_dir,case,"pre","nii_reg","PV","tumor_original_space.nii.gz")
		post_HA_label_path = os.path.join(data_dir,case,"post","nii_reg_pre","HA","tumor_original_space.nii.gz")
		post_PV_label_path = os.path.join(data_dir,case,"post","nii_reg_pre","PV","tumor_original_space.nii.gz")
		
		if not (os.path.exists(plain_path) and os.path.exists(pre_HA_path) and os.path.exists(pre_PV_path) and os.path.exists(post_HA_path) and os.path.exists(post_PV_path)):
			continue

		output_dir = os.path.join(data_dir,case,"plot","boundary")
		if not os.path.exists(output_dir):
			os.makedirs(output_dir,exist_ok=True)
		plot_all(plain_path, pre_HA_path, pre_PV_path, post_HA_path, post_PV_path, 
			pre_HA_label_path, pre_PV_label_path, post_HA_label_path, post_PV_label_path,output_dir)

		output_dir = os.path.join(data_dir,case,"plot","boundary_PV")
		if not os.path.exists(output_dir):
			os.makedirs(output_dir,exist_ok=True)
		plot_PV(plain_path, pre_HA_path, pre_PV_path, post_PV_path, pre_HA_label_path, pre_PV_label_path, post_PV_label_path,output_dir)

		output_dir = os.path.join(data_dir,case,"plot","boundary_HA")
		if not os.path.exists(output_dir):
			os.makedirs(output_dir,exist_ok=True)
		plot_HA(plain_path, pre_HA_path, post_HA_path, pre_HA_label_path, post_HA_label_path, output_dir)

if __name__=="__main__":
	main()