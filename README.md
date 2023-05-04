# Image Randomizer

Image Randomizer is a simple Python application that takes an input image, resizes it to fit an A4 size, splits it into 24 (3x9) rectangles, randomizes the order of the rectangles, and reassembles them into a new A4 image. The application also generates a version of the image without shuffling the rectangles. Each rectangle is labeled with a number indicating its initial position in the original image.

The application consists of a command-line script (`image_randomizer.py`) and a Flask web server (`app.py`) with an HTML interface (`index.html`).

## Requirements

- Python 3.6 or higher
- Pillow
- Flask

## Installation

1. Clone this repository:
```bash
git clone https://github.com/gfarcas/image-randomizer.git
cd image-randomizer
```

2. Create a virtual environment and install the required packages:
```bash
python -m venv venv
source venv/bin/activate # For Linux/macOS
.\venv\Scripts\activate # For Windows
pip install -r requirements.txt
```

## Usage

### Command-line

Run the `image_randomizer.py` script as follows:
```bash
python image_randomizer.py input_image.jpg shuffled_output_image.jpg unshuffled_output_image.jpg
```

This will create a shuffled and an unshuffled version of the input image and save them as `shuffled_output_image.jpg` and `unshuffled_output_image.jpg`, respectively.

### Web Interface

1. Start the Flask server:
`python app.py`

2. Open your browser and visit `http://127.0.0.1:5000/`.

3. Choose an image file and click "Submit" to generate the shuffled and unshuffled output images. The images will be displayed on the result page.


