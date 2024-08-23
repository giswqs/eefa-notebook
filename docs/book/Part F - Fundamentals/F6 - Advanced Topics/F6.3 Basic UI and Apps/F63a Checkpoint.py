import ee
import geemap

Map = geemap.Map()

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Chapter:      F6.3 Sharing Work in Earth Engine: Basic UI and Apps
#  Checkpoint:   F63a
#  Author:       Qiusheng Wu
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Get an NLCD image by year.
def getNLCD(year):
    # Import the NLCD collection.
    dataset = ee.ImageCollection(
        'USGS/NLCD_RELEASES/2019_REL/NLCD')

    # Filter the collection by year.
    nlcd = dataset.filter(ee.Filter.eq('system:index', year)) \
        .first()

    # Select the land cover band.
    landcover = nlcd.select('landcover')
    return ui.Map.Layer(landcover, {}, year)


# Create a dictionary with each year as the key
# and its corresponding NLCD image layer as the value.
images = {
    '2001': getNLCD('2001'),
    '2004': getNLCD('2004'),
    '2006': getNLCD('2006'),
    '2008': getNLCD('2008'),
    '2011': getNLCD('2011'),
    '2013': getNLCD('2013'),
    '2016': getNLCD('2016'),
    '2019': getNLCD('2019'),
}

#
# Set up the maps and control widgets
#

# Create the left map, and have it display the first layer.
leftMap = ui.Map()
leftMap.setControlVisibility(False)
leftSelector = addLayerSelector(leftMap, 0, 'top-left')

# Create the right map, and have it display the last layer.
rightMap = ui.Map()
rightMap.setControlVisibility(True)
rightSelector = addLayerSelector(rightMap, 7, 'top-right')

# Adds a layer selection widget to the given map, to allow users to
# change which image is displayed in the associated map.
def addLayerSelector(mapToChange, defaultValue, position):
    label = ui.Label('Select a year:')

    # This function changes the given map to show the selected image.
    def updateMap(selection):
        mapToChange.layers().set(0, images[selection])


    # Configure a selection dropdown to allow the user to choose
    # between images, and set the map to update when a user
    # makes a selection.
    select = ui.Select({
        'items': Object.keys(images),
        'onChange': updateMap
    })
    select.setValue(Object.keys(images)[defaultValue], True)

    controlPanel =
        ui.Panel({
            'widgets': [label, select],
            'style': {
                'position': position
            }
        })

    mapToChange.add(controlPanel)


# Set the legend title.
title = 'NLCD Land Cover Classification'

# Set the legend position.
position = 'bottom-right'

# Define a dictionary that will be used to make a legend
# Reference: https:#code.earthengine.google.com/74ffc1eb0caabbbfaea535537829dda5
dict = {
    'names': [
        '11	Open Water',
        '12	Perennial Ice/Snow',
        '21	Developed, Open Space',
        '22	Developed, Low Intensity',
        '23	Developed, Medium Intensity',
        '24	Developed, High Intensity',
        '31	Barren Land (Rock/Sand/Clay)',
        '41	Deciduous Forest',
        '42	Evergreen Forest',
        '43	Mixed Forest',
        '51	Dwarf Scrub',
        '52	Shrub/Scrub',
        '71	Grassland/Herbaceous',
        '72	Sedge/Herbaceous',
        '73	Lichens',
        '74	Moss',
        '81	Pasture/Hay',
        '82	Cultivated Crops',
        '90	Woody Wetlands',
        '95	Emergent Herbaceous Wetlands',
    ],

    'colors': [
        '#466b9f', '#d1def8', '#dec5c5', '#d99282', '#eb0000',
        '#ab0000',
        '#b3ac9f', '#68ab5f', '#1c5f2c', '#b5c58f', '#af963c',
        '#ccb879',
        '#dfdfc2', '#d1d182', '#a3cc51', '#82ba9e', '#dcd939',
        '#ab6c28',
        '#b8d9eb', '#6c9fb8',
    ]
}

# Create a panel to hold the legend widget.
legend = ui.Panel({
    'style': {
        'position': position,
        'padding': '8px 15px'
    }
})

# Function to generate the legend.
def addCategoricalLegend(panel, dict, title):

    # Create and add the legend title.
    legendTitle = ui.Label({
        'value': title,
        'style': {
            'fontWeight': 'bold',
            'fontSize': '18px',
            'margin': '0 0 4px 0',
            'padding': '0'
        }
    })
    panel.add(legendTitle)

    loading = ui.Label('Loading legend...', {
        'margin': '2px 0 4px 0'
    })
    panel.add(loading)

    # Creates and styles 1 row of the legend.
    def makeRow(color, name):
        # Create the label that is actually the colored box.
        colorBox = ui.Label({
            'style': {
                'backgroundColor': color,
                # Use padding to give the box height and width.
                'padding': '8px',
                'margin': '0 0 4px 0'
            }
        })

        # Create the label filled with the description text.
        description = ui.Label({
            'value': name,
            'style': {
                'margin': '0 0 4px 6px'
            }
        })

        return ui.Panel({
            'widgets': [colorBox, description],
            'layout': ui.Panel.Layout.Flow('horizontal')
        })


    # Get the list of palette colors and class names from the image.
    palette = dict.colors
    names = dict.names
    loading.style(**).set('shown', False)

    for i in range(0, names.length, 1):
        panel.add(makeRow(palette[i], names[i]))


    rightMap.add(panel)



addCategoricalLegend(legend, dict, title)

#
# Tie everything together
#

# Create a SplitPanel to hold the adjacent, linked maps.
splitPanel = ui.SplitPanel({
    'firstPanel': leftMap,
    'secondPanel': rightMap,
    'wipe': True,
    'style': {
        'stretch': 'both'
    }
})

# Set the SplitPanel as the only thing in the UI root.
ui.root.widgets().reset([splitPanel])
linker = ui.Map.Linker([leftMap, rightMap])
leftMap.setCenter(-100, 40, 4)

#  -----------------------------------------------------------------------
#  CHECKPOINT
#  -----------------------------------------------------------------------


Map
