## Python projects

This page introduces some of the Python projects which I developed during the university course _"Multimedia databases"_. 


##### Filter

Implementation of a box filter (blur), a sharpen filter and a median filter for .gif images. A simple GUI (Tkinter) helps to interact with the program.


##### Edge detection (Robinson operator)

_Used libraries: NumPy, scikit-image, SciPy_

Implementation of a compass mask for detecting edges (Robinson operator). Also saves pictures after using other edge detection operators imported from libraries (e.g. Prewitt, Sobel, etc) for comparison. 


##### K-means clustering

_Used libraries: NumPy, Matplotlib_

Small k-means program which takes a given point dataset and plots k centroids with their clusters before and after the k-means calculation. The initial clusters are chosen randomly.


##### Nearest centroid classifier

_Used libraries: NumPy, scikit-image, OpenCV_

The classifier classifies handwritten digits. It is trained and tested with the [MNIST dataset of handwritten digits](http://yann.lecun.com/exdb/mnist/). Histograms of oriented gradients are extracted as features for every picture. 9304 records of the 10k test dataset are correctly classified with this method.
