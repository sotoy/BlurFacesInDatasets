# Blur Faces in Datasets
An easy to install and use tool based on [deepface](https://github.com/serengil/deepface) and [retinaface](https://github.com/serengil/retinaface) to anonymize people in your dataset images.
<kbd>
![Example of applying the blurring pipeline in a collection of Times Person of the Year magazines.](/example_imgs/BlurFaces.png)
</kbd>
## Installation:
Ensure that docker is installed in your system. If not, follow the [official webpage](https://docs.docker.com/engine/install/)

## Data Preparation
The code operates on all files contained in a directory, **including those in subfolders**. Therefore, the existing folder structure does not have to be altered.
>[!CAUTION]
>The blurring pipeline modifies images **inplace**. Please make sure to not apply blurring on the original data. Instead operate on a copy of the dataset for security reasons.

## Usage
### Step 1: Build the Docker Image:
Navigate to the repo folder and build the docker:
```
cd BlurFacesInDatasets
docker build -t face-blur ./src
```
### Step 2: Run the Docker Container
Ensure you have a directory with images you want to process. Then, run the container, mounting the directory into the container.
```
docker run -v /path/to/your/dataset/root:/app/images face-blur /app/images
```
This command mounts your local images directory to the /app/images directory inside the Docker container, allowing the script to access and process them.

## Note
Please bear in mind that in the current version the CNN runs on cpu. For gpu deployment, please make the necessary adjustments in the dockerfile, as well as in the requirements.txt file. Otherwise, please wait for a release with proper gpu intergration.
