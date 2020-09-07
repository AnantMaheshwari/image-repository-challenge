# Shopify Challenge: Image Repository


## Overview

This program provides a command line interface to interact with an image repository. 
The main focus is supporting searching the image repository using both **query strings** and **query images**, and searching at multiple levels (e.g. searching within previous search results). As well, through the use of an XOR-based hashing scheme, image corruption can be identified.
## Usage
We will use the iris flower dataset (a small subset) to show off some features. This contains a mix of daisy, dandelion, rose, sunflower and tulip pictures :)

```terminal
python ImageRepoView.py /path/to/folder/with/images
Building image repository and clustering images for searching, wait a few moments...
```

Upon startup, all the images in the passed in folder */path/to/folder/with/images* are clustered (KMeans) using their pixel values such that they can be efficiently searched against. As well, hashes of image pixels are computed to allow image corruption identification.
The same menu items are available to perform a search on the results from the previous search to further refine the search results.

```terminal
Type "search text" to search within the current view of the image repository
Type "search images" to search within the current view of the image repository
Type "return" to get back to the previous search result
Type "return home" to get back to the original image repository
Type "check for corruption" to check whether any images in the current view of the repository have been modified
```

**search text**: Searches the repository using the provided query string against all the image file names (checking if the query is a substring of any image file names), and finds any search hits.

**search images**: Searches the repository using the query image path input by the user, and finds any "similar" images in the repository (KMeans Clustering is used for the search).

**return**: Return to the previous search result (zoom out of current search level)

**return home**: Return to the original view of the image repository

**check for corruption**: Check if any image in the current view of the repository has been corrupted. This is achieved by computing a hash (XOR-based) of the image pixels at each level of the image repository,and comparing the current hash with the current level's hash to ensure the picture has not been modified.

```terminal
$search text
Type the query text string you wish to search with
$ tulip
Searching image repository based on inputted text query: tulip
Found some hits! Now constructing new image repository view with your results...
6 Search Result(s): 
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6770436217_281da51e49_n.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6539831765_c21b68910e_n.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/SCARY_tulip_6808860548_53796b90ca_n.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6808860548_53796b90ca_n.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6325571510_7544b27e57_n.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6799076717_575944af91_m.jpg
You are now in a view of the repository containing only the above search results.
```

As we can see, we found some images with filenames containing tulip. 
Also notice that we are now at the second level so we can search through the results of the previous search to find a specific tulip.

```terminal
$ search text
Type the query text string you wish to search with
$ c21b68910e_n
Searching image repository based on inputted text query: c21b68910e_n
Found some hits! Now constructing new image repository view with your results...
1 Search result(s): 
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6539831765_c21b68910e_n.jpg
You are now in a view of the repository containing only the above search results.
```

Now, let's zoom back out and return to the first level containing the original repository. We will do this using "return home", however note that using "return" twice would accomplish the same thing.

```terminal
$ return home
At original image repository.
```

Now, for something cool! Let's consider if we wanted to search our image repository purely using a query image instead of query text.
This can be thought of like a google image search, except you pass in a photo as your search query instead of text. 
We'll use a sunflower picture from our dataset:
![alt text](/IrisDataVerySmall/sunflower_16975010069_7afd290657_m.jpg?raw=true) and search it against the dataset, we should expect to get some sunflowers as search hits!

```terminal
$ search images
Type the path to the image you wish to search with
$ /Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/sunflower_16975010069_7afd290657_m.jpg
Searching image repository for similar images based on query image: /Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/sunflower_16975010069_7afd290657_m.jpg
Found some hits! Now constructing new image repository view with your results...
11 Search Result(s): 
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/rose_3450344423_63ba3190e3.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/dandelion_4155914848_3d57f50fc7.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/dandelion_4151883194_e45505934d_n.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6539831765_c21b68910e_n.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/rose_3451177763_729a4d54af_n.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/sunflower_16988605969_570329ff20_n.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/rose_3415176946_248afe9f32.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6808860548_53796b90ca_n.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/daisy_1285423653_18926dc2c8_n.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/sunflower_16975010069_7afd290657_m.jpg
/Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/tulip_6799076717_575944af91_m.jpg
```

![alt text](/IrisDataVerySmall/sunflower_16967372357_15b1b9a812_n.jpg?raw=true)
![alt text](/IrisDataVerySmall/dandelion_4151883194_e45505934d_n.jpg?raw=true)
![alt text](/IrisDataVerySmall/sunflower_16988605969_570329ff20_n.jpg?raw=true)
![alt text](/IrisDataVerySmall/sunflower_16975010069_7afd290657_m.jpg?raw=true)
![alt text](/IrisDataVerySmall/sunflower_17148843706_df148301ac_n.jpg?raw=true)
![alt text](/IrisDataVerySmall/sunflower_17433282043_441b0a07f4_n.jpg?raw=true)
![alt text](/IrisDataVerySmall/dandelion_4226758402_a1b75ce3ac_n.jpg?raw=true)


We can see we got all of the sunflowers in the dataset, as well as some dandelions which appear to share some general shape with the sunflowers.
Note that from here we could now perform another search using another image query, or a text query, to further narrow down results.

Now, we'll demo the **check for corruption** command. 

```terminal
$ check for corruption
Type "search text" to search within current view of the image repository
...
```

As we can see, currently the images are not corrupted (since they have not been modified at all).
To demo a corruption, I'll modify the picture SCARY_tulip_6808860548_53796b90ca_n.jpg by fading it (using my local image editor).
The image used to look like this:
![alt text](/IrisDataVerySmall/tulip_6808860548_53796b90ca_n.jpg?raw=true)

Now, we make it look like this:
![alt text](/IrisDataVerySmall/SCARY_tulip_6808860548_53796b90ca_n.jpg?raw=true)

```terminal
$ check for corruption
Corrupted image! /Users/anantmaheshwari/PycharmProjects/ImageRepo/IrisDataVerySmall/SCARY_tulip_6808860548_53796b90ca_n.jpg
```

## Next Directions
Now with this base implementation, there can be a lot of improvements made/future work!
1) **Paging**: In practice when working with a huge image repository, search results should appear as the first "x" results alongside a feature to "scroll" to the next x results, where x is some fraction of the total number of results (a page of results). For a large image repository we would not want to always show the user all of their search hits as this can be a huge, rather show them enough so they can gain intuition about what their next search should be.
2) **Image Classification**: There are a lot of other algorithms (other than KMeans) that can be explored, and better feature selection methods that can be used. Instead of flattening all of the RGB pixels for the images, it might be better to focus on, for example, the five highest consecutive red pixel values, and the same with green and blue. This would better account for situations where the images are the same, but have very different layouts (flower is in top right of one picture, bottom left of other picture).
Another key point to make this feature scale is that it is costly to flatten out all of the pixels, and so for larger image repositories it might make sense to only look at the top left quadrant of the pixels for each picture (or another technique to sample from the picture features/ dimension reduction of the feature matrix).
3) **Download/Upload Corruption Checking:** Could add a feature to allow users to "check out" and "check in" images, and then could use the implemented hashing logic to ensure users return images in the same state they found them in.
