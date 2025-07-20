import ee
import geemap
import geemap.colormaps as cm
import os
from dotenv import load_dotenv
import urllib.request

load_dotenv()
ProjectName = os.getenv("PROJECT_NAME")

def urban_map(lat, lng):
    try:
        ee.Initialize(project=ProjectName)
    except Exception as e:
        ee.Authenticate()
        ee.Initialize(project=ProjectName)

    # --------------------------------------------
    # Define Area of Interest (AOI)
    # --------------------------------------------
    point = ee.Geometry.Point(float(lng), float(lat))
    aoi = point.buffer(5000).bounds()  # 5 km buffer

    # Setup Map
    Map = geemap.Map()
    Map.centerObject(aoi, 12)
    Map.addLayer(aoi, {}, 'AOI')

    # Sentinel-2 Image Collection for NDVI Calculation
    sentinel2 = (
        ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterBounds(aoi)
        .filterDate('2022-01-01', '2022-12-31')
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
        .first()
    )
    ndvi = sentinel2.normalizedDifference(['B8', 'B4']).rename('NDVI').clip(aoi)

    # ESRI LULC Classification
    esri_lulc = (
        ee.ImageCollection("projects/sat-io/open-datasets/landcover/ESRI_Global-LULC_10m_TS")
        .filterDate('2022-01-01', '2022-12-31')
        .mosaic()
        .clip(aoi)
    )

    # Group LULC into classes
    grouped_lulc = esri_lulc.remap(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [4, 1, 2, 2, 2, 2, 2, 3, 3, 4, 4]
    ).rename('Grouped_LC')

    # Building and Road Classification
    buildings_fc = ee.FeatureCollection('GOOGLE/Research/open-buildings/v3/polygons').filterBounds(aoi)
    building_image = ee.Image(0).byte().paint(buildings_fc, 1).rename('Buildings').clip(aoi)

    urban_mask = grouped_lulc.eq(3)
    buildings_class = urban_mask.And(building_image).multiply(5)
    roads_class = urban_mask.And(building_image.Not()).multiply(6)

    # Water and Vacant Classification
    water_class = grouped_lulc.eq(1).multiply(7)
    vacant_class = grouped_lulc.eq(4).multiply(8)

    # Final Classification Image
    final_urban_water_vacant = buildings_class.unmask(0).add(roads_class).add(water_class).add(vacant_class).rename('Urban_Water_Vacant').clip(aoi)

    # Sample and Train
    samples = final_urban_water_vacant.stratifiedSample(
        numPoints=1000,
        classBand='Urban_Water_Vacant',
        region=aoi,
        scale=10,
        seed=42,
        geometries=True
    )

    samples = ndvi.sampleRegions(
        collection=samples,
        properties=['Urban_Water_Vacant'],
        scale=10,
        geometries=True
    )

    samples = samples.randomColumn()
    training = samples.filter(ee.Filter.lt('random', 0.7))
    testing = samples.filter(ee.Filter.gte('random', 0.7))

    classifier = ee.Classifier.smileRandomForest(
        numberOfTrees=150, minLeafPopulation=5, bagFraction=0.7
    ).train(
        features=training,
        classProperty='Urban_Water_Vacant',
        inputProperties=['NDVI']
    )

    # Classify and evaluate
    classified = final_urban_water_vacant.classify(classifier).clip(aoi)

    classified_testing = testing.classify(classifier)
    test_matrix = classified_testing.errorMatrix('Urban_Water_Vacant', 'classification')
    test_accuracy = test_matrix.accuracy().getInfo()
    print("Testing Accuracy:", test_accuracy)

    # Visualization
    urban_palette = ['black', 'purple', 'yellow', 'blue', 'gray']
    visualized = final_urban_water_vacant.remap([0, 6, 5, 7, 8], [0, 1, 2, 3, 4])
    Map.addLayer(visualized, {'min': 0, 'max': 4, 'palette': urban_palette}, 'Urban, Water & Vacant Areas')

    # Export as PNG + HTML
    try:
        thumb_url = visualized.getThumbURL({
            'region': aoi,
            'dimensions': '1024x1024',
            'format': 'png',
            'min': 0,
            'max': 4,
            'palette': urban_palette
        })

        urllib.request.urlretrieve(thumb_url, 'Urban_Water_Vacant.png')
        Map.to_html('Map.html')
        return True

    except Exception as e:
        print("Export Error:", str(e))
        return False
