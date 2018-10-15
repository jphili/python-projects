from __future__ import division

import numpy as np
from struct import unpack
from skimage import feature, exposure
import cv2 as cv


class NearestCentroidClassifier:
    def __init__(self, images, labels):
        self.images = images
        self.labels = labels
        self.num_images = len(images)

    def euclidean_distance(self, p1, p2):
        dist = np.sqrt(np.sum((p1 - p2) ** 2))
        return dist

    def train(self):
        classes = np.unique(self.labels)
        self.classes = classes

        centroids = np.empty((classes.shape[0], self.images.shape[1]))
        label_to_image = []                                     # master list

        for cl in classes:
            img_label = []                                      # create a list for each class (for each digit)
            for j in xrange(0, self.num_images):
                if self.labels[j] == cl:                        # if the label equals the picture label 
                    img_label.append(self.images[j])            # append to list
            label_to_image.append(img_label)                    # append to master list

        for i in xrange(0, len(classes)):  # calculate mean for centroids
            centroids[i] = np.mean(label_to_image[i], axis=0)


        self.centroids = centroids

        # save training data
        #np.savez('centroids.npz', centroids=centroids, labels=self.labels)


    def classify(self, images):
        classified = []
        for image in images:                                       
            smallest_dist = 99999999                                
            cl = None                                               
            for i, centroid in enumerate(self.centroids):           
                dist = np.sqrt(np.sum((image - centroid) ** 2))     # calculate the distance of the picture to each centroid
                if dist < smallest_dist:
                    smallest_dist = dist
                    cl = i
            classified.append([cl])                                 # append classified picture

        return classified



    def set_data(self, centroids, labels):
        self.centroids = centroids
        self.labels = labels


def get_data(file_labels, file_images ):

    # Label dimensions
    f_label = open(file_labels, mode='rb')
    magic_number_label = f_label.read(4)
    num_labels = f_label.read(4)
    num_labels = unpack(">I", num_labels)[0]


    # Picture dimensions
    f_img = open(file_images, mode='rb')
    magic_number_image = f_img.read(4)
    num_images = f_img.read(4)
    num_images = unpack('>I', num_images)[0]             # > for Big Endian, I = unsigned integer
    num_rows = f_img.read(4)
    num_rows = unpack('>I', num_rows)[0]
    num_cols = f_img.read(4)
    num_cols = unpack('>I', num_cols)[0]


    # read labels and pictures
    images = np.zeros((num_images, num_rows, num_cols))
    labels = np.zeros((num_labels, 1), dtype=np.uint8)
    images_features = []

    for i in np.arange(num_images):
        for u in np.arange(num_rows):
            for v in np.arange(num_cols):
                pixel = f_img.read(1)
                pixel = unpack('>B', pixel)[0]
                pixel = pixel/255.0
                images[i][u][v] = pixel

        image = deskew(images[i])                               # deskew 
        features = feature.hog(image, orientations=9, pixels_per_cell=(7, 7), cells_per_block=(4, 4), visualise=False, block_norm='L1-sqrt', feature_vector=True)
        images_features.append(features)
        label = f_label.read(1)
        labels[i] = unpack('>B', label)[0]

    f_label.close()
    f_img.close()
    images_features = np.array(images_features)

    return images_features, labels


# from docs.opencv.org: Python Tutorials; deskew numbers
def deskew(img):
    affine_flags = cv.WARP_INVERSE_MAP | cv.INTER_LINEAR
    SZ = 28
    m = cv.moments(img)
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11']/m['mu02']
    M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
    img = cv.warpAffine(img,M,(SZ, SZ),flags=affine_flags)
    return img



def main():
    trained_data = np.DataSource()

    if trained_data.exists('centroids.npz'):
        print "Read already trained data...\n"
        with np.load('centroids.npz') as data:
            centroids = data['centroids']
            labels = data['labels']
            classifier = NearestCentroidClassifier(centroids, labels)
            classifier.set_data(centroids, labels)
    else:
        print "Reading data...\n"
        images, labels = get_data('train-labels.idx1-ubyte', 'train-images.idx3-ubyte')

        classifier = NearestCentroidClassifier(images, labels)

        print "Train classifier...\n"
        classifier.train()

    test_images, test_labels = get_data('t10k-labels.idx1-ubyte', 't10k-images.idx3-ubyte')
    print "Classify test data...\n"

    classified_images = classifier.classify(test_images)

    right = 0

    print "Check results...\n"
    for i in xrange(0, len(classified_images)):
        if classified_images[i] == test_labels[i]:
            right = right +1

    print str(right/len(classified_images)*100) + " percent of the test data were classified correctly.\n"
    print "\nFrom 10,000 digits, " + str(right) + " were classified correctly."



if __name__ == '__main__':
    main()