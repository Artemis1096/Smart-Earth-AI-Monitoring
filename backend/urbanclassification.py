import ee
import geemap
import geemap.colormaps as cm


# Initialize Earth Engine
def urban_map(lat, lng):
    lat = float(lat)
    lng = float(lng)
    
    try:
        ee.Initialize(project='airgreen-javengers')
    except Exception as e:
        ee.Authenticate()
        ee.Initialize(project='airgreen-javengers')

    # --------------------------------------------
    # Define Area of Interest (AOI)
    # --------------------------------------------
    point = ee.Geometry.Point(81.6261,21.2321)
    aoi = point.buffer(5000).bounds()  # 5 km buffer

    # Setup Map
    Map = geemap.Map()
    Map.centerObject(aoi, 12)
    Map.addLayer(aoi, {}, 'AOI')

    # --------------------------------------------
    # Sentinel-2 Image Collection for NDVI Calculation
    # --------------------------------------------
    sentinel2 = (
        ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterBounds(aoi)
        .filterDate('2022-01-01', '2022-12-31')
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
        .first()  # Take the first image from the filtered collection
    )

    # Compute NDVI using Sentinel-2 bands (B8: NIR, B4: Red)
    ndvi = sentinel2.normalizedDifference(['B8', 'B4']).rename('NDVI').clip(aoi)

    # --------------------------------------------
    # Grouped Land Use Land Cover (LULC) for Urban Detection
    # --------------------------------------------
    esri_lulc = (
        ee.ImageCollection("projects/sat-io/open-datasets/landcover/ESRI_Global-LULC_10m_TS")
        .filterDate('2022-01-01', '2022-12-31')
        .mosaic()
        .clip(aoi)
    )

    # Group ESRI LULC to Urban (Class 3) and Water (Class 1)
    grouped_lulc = esri_lulc.remap(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [4, 1, 2, 2, 2, 2, 2, 3, 3, 4, 4]
    ).rename('Grouped_LC').clip(aoi)

    # --------------------------------------------
    # Extract Buildings, Roads, Water, and Vacant Areas
    # --------------------------------------------
    buildings_fc = ee.FeatureCollection('GOOGLE/Research/open-buildings/v3/polygons').filterBounds(aoi)
    building_image = ee.Image(0).byte().paint(buildings_fc, 1).rename('Buildings').clip(aoi)

    urban_mask = grouped_lulc.eq(3)  # Urban areas (Roads and Built-up)
    buildings_class = urban_mask.And(building_image).multiply(5)  # Class 5: Buildings
    roads_class = urban_mask.And(building_image.Not()).multiply(6)  # Class 6: Roads/Other Urban

    # Water and Vacant Areas (Non-Urban, non-vegetated)
    water_mask = grouped_lulc.eq(1)  # Water class
    vacant_mask = grouped_lulc.eq(4)  # Vacant/Bare Land class

    water_class = water_mask.multiply(7)  # Class 7: Water
    vacant_class = vacant_mask.multiply(8)  # Class 8: Vacant Area

    # Combine into final urban and non-urban classification
    final_urban_water_vacant = buildings_class.unmask(0).add(roads_class).add(water_class).add(vacant_class).rename('Urban_Water_Vacant').clip(aoi)

    # --------------------------------------------
    # Random Forest Classification Training
    # --------------------------------------------
    # Sampling LULC for model training
    samples = final_urban_water_vacant.stratifiedSample(
        numPoints=1000,
        classBand='Urban_Water_Vacant',
        region=aoi,
        scale=10,
        seed=42,
        geometries=True
    )

    # Add NDVI to the samples for feature input
    samples = ndvi.sampleRegions(
        collection=samples,
        properties=['Urban_Water_Vacant'],
        scale=10,
        geometries=True
    )

    # Split samples into 70% training and 30% testing
    samples = samples.randomColumn()
    training = samples.filter(ee.Filter.lt('random', 0.7))
    testing = samples.filter(ee.Filter.gte('random', 0.7))

    # Train Random Forest Classifier
    classifier = ee.Classifier.smileRandomForest(
        numberOfTrees=150, minLeafPopulation=5, bagFraction=0.7
    ).train(
        features=training,
        classProperty='Urban_Water_Vacant',
        inputProperties=['NDVI']  # Using NDVI as the input property
    )

    # Classify entire AOI using the trained classifier
    classified_urban_water_vacant = final_urban_water_vacant.classify(classifier).clip(aoi)

    # --------------------------------------------
    # Evaluate Classifier Accuracy
    # --------------------------------------------
    # Training accuracy
    train_matrix = classifier.confusionMatrix()
    train_accuracy = train_matrix.accuracy().getInfo()
    print("Training Accuracy:", train_accuracy)

    # Testing accuracy
    classified_testing = testing.classify(classifier)
    test_matrix = classified_testing.errorMatrix('Urban_Water_Vacant', 'classification')
    test_accuracy = test_matrix.accuracy().getInfo()
    print("Testing Accuracy:", test_accuracy)

    # --------------------------------------------
    # Map Visualization for Urban, Water, and Vacant Areas
    # --------------------------------------------
    urban_palette = ['black', 'purple', 'yellow', 'blue', 'gray']  # Background, Roads, Buildings, Water, Vacant

    # Remap for visualization (0: Background, 6: Roads, 5: Buildings, 7: Water, 8: Vacant)
    visualized_urban_water_vacant = final_urban_water_vacant.remap([0, 6, 5, 7, 8], [0, 1, 2, 3, 4])
    Map.addLayer(visualized_urban_water_vacant,
                {'min': 0, 'max': 4, 'palette': urban_palette},
                'Urban, Water & Vacant Areas')

    # --------------------------------------------
    # Display Map
    # --------------------------------------------
    Map

    # Group ESRI LULC to Urban (Class 3) and Water (Class 1)
    grouped_lulc = esri_lulc.remap(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [4, 1, 2, 2, 2, 2, 2, 3, 3, 4, 4]
    ).rename('Grouped_LC').clip(aoi)

    # --------------------------------------------
    # Extract Buildings, Roads, Water, and Vacant Areas
    # --------------------------------------------
    buildings_fc = ee.FeatureCollection('GOOGLE/Research/open-buildings/v3/polygons').filterBounds(aoi)
    building_image = ee.Image(0).byte().paint(buildings_fc, 1).rename('Buildings').clip(aoi)

    urban_mask = grouped_lulc.eq(3)  # Urban areas (Roads and Built-up)
    buildings_class = urban_mask.And(building_image).multiply(5)  # Class 5: Buildings
    roads_class = urban_mask.And(building_image.Not()).multiply(6)  # Class 6: Roads/Other Urban

    # Water and Vacant Areas (Non-Urban, non-vegetated)
    water_mask = grouped_lulc.eq(1)  # Water class
    vacant_mask = grouped_lulc.eq(4)  # Vacant/Bare Land class

    water_class = water_mask.multiply(7)  # Class 7: Water
    vacant_class = vacant_mask.multiply(8)  # Class 8: Vacant Area

    # Combine into final urban and non-urban classification
    final_urban_water_vacant = buildings_class.unmask(0).add(roads_class).add(water_class).add(vacant_class).rename('Urban_Water_Vacant').clip(aoi)

    # --------------------------------------------
    # Random Forest Classification Training
    # --------------------------------------------
    # Sampling LULC for model training
    samples = final_urban_water_vacant.stratifiedSample(
        numPoints=1000,
        classBand='Urban_Water_Vacant',
        region=aoi,
        scale=10,
        seed=42,
        geometries=True
    )

    # Add NDVI to the samples for feature input
    samples = ndvi.sampleRegions(
        collection=samples,
        properties=['Urban_Water_Vacant'],
        scale=10,
        geometries=True
    )

    # Split samples into 70% training and 30% testing
    samples = samples.randomColumn()
    training = samples.filter(ee.Filter.lt('random', 0.7))
    testing = samples.filter(ee.Filter.gte('random', 0.7))

    # Train Random Forest Classifier
    classifier = ee.Classifier.smileRandomForest(
        numberOfTrees=150, minLeafPopulation=5, bagFraction=0.7
    ).train(
        features=training,
        classProperty='Urban_Water_Vacant',
        inputProperties=['NDVI']  # Using NDVI as the input property
    )

    # Classify entire AOI using the trained classifier
    classified_urban_water_vacant = final_urban_water_vacant.classify(classifier).clip(aoi)

    # --------------------------------------------
    # Evaluate Classifier Accuracy
    # --------------------------------------------
    # Training accuracy
    train_matrix = classifier.confusionMatrix()
    train_accuracy = train_matrix.accuracy().getInfo()
    print("Training Accuracy:", train_accuracy)

    # Testing accuracy
    classified_testing = testing.classify(classifier)
    test_matrix = classified_testing.errorMatrix('Urban_Water_Vacant', 'classification')
    test_accuracy = test_matrix.accuracy().getInfo()
    print("Testing Accuracy:", test_accuracy)

    # --------------------------------------------
    # Map Visualization for Urban, Water, and Vacant Areas
    # --------------------------------------------
    urban_palette = ['black', 'purple', 'yellow', 'blue', 'gray']  # Background, Roads, Buildings, Water, Vacant

    # Remap for visualization (0: Background, 6: Roads, 5: Buildings, 7: Water, 8: Vacant)
    visualized_urban_water_vacant = final_urban_water_vacant.remap([0, 6, 5, 7, 8], [0, 1, 2, 3, 4])
    Map.addLayer(visualized_urban_water_vacant,
                {'min': 0, 'max': 4, 'palette': urban_palette},
                'Urban, Water & Vacant Areas')

    # --------------------------------------------
    # Display Map
    # --------------------------------------------
    try:
        print("Saving Map as HTML")
        Map.to_html('Map.html')
        print("Map saved successfully.")
        return True
    
    except Exception as e:
        print("Error while saving map: ", str(e))
        return False