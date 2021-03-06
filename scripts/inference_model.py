import torch
import time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os 

from sklearn.metrics import confusion_matrix, f1_score

import MLP

def load_image(fname, imw, imh):
	img = Image.open(fname).resize((imw, imh))

	a = np.asarray(img).transpose(2,0,1).astype(np.float32)/255.
	return a, img

def png2array(lfile_array, imw, imh):
	a = np.zeros((3, imh, imw), dtype=np.float32)
	for x in range(imw):
		for y in range(imh):
			if (lfile_array[y][x] == 50):
				a[0][y][x] = 1
			elif (lfile_array[y][x] == 225):
				a[1][y][x] = 1
	return a

def eval_image(fname, thre):
	imw = 320
	imh = 240
	testx = np.zeros((0, 3, imh, imw), dtype=np.float32)

	a, img = load_image(fname, imw, imh)
	a1 = np.expand_dims(a,axis=0)

	testx = np.append(testx, a1, axis=0)

	t0 = time.time()
	testy = model(torch.FloatTensor(testx))
	print(f"testy : {testy.shape}")
	print('forward time [s]: ' + str(time.time()-t0))

	imd = Image.new('RGB', (imw*3, imh))
    
	thimg_g = (testy.to(cpu).detach().numpy()[0][0] > thre) * 255
	thimg_w = (testy.to(cpu).detach().numpy()[0][1] > thre) * 255

	print(f'max {np.max(thimg_g)}')
	print(f'min {np.min(thimg_g)}')

	print(f'max {np.max(thimg_w)}')
	print(f'min {np.min(thimg_w)}')

	testy_np = ((testy.to(cpu).detach().numpy() > thre) * 255) / 255

	lfile = os.path.splitext(fname)[0] + '_label.png'
	l_img = Image.open(lfile).resize((imw, imh))
	a = np.asarray(l_img).astype(np.float32)
	a = a.astype(np.int32)
	#print(a)
	a = png2array(a, imw, imh)
	a1 = np.expand_dims(a,axis=0)
	#print(f"a1 : {a1}")

	target, pred = a1.reshape(-1), testy_np.reshape(-1)

	print(f"cm : {confusion_matrix(target, pred)}")
	F_score = f1_score(target, pred)
	print(f"F_score : {F_score}")

	thimg_g = thimg_g.astype(np.uint8)
	thimg_w = thimg_w.astype(np.uint8)

	thimg_g = Image.fromarray(thimg_g).convert('L')
	thimg_w = Image.fromarray(thimg_w).convert('L')

	imd.paste(img, (0,0))
	imd.paste(thimg_g, (imw, 0))
	imd.paste(thimg_w, (imw*2, 0))
	plt.figure(figsize=(16,9))
	plt.imshow(imd)
	plt.show()

cpu = torch.device("cpu")

model_path = "wl_model.pt"
#model_path = "220109_1000_wl_model.pt"
#model_path = "1000_model.pt"
#model_path = "/home/citbrains/Dan/soccerfield_detector/scripts/weights/220110_weights_2/wl_model.pt"

model = MLP.MLP(4, 3)
model.load_state_dict(torch.load(model_path))
model.eval()

#eval_image('/home/citbrains/Dan/000007.jpg', 0.35)
eval_image('/home/citbrains/Dan/100_test/000020.jpg', 0.35)
eval_image('/home/citbrains/Dan/100_test/000051.jpg', 0.35)
eval_image('/home/citbrains/Dan/100_test/000065.jpg', 0.35)
eval_image('/home/citbrains/Dan/100_test/000071.jpg', 0.35)
eval_image('/home/citbrains/Dan/100_test/000246.jpg', 0.35)
eval_image('/home/citbrains/Dan/100_test/000256.jpg', 0.35)
eval_image('/home/citbrains/Dan/100_test/000278.jpg', 0.35)
eval_image('/home/citbrains/Dan/100_test/000314.jpg', 0.35)
eval_image('/home/citbrains/Dan/100_test/000131.jpg', 0.35)
eval_image('/home/citbrains/Dan/100_test/000143.jpg', 0.35)
eval_image('/home/citbrains/Dan/100_test/000166.jpg', 0.35)
eval_image('/home/citbrains/Dan/100_test/000169.jpg', 0.35)
#eval_image('/home/citbrains/Dan/000026.jpg', 0.4)
#eval_image('/home/citbrains/Dan/000039.jpg', 0.4)
#eval_image('/home/citbrains/Dan/000028.jpg', 0.4)

