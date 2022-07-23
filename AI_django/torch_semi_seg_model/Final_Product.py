from __future__ import division
import os
from collections import OrderedDict
import rasterio
import numpy as np
import torch
from torch import nn
from .network import Network
import cv2
from sklearn.decomposition import PCA, IncrementalPCA
from glob import glob


def pca_process(data):
    data = data.transpose(1, 2, 0)
    first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelve, thirteenth = cv2.split(data)

    pca = PCA()
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
    p_re = ipca.inverse_transform(ipca.fit_transform(twelve))
    q_re = ipca.inverse_transform(ipca.fit_transform(thirteenth))

    newimage = np.stack((a_re, b_re, c_re, d_re, e_re, f_re, g_re, h_re, l_re, m_re, n_re, p_re, q_re))

    '''Add NDBI - NDVI - NDWI to dataset'''
    NDBI_index = (newimage[8] - newimage[6]) / (newimage[8] + newimage[6])
    NDWI_index = (newimage[1] - newimage[6]) / (newimage[1] + newimage[6])
    NDVI_index = (newimage[6] - newimage[2]) / (newimage[6] + newimage[2])
    image = np.stack((a_re, b_re, c_re, d_re, e_re, f_re, g_re, h_re, l_re, m_re, n_re, p_re, q_re, NDWI_index, NDVI_index, NDBI_index))

    return image


def semi_seg_product(path):
    ai_images = os.path.join(path, 'images/AI_image')
    result_images = os.path.join(path, 'images/AI_Result')
    Tsmodel_path = os.path.join(path, 'torch_semi_seg_model/TSmodel.pth')

    batch = nn.BatchNorm2d
    seed = 123
    torch.manual_seed(seed)
    model = Network(num_classes=11, criterion=nn.CrossEntropyLoss, pretrained_model=None, norm_layer=batch)

    state_dict = torch.load(Tsmodel_path, map_location='cpu')

    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = k[7:]  # remove `module.`
        new_state_dict[name] = v
    # load params
    model.load_state_dict(new_state_dict)
    model.eval()

    os.chdir(ai_images)

    tiles = ['T39SVV', 'T39SVA', 'T39SWV', 'T39SWA']
    for tile in tiles:
        for i in range(600):
            ai_image = []
            images = sorted(glob(f'{i}_{tile}_*'))
            print(images)
            for image in images:
                dataset = rasterio.open(image)
                transform = dataset.transform
                crs = dataset.crs
                ai_image.append(dataset.read(1))
            img = np.array(ai_image)

            'PCA'
            img = pca_process(img)
            img = torch.from_numpy(img).to(torch.float32)

            '''Getting the Product'''
            # semi_seg_product(img[None, :])
            output = model(img[None, :], step=1)
            output = torch.argmax(output, 1)
            output = output.detach().to('cpu').numpy().astype('uint16')

            '''Save the product as .jp2'''
            if not os.path.isdir(result_images):
                os.mkdir(result_images)
            os.chdir(result_images)
            print(f'product_{i}_{tile}.tif')
            new_dataset = rasterio.open(f"product_{str(i)}_{tile}.tif", 'w', driver='GTiff',
                                   height=366, width=549,
                                   count=1, dtype=str(output.dtype),
                                   crs=crs,
                                   transform=transform)
            new_dataset.write(output)
            new_dataset.close()
            os.chdir(ai_images)

        print(f'labels of {tile} is created')





