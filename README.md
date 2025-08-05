# bento_diatom

This is a test exposing a trained dead or alive diatom image classifier through an API. It uses [BentoML](https://github.com/bentoml/BentoML) for this purpose.

## How to use

### Option 1 - Run locally

1. Clone the repo
1. Create virtual env
    ```
    python -m venv venv
    ```
1. Optional - activate virtual env if it's not active
    ```
    source venv/bin/activate
    ```
1. Install requirements. This project was developed using Python 3.12.3.
    ```
    pip install requirements.txt
    ```
    The virtual env is quite big (5.5Gb on the dev machine), so be warned.
1. If all goes well, execute the data setup script. 
    ```
    python create_doa_dataset
    ```
    This script downloads the model weights and the original diatom image dataset, then unzips both files and creates an output directory called "data" at the project root. This directory contains two folders ('test','train') and inside each folder there are two subfolders ('alive','dead'). Each of this folders contains the sets for dead and alive diatoms. By default, in the test set we put 10 images, this can be changed by changing the value of the script constant ```N_TEST```.
1. After executing the setup script, on the root folder should exist two crucial files: a file called ```doa_diatom_model.pth``` which contains the weights for a trained ResNet network, and the directory data with the labeled images. We need to start the server, this can be done with the command:
    ```
    bentoml serve
    ```
    Which starts a server which by default runs at [http://127.0.0.1:3000](http://127.0.0.1:3000). This address exposes a [swagger](https://github.com/swagger-api/swagger-ui) interface with the API endpoints.
1. Once running, we can play with the [classify endpoint](http://127.0.0.1:3000/#/Service%20APIs/MyResNet__classify). This endpoint receives an image (we can use any image in the data directory) and returns a simple "dead" or "alive" string with the precision.
1. To get an overall feel of the ResNet network performance, we can run the script test.py
    ```
    python test.py
    ```
    This scripts calls the "classify" endpoint for all of the images in the data folder and outputs the accuracy.

### Option 2 - Use docker

1. Build the docker image, with the command:
    ```
    docker build -t bento-diatom .
    ```
1. Run the created image with
    ```
    docker run -it --rm -p3000:3000 --name bento-diatom-docker bento-diatom
    ```
The service is accessible locally on [http://127.0.0.1:3000](http://127.0.0.1:3000)
