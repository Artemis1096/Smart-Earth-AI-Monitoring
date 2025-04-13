import ee
import geemap
import geemap.colormaps as cm
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize Earth Engine
ProjectName = os.getenv("PROJECT_NAME")

def generate_map(lat, lng):
    lat = float(lat)
    lng = float(lng)
         
    try:
        print("Attempting Earth Engine Initialization")
        ee.Initialize(project=ProjectName)
        print("Initialization Success!")
    except Exception as e:
        print("Initialization Failed: ", str(e))
        try:
            print("Attempting Authentication")
            ee.Authenticate()
            ee.Initialize(project=ProjectName)
            print("Initialization after Authentication Success!")
        except Exception as auth_error:
            print("Authentication Failed: ", str(auth_error))
            return  # Stop execution if both init and auth fail

    # --------------------------------------------
    # Define Area of Interest (AOI) around Amazon Rainforest
    # --------------------------------------------
    print("Defining Area of Interest (AOI)")
    try:
        point = ee.Geometry.Point(float(lng), float(lat))  # Coordinates for the point
        aoi = point.buffer(5000).bounds()  # 5 km buffer
        print("Area of Interest (AOI) successfully created.")
    except Exception as e:
        print("Error while creating AOI: ", str(e))

    print("Setting up map")
    try:
        # Setup Map
        Map = geemap.Map()
        Map.centerObject(aoi, 12)
        Map.addLayer(aoi, {}, 'AOI')
        print("Map setup successful.")
    except Exception as e:
        print("Error while setting up map: ", str(e))

    # --------------------------------------------
    # Sentinel-2 Collection Filtering
    # --------------------------------------------
    try:
        print("Filtering Sentinel-2 Collection")
        sentinel2_collection = (
            ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
            .filterBounds(aoi)
            .filterDate('2014-01-01', '2024-01-01')
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
        )
        print("Sentinel-2 Collection Filtered.")
    except Exception as e:
        print("Error while filtering Sentinel-2 collection: ", str(e))

    # Median Composite and NDVI Calculation
    try:
        print("Calculating NDVI")
        median_image = sentinel2_collection.median().clip(aoi)
        ndvi = median_image.normalizedDifference(['B8', 'B4']).rename('NDVI').clip(aoi)
        print("NDVI Calculation Successful.")
    except Exception as e:
        print("Error while calculating NDVI: ", str(e))

    # --------------------------------------------
    # Vegetation Classification Based on NDVI Severity
    # --------------------------------------------
    try:
        print("Classifying Vegetation Severity")
        classified_ndvi = ndvi.expression(
            "b('NDVI') < 0.2 ? 1 : (b('NDVI') < 0.4 ? 2 : (b('NDVI') < 0.7 ? 3 : 4))"
        ).rename('Vegetation_Severity').clip(aoi)
        masked_ndvi = classified_ndvi.updateMask(classified_ndvi.gt(0))
        print("Vegetation Severity Classification Successful.")
    except Exception as e:
        print("Error while classifying vegetation severity: ", str(e))

    # --------------------------------------------
    # Highlight Low Vegetation (NDVI < 0.2) Areas
    # --------------------------------------------
    try:
        print("Highlighting Low Vegetation Areas")
        low_vegetation_mask = ndvi.lt(0.2)
        red_area = low_vegetation_mask.rename('Low_Veg_Red').clip(aoi)
        print("Low Vegetation Areas Highlighted.")
    except Exception as e:
        print("Error while highlighting low vegetation areas: ", str(e))

    # --------------------------------------------
    # Grouped Land Use Land Cover (LULC) Classification
    # --------------------------------------------
    try:
        print("Filtering ESRI LULC Collection")
        esri_lulc = (
            ee.ImageCollection("projects/sat-io/open-datasets/landcover/ESRI_Global-LULC_10m_TS")
            .filterDate('2022-01-01', '2022-12-31')
            .mosaic()
            .clip(aoi)
        )
        grouped_lulc = esri_lulc.remap(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Original classes
            [4, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4]    # Grouped: Water-1, Vegetation-2, Urban-3, Other-4
        ).rename('Grouped_LC').clip(aoi)
        masked_lulc = grouped_lulc.updateMask(grouped_lulc.gt(0))
        print("ESRI LULC Collection Filtered and Grouped.")
    except Exception as e:
        print("Error while processing LULC collection: ", str(e))

    # --------------------------------------------
    # Combine Grouped LULC & Low Vegetation Areas
    # --------------------------------------------
    try:
        print("Combining Grouped LULC and Low Vegetation Areas")
        final_classification = masked_lulc.addBands(red_area).clip(aoi)
        print("Final Classification Combined.")
    except Exception as e:
        print("Error while combining LULC and Low Vegetation Areas: ", str(e))

    # --------------------------------------------
    # Map Layer Visualizations
    # --------------------------------------------
    try:
        # Grouped LULC Layer
        urban_palette = ['blue', 'orange', 'red', 'gray']  # Vegetation, Medium, Urban, Other
        Map.addLayer(final_classification.select('Grouped_LC'), 
                    {'min': 1, 'max': 4, 'palette': urban_palette}, 
                    'Grouped LULC')

        # Low Vegetation Highlight Layer
        Map.addLayer(final_classification.select('Low_Veg_Red'), 
                    {'min': 0, 'max': 1, 'palette': ['red']}, 
                    'Low Vegetation Red')

        # Vegetation Severity Layer
        vegetation_palette = ['gray', 'yellow', 'lightgreen', 'darkgreen']
        Map.addLayer(masked_ndvi, 
                    {'min': 1, 'max': 4, 'palette': vegetation_palette}, 
                    'Vegetation Severity')

        # NDVI Continuous Density Layer
        ndvi_density_palette = ['gray', 'yellow', 'lightgreen', 'green', 'darkgreen']
        Map.addLayer(ndvi.clip(aoi), 
                    {'min': 0, 'max': 1, 'palette': ndvi_density_palette}, 
                    'Vegetation Density (NDVI)')
        print("Map Layers Visualized.")
    except Exception as e:
        print("Error while visualizing map layers: ", str(e))

    # --------------------------------------------
    # Random Forest Classification Training
    # --------------------------------------------
    try:
        print("Training Random Forest Classifier")
        # Sampling NDVI and Grouped_LC for model training
        samples = final_classification.stratifiedSample(
            numPoints=1000,
            classBand='Grouped_LC',
            region=aoi,
            scale=10,
            seed=42,
            geometries=True
        )
        samples = ndvi.sampleRegions(
            collection=samples,
            properties=['Grouped_LC'],
            scale=10,
            geometries=True
        )

        # Split samples into 70% training and 30% testing
        samples = samples.randomColumn(columnName='random', seed=42)

        # print("Generated samples, checking size...")
        # size = samples.size()
        # print("Size (object):", size)  # This is the line likely failing
        training = samples.filter(ee.Filter.lt('random', 0.7))
        # testing = samples.filter(ee.Filter.gte('random', 0.7))
        # print("Training samples:", training.size().getInfo())
        # print("Testing samples:", testing.size().getInfo())

        # Train Random Forest Classifier
        classifier = ee.Classifier.smileRandomForest(
            numberOfTrees=150, minLeafPopulation=5, bagFraction=0.7
        ).train(
            features=training,
            classProperty='Grouped_LC',
            inputProperties=['NDVI']
        )

        # Classify entire AOI using the trained classifier
        classified_lulc = ndvi.classify(classifier).clip(aoi)

        # Classified LULC Result Layer
        Map.addLayer(classified_lulc, 
                    {'min': 1, 'max': 4, 'palette': urban_palette}, 
                    'Classified LULC')
        print("Random Forest Classifier Trained and Applied.")
    except Exception as e:
        print("Error during Random Forest Classification: ", str(e))

    # --------------------------------------------
    # Evaluate Classifier Accuracy
    # --------------------------------------------
    try:
        print("Evaluating Classifier Accuracy")
        # Training Accuracy
        train_matrix = classifier.confusionMatrix()
        print("Train Confusion Matrix:", train_matrix.getInfo())
        print("Train Accuracy:", train_matrix.accuracy().getInfo())

        # Testing Accuracy
        classified_testing = testing.classify(classifier)
        test_matrix = classified_testing.errorMatrix('Grouped_LC', 'classification')
        print("Test Confusion Matrix:", test_matrix.getInfo())
        print("Test Accuracy:", test_matrix.accuracy().getInfo())
    except Exception as e:
        print("Error during classifier evaluation: ", str(e))

    # --------------------------------------------
    # NEW: Vegetation Density Class Layer (Pure Green Class)
    # --------------------------------------------
    try:
        print("Creating Vegetation Density Class Layer")
        vegetation_class = ndvi.expression(
            "(b('NDVI') <= 0.2) ? 1 : "
            "(b('NDVI') <= 0.4) ? 2 : "
            "(b('NDVI') <= 0.6) ? 3 : "
            "(b('NDVI') <= 0.8) ? 4 : 5"
        ).rename('Vegetation_Class').clip(aoi)

        masked_vegetation_class = vegetation_class.updateMask(vegetation_class.gt(0))

        green_palette = ['gray', 'lightyellow', 'lightgreen', 'green', 'darkgreen']

        Map.addLayer(masked_vegetation_class,
                    {'min': 1, 'max': 5, 'palette': green_palette},
                    'Vegetation Density Class')
        print("Vegetation Density Class Layer Created.")
    except Exception as e:
        print("Error while creating vegetation density class layer: ", str(e))

    # --------------------------------------------
    # Display Map and Save as HTML
    # --------------------------------------------
    try:
        print("Saving Map as HTML")
        Map.to_html('Map2.html')
        print("Map saved successfully.")
        return True
    
    except Exception as e:
        print("Error while saving map: ", str(e))
        return False