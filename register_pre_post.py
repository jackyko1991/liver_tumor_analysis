import SimpleITK as sitk
import os

def main():
	data_dir = "./data/by_case"

	for case in os.listdir(data_dir):
		linear_tfm = sitk.ReadTransform("D:/projects/liver_tumor/data/by_case/ChoySimWang")

if __name__ == "__main__":
	main():