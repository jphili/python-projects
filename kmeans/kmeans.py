import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
import random

def k_means(centroids, dataset):
    new_centroids2 = []
    # calculate the distance for every point and assign to the cluster with the smallest distance 
    clusters = [[] for i in centroids]      # create cluster
    for point in dataset:
        cluster = None
        distance = 999999999
        for i in xrange(len(centroids)):
            new_distance = euclidean_distance(point, centroids[i])
            if new_distance < distance and new_distance is not 0.0:             # if distance 0.0 -> the data point is the centroid, skip
                distance = new_distance
                cluster = i
        clusters[cluster].append(point)

    # calculate new centroids 
    for cluster in clusters:
        new_centroids2.append(np.mean(cluster, axis=0))
    return new_centroids2, clusters


def euclidean_distance(p1, p2):
    dist = sqrt(np.sum((p1-p2)**2))
    return dist


def plot_everything(centroids, initial_centroids, initial_clusters, clusters):
    fig, ax = plt.subplots(2, sharex=True)
    for i in xrange(len(centroids)):
        color = np.random.rand(3, )
        ax[0].plot(initial_centroids[i][0], initial_centroids[i][1], linestyle='None', marker='x', markersize='15', c=color)
        for point in initial_clusters[i]:
            ax[0].plot(point[0], point[1], linestyle='None', marker='o', c=color)

        ax[1].plot(centroids[i][0], centroids[i][1], linestyle='None', marker='x', markersize='15', c=color)
        for point in clusters[i]:
            ax[1].plot(point[0], point[1], linestyle='None', marker='o', c=color)

    ax[0].set_title("Scatterplot with initial clusters")
    ax[1].set_title("Scatterplot with final clusters")
    plt.show()


k = np.int(raw_input("\nHow many clusters?\n"))

# hardcoded input from course assignment
dataset = np.array([[1,1],
                    [1,3],
                    [1,4],
                    [2,2],
                    [4,10],
                    [4,12],
                    [5,9],
                    [5,12],
                    [6,8],
                    [6,9],
                    [6,10],
                    [6,11],
                    [7,8],
                    [7,10],
                    [8,9],
                    [8,10],
                    [10,3],
                    [11,2],
                    [11,3],
                    [11,4]
                   ])

# randomly create initial clusters
initial_centroids = random.sample(dataset, k)
centroids = initial_centroids
new_centroids, initial_clusters = k_means(initial_centroids, dataset)
clusters = initial_clusters


while not np.array_equal(new_centroids, centroids):
    centroids = new_centroids
    new_centroids, clusters = k_means(centroids, dataset)

if (len(centroids[0])) == 2:
    plot_everything(new_centroids, initial_centroids, initial_clusters, clusters)


print "Final centroids: " + str(centroids)
