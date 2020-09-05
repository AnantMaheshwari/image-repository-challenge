import math
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.cluster import KMeans
from scipy.spatial import distance
import ntpath


class ImagesRepoModel:
    """A class to store different views of the image repository"""

    """ arbitrarily chosen global image size, to allow for easy image comparison """
    IMG_WIDTH = 320
    IMG_HEIGHT = 240

    def __validate_image(self, image_path):
        valid_formats = ('png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif')
        if not image_path.lower().endswith(valid_formats):
            raise ValueError
        img = Image.open(image_path)
        img.verify()

    def __define_image_space(self, pic):
        """ Account for comparing greyscale, coloured, and multi-sized images
                        by normalizing all pictures to be RGB formatted with the same size. """
        img = Image.open(pic).convert('RGB')
        img = img.resize((self.IMG_WIDTH, self.IMG_HEIGHT))

        """ flatten pixel values """
        img_converted = np.array(img)
        row = img_converted.ravel()
        row_as_list = np.array(row.tolist())
        return row_as_list

    def __init__(self, image_folder=None, parent=None):
        """ Initialize the image repository using images in image_folder.
        Store names of image to allow for textual searching, and cluster the
        current images to allow for image-based searching """

        self.image_names = []
        self.parent = parent

        for image in image_folder:
            try:
                self.__validate_image(image)
                self.image_names.append(image)
            except (IOError, SyntaxError, ValueError):
                print('Bad image file, not including in repository: ', image)

        """ Construct matrix where there is a row per image, and columns representing pixel values.
            Note that there is 3*IMG_WIDTH*IMG_HEIGHT columns, since each pixel contributes 3 values (RGB). """
        self.df = pd.DataFrame(index=self.image_names, columns=np.arange(3 * self.IMG_WIDTH * self.IMG_HEIGHT))

        for pic in self.image_names:
            pixel_features = self.__define_image_space(pic)
            self.df.loc[pic] = pixel_features

        """ Cluster images such that they can be searched against """
        self.kmeans = KMeans(n_clusters=math.ceil(math.sqrt(len(self.image_names)))).fit(self.df)


    def text_search(self, query_string):
        print("Searching image repository based on inputted text query...")

        image_names = list(filter(lambda k: query_string in ntpath.basename(k), self.image_names))
        if not image_names:
            print("No search results found")
            return self
        print("Found some hits! Now constructing new image repository view with your results...")

        filtered_repo = ImagesRepoModel(image_names, self)
        print("Search results: ")
        print(*filtered_repo.image_names, sep=", ")

        print("You are now in a view of the repository containing only the above search results.")
        return filtered_repo

    def image_search(self, query_image):
        print("Searching image repository for similar images...")

        try:
            self.__validate_image(query_image)
        except (IOError, SyntaxError, ValueError):
            print('Inputted image is not valid: ', query_image)
            return self
        centroids = self.kmeans.cluster_centers_
        labels = self.kmeans.labels_

        pixel_features = self.__define_image_space(query_image)

        min_distance = float('inf')
        cluster_belongs = -1
        for index, centroid in enumerate(centroids):
            dist_to_centroid = distance.euclidean(centroid, pixel_features)
            print("cluster distances were: " + str(dist_to_centroid))
            print("min distance was: " + str(min_distance))
            if dist_to_centroid < min_distance:
                min_distance = dist_to_centroid
                cluster_belongs = index

        search_results = []
        for index, name in enumerate(self.image_names):
            if labels[index] == cluster_belongs:
                search_results.append(name)

        if not search_results:
            print("No search results found")
            return self
        print("Found some hits! Now constructing new image repository view with your results...")

        filtered_repo = ImagesRepoModel(search_results, self)
        print("Search results: ")
        print(*filtered_repo.image_names, sep=", ")

        print("You are now in a view of the repository containing only the above search results.")
        return filtered_repo
