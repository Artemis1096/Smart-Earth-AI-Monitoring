import ee
import geemap
import geemap.colormaps as cm

# Initialize Earth Engine
def generate_map(lat, lng):
    lat = float(lat)
    lng = float(lng)
        
    try:
        print("Attempting Earth Engine Initialization")
        ee.Initialize(project='ee-jashanpreetsingh1096')
        print("Initialization Success!")
    except Exception as e:
        print("Initialization Failed: ", str(e))
        try:
            print("Attempting Authentication")
            ee.Authenticate()
            ee.Initialize(project='ee-jashanpreetsingh1096')
            print("Initialization after Authentication Success!")
        except Exception as auth_error:
            print("Authentication Failed: ", str(auth_error))
            return

    print("Defining Area of Interest (AOI)")
    try:
        point = ee.Geometry.Point(lng, lat)
        aoi = point.buffer(5000).bounds()
        print("AOI created.")
    except Exception as e:
        print("Error creating AOI:", str(e))
        return

    print("Setting up map")
    try:
        Map = geemap.Map()
        Map.centerObject(aoi, 12)
        Map.addLayer(aoi, {}, 'AOI')
        print("Map setup successful.")
    except Exception as e:
        print("Map setup error:", str(e))
        return

    # Sentinel-2 collection with band selection fix
    try:
        print("Filtering Sentinel-2 Collection")
        selected_bands = ['B4', 'B8']  # Red and NIR for NDVI
        sentinel2_collection = (
            ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
            .filterBounds(aoi)
            .filterDate('2014-01-01', '2024-01-01')
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
            .map(lambda img: img.select(selected_bands))  # Consistent bands
        )
        print("Collection filtered.")
    except Exception as e:
        print("Error filtering collection:", str(e))
        return

    try:
        print("Calculating NDVI")
        median_image = sentinel2_collection.median().clip(aoi)
        ndvi = median_image.normalizedDifference(['B8', 'B4']).rename('NDVI').clip(aoi)
        print("NDVI calculated.")
    except Exception as e:
        print("NDVI error:", str(e))
        return

    try:
        print("Classifying vegetation severity")
        classified_ndvi = ndvi.expression(
            "b('NDVI') < 0.2 ? 1 : (b('NDVI') < 0.4 ? 2 : (b('NDVI') < 0.7 ? 3 : 4))"
        ).rename('Vegetation_Severity').clip(aoi)
        masked_ndvi = classified_ndvi.updateMask(classified_ndvi.gt(0))
        print("Vegetation classified.")
    except Exception as e:
        print("Vegetation classification error:", str(e))
        return

    try:
        print("Highlighting low vegetation")
        red_area = ndvi.lt(0.2).rename('Low_Veg_Red').clip(aoi)
        print("Low vegetation highlighted.")
    except Exception as e:
        print("Low vegetation error:", str(e))
        return

    try:
        print("Filtering ESRI LULC")
        esri_lulc = (
            ee.ImageCollection("projects/sat-io/open-datasets/landcover/ESRI_Global-LULC_10m_TS")
            .filterDate('2022-01-01', '2022-12-31')
            .mosaic()
            .clip(aoi)
        )
        grouped_lulc = esri_lulc.remap(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [4, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4]
        ).rename('Grouped_LC').clip(aoi)
        masked_lulc = grouped_lulc.updateMask(grouped_lulc.gt(0))
        print("ESRI LULC grouped.")
    except Exception as e:
        print("LULC error:", str(e))
        return

    try:
        print("Combining NDVI and LULC")
        final_classification = masked_lulc.addBands(red_area).clip(aoi)
        print("Combination complete.")
    except Exception as e:
        print("Combination error:", str(e))
        return

    try:
        print("Adding layers to map")
        urban_palette = ['blue', 'orange', 'red', 'gray']
        Map.addLayer(final_classification.select('Grouped_LC'),
                     {'min': 1, 'max': 4, 'palette': urban_palette},
                     'Grouped LULC')

        Map.addLayer(final_classification.select('Low_Veg_Red'),
                     {'min': 0, 'max': 1, 'palette': ['red']},
                     'Low Vegetation Red')

        vegetation_palette = ['gray', 'yellow', 'lightgreen', 'darkgreen']
        Map.addLayer(masked_ndvi,
                     {'min': 1, 'max': 4, 'palette': vegetation_palette},
                     'Vegetation Severity')

        ndvi_palette = ['gray', 'yellow', 'lightgreen', 'green', 'darkgreen']
        Map.addLayer(ndvi,
                     {'min': 0, 'max': 1, 'palette': ndvi_palette},
                     'Vegetation Density (NDVI)')
        print("Map layers added.")
    except Exception as e:
        print("Map visualization error:", str(e))
        return

    # Random Forest Classification
    try:
        print("Training Random Forest Classifier")
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

        samples = samples.randomColumn('random', seed=42)
        training = samples.filter(ee.Filter.lt('random', 0.7))
        testing = samples.filter(ee.Filter.gte('random', 0.7))

        classifier = ee.Classifier.smileRandomForest(
            numberOfTrees=150, minLeafPopulation=5, bagFraction=0.7
        ).train(
            features=training,
            classProperty='Grouped_LC',
            inputProperties=['NDVI']
        )

        classified_lulc = ndvi.classify(classifier).clip(aoi)

        Map.addLayer(classified_lulc,
                     {'min': 1, 'max': 4, 'palette': urban_palette},
                     'Classified LULC')
        print("Random Forest classification complete.")
    except Exception as e:
        print("Random Forest error:", str(e))
        return

    try:
        print("Evaluating classifier")
        train_matrix = classifier.confusionMatrix()
        print("Train Confusion Matrix:", train_matrix.getInfo())
        print("Train Accuracy:", train_matrix.accuracy().getInfo())

        classified_testing = testing.classify(classifier)
        test_matrix = classified_testing.errorMatrix('Grouped_LC', 'classification')
        print("Test Confusion Matrix:", test_matrix.getInfo())
        print("Test Accuracy:", test_matrix.accuracy().getInfo())
    except Exception as e:
        print("Evaluation error:", str(e))

    # Vegetation Class Layer
    try:
        print("Creating vegetation class layer")
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
        print("Vegetation class added.")
    except Exception as e:
        print("Vegetation class error:", str(e))

    try:
        print("Saving map")
        Map.to_html('Map.html')
        print("Map saved to Map.html")
        return True
    except Exception as e:
        print("Saving map error:", str(e))
        return False
