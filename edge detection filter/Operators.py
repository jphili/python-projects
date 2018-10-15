from scipy import ndimage, misc
import numpy as np
from skimage import filters, io, util
from math import pi


class Operators:
    def __init__(self, image, name):
        self.image = image
        self.image_name = name


    def prewitt(self):
        prewitt = filters.prewitt(self.image)
        io.imsave(str('prewitt_' + self.image_name), util.invert(prewitt))


    def sobel(self):
        sobel = filters.sobel(self.image)
        io.imsave(str('sobel_' + self.image_name), util.invert(sobel))


    def roberts(self):
        roberts = filters.roberts(self.image)
        io.imsave(str('roberts_' + self.image_name), util.invert(roberts))


    def laplacian_of_gaussian(self, name):
        image = ndimage.imread(name)
        l_o_g1 = ndimage.gaussian_laplace(image, sigma=0.7, mode='nearest')
        l_o_g2 = ndimage.gaussian_laplace(image, sigma=0.8, mode='nearest')
        l_o_g3 = ndimage.gaussian_laplace(image, sigma=1.0, mode='nearest')
        l_o_g4 = ndimage.gaussian_laplace(image, sigma=1.5, mode='nearest')
        l_o_g5 = ndimage.gaussian_laplace(image, sigma=2.0, mode='nearest')

        misc.imsave(str('l_o_g07_' + self.image_name), l_o_g1)
        misc.imsave(str('l_o_g08_' + self.image_name), l_o_g2)
        misc.imsave(str('l_o_g10_' + self.image_name), l_o_g3)
        misc.imsave(str('l_o_g15_' + self.image_name), l_o_g4)
        misc.imsave(str('l_o_g20_' + self.image_name), l_o_g5)

    # Implementation of Robinson operator (compass mask)
    def robinson(self, name):
        image = ndimage.imread(name)

        h0_3 = np.array([
            [[-1.0, 0.0, 1.0],
            [-2.0, 0.0, 2.0],
            [-1.0, 0.0, 1.0]],

            [[-2.0, -1.0, 0.0],
            [-1.0, 0.0, 1.0],
            [0.0, 1.0, 2.0]],

            [[-1.0, -2.0, -1.0],
            [0.0, 0.0, 0.0],
            [1.0, 2.0, 1.0]],

            [[0.0, -1.0, -2.0],
            [1.0, 0.0, -1.0],
            [2.0, 1.0, 0.0]]
        ])

        h4_7 = np.negative(h0_3)
        e_k = np.zeros(image.shape)

        h0_7 = np.concatenate((h0_3, h4_7), axis=0)

        for filter in h0_7:
            e_k = np.maximum(ndimage.filters.convolve(image, filter), e_k)


        k_k = image
        for v in range(0, image.shape[1]):
            for u in range(0, image.shape[0]):
                k_k[u][v] = pi/4*e_k[u][v]

        misc.imsave(str('robinson_' + self.image_name), util.invert(k_k))


def main():

    images = ['testchelsea.png', 'testcoins.png']

    for image_name in images:
        image = io.imread(image_name)
        operators = Operators(image, image_name)
        operators.sobel()
        operators.prewitt()
        operators.roberts()
        operators.laplacian_of_gaussian(image_name)
        operators.robinson(image_name)


if __name__ == '__main__':
    main()