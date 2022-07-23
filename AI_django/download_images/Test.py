from __future__ import division

import os


import rasterio as rio

import argparse
import numpy as np


import torch
import torch.backends.cudnn as cudnn


import cv2
# from engine.engine import Engine

def pca_process(data):

    from sklearn.decomposition import PCA, IncrementalPCA
    pca = PCA()
    data = data.transpose(1, 2, 0)
    first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, towelth, thirteenth = cv2.split(data)
    a = pca.fit_transform(first)

    'Evaluate variance'
    var_cumu = np.cumsum(pca.explained_variance_ratio_) * 100
    'How many PCs explain 95% of the variance?'
    k = np.argmax(var_cumu > 95)
    k = k + 50

    ipca = IncrementalPCA(n_components=k)
    a_re = ipca.inverse_transform(ipca.fit_transform(first))
    b_re = ipca.inverse_transform(ipca.fit_transform(second))
    c_re = ipca.inverse_transform(ipca.fit_transform(third))
    d_re = ipca.inverse_transform(ipca.fit_transform(fourth))
    e_re = ipca.inverse_transform(ipca.fit_transform(fifth))
    f_re = ipca.inverse_transform(ipca.fit_transform(sixth))
    g_re = ipca.inverse_transform(ipca.fit_transform(seventh))
    h_re = ipca.inverse_transform(ipca.fit_transform(eighth))
    l_re = ipca.inverse_transform(ipca.fit_transform(ninth))
    m_re = ipca.inverse_transform(ipca.fit_transform(tenth))
    n_re = ipca.inverse_transform(ipca.fit_transform(eleventh))
    p_re = ipca.inverse_transform(ipca.fit_transform(towelth))
    q_re = ipca.inverse_transform(ipca.fit_transform(thirteenth))
    newimage = np.stack((a_re, b_re, c_re, d_re, e_re, f_re, g_re, h_re, l_re, m_re, n_re, p_re, q_re))

    '''Add NDBI - NDVI - NDWI to dataset'''
    NDBI_index = (newimage[8] - newimage[6]) / (newimage[8] + newimage[6])
    NDWI_index = (newimage[1] - newimage[6]) / (newimage[1] + newimage[6])
    NDVI_index = (newimage[6] - newimage[2]) / (newimage[6] + newimage[2])
    image = np.stack((a_re, b_re, c_re, d_re, e_re, f_re, g_re, h_re, l_re, m_re, n_re, p_re, q_re, NDWI_index, NDVI_index, NDBI_index))

    # plt.figure(figsize=(20,10))
    # plt.subplot(1,3,1)
    # plt.imshow(image[15])
    # plt.subplot(1, 3, 2)
    # plt.imshow(image[14])
    # plt.subplot(1, 3, 3)
    # plt.imshow(image[13])
    # plt.waitforbuttonpress()
    return image



parser = argparse.ArgumentParser()
# with Engine(custom_parser=parser) as engine:
args = parser.parse_args()
cudnn.benchmark = True
seed = 1234
torch.manual_seed(seed)

'Load Model'
model = torch.load('/home/sedreh-dinvarzadeh/Desktop/Teacher-StudentModel.pth')
model.eval()


'Images List'
input_list = ['sentinel2_0.tif', 'sentinel2_1.tif', 'sentinel2_2.tif','sentinel2_3.tif','sentinel2_4.tif',
              'sentinel2_5.tif']


for inp in range(len(input_list)):
    os.chdir("/home/sedreh-dinvarzadeh/Desktop")
    img = rio.open(input_list[inp])
    transform = img.transform
    img = img.read()

    'PCA'
    img = pca_process(img)
    img = torch.from_numpy(img).to(torch.float32)

    '''Getting the Product'''
    output = model(img[None, :].to('cpu'), step=1)

    output = torch.argmax(output, 1)
    output = output.detach().to('cpu').numpy().astype('float32')
    print(output.shape, output.dtype)



    '''Save the product as .tif'''
    os.chdir("/home/sedreh-dinvarzadeh/Desktop/Result")
    new_dataset = rio.open(f"product_{str(inp)}.tif", 'w', driver='GTiff',
                           height=308, width=416,
                           count=1, dtype=str(output.dtype),
                           crs='+proj=utm +zone=10 +ellps=GRS80 +datum=NAD83 +units=m +no_defs',
                           transform=transform)
    new_dataset.write(output)
    new_dataset.close()













