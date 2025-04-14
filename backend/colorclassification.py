import cv2
import numpy as np
from sklearn.cluster import KMeans
import os
import json
from flask import Flask
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)  # Only if this is part of a Flask app

def kmeans_color_segmentation(image_path, k=4):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w, _ = image.shape
    pixels = image.reshape((-1, 3))
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(pixels)
    centers = np.uint8(kmeans.cluster_centers_)
    segmented_pixels = centers[labels]
    segmented_image = segmented_pixels.reshape((h, w, 3))
    return image, segmented_image, labels.reshape((h, w)), centers

def get_color_name(rgb):
    r, g, b = rgb
    if r > 200 and g > 200 and b > 200:
        return "White / Light Gray"
    elif r < 50 and g < 50 and b < 50:
        return "Black"
    elif b > r and b > g:
        return "Blue"
    elif g > r and g > b:
        return "Green"
    elif r > g and r > b:
        return "Red / Brown"
    elif r > 150 and g > 150 and b < 100:
        return "Yellow"
    elif r > 150 and b > 150 and g < 100:
        return "Magenta / Pink"
    elif abs(r - g) < 20 and b < 100:
        return "Gray / Road-like"
    else:
        return "Purple"

def calculate_percentages_better(image_path, k=4):
    _, _, label_map, cluster_colors = kmeans_color_segmentation(image_path, k)
    unique_labels, counts = np.unique(label_map, return_counts=True)
    total_pixels = label_map.size

    percentages = {}
    for label, count in zip(unique_labels, counts):
        percent = round((count / total_pixels) * 100, 2)
        color = cluster_colors[label]
        color_name = get_color_name(color)
        percentages[color_name] = percent
    return percentages

def get_color_class():
    image_path = os.getenv("IMAGE_PATH")
    print(image_path)
    if not image_path:
        return app.response_class(
            response=json.dumps({"error": "IMAGE_PATH not set"}),
            status=400,
            mimetype='application/json'
        )
    percentages = calculate_percentages_better(image_path)
    
    # Custom label mapping
    label_map = {
        "Black": "Vacant",
        "Purple": "Roads",
        "Blue": "Water",
        "Yellow": "Buildings"
    }
    
    result_dict = {}
    for category, percent in percentages.items():
        label = label_map.get(category.capitalize(), category.capitalize())
        result_dict[label] = f"{percent}%"
    print(result_dict)
    
    json_response = json.dumps(result_dict)
    return app.response_class(
        response=json_response,
        status=200,
        mimetype='application/json'
    )
    