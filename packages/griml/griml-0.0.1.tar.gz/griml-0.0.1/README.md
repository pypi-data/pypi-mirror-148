# Investigating Greenland's ice marginal lakes under a changing climate (GrIML)

[![Documentation Status](https://readthedocs.org/projects/griml/badge/?version=latest)](https://griml.readthedocs.io/en/latest/?badge=latest)

A repository for all project-related materials, funded under the ESA Living Planet Fellowship.

**Project aim:** To examine ice marginal lake changes across Greenland using a multi-method and multi-sensor remote sensing approach, refined with in situ validation.

## Background

<img src="https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41598-021-83509-1/MediaObjects/41598_2021_83509_Fig1_HTML.png?raw=true" align="right" width="400">

Sea level is predicted to rise drastically by 2100, with significant contribution from the melting of the Greenland Ice Sheet (GrIS). In these predictions, melt runoff is assumed to contribute directly to sea level change, with little consideration for meltwater storage at the terrestrial margin of the ice sheet; such as ice marginal lakes. 

In 2017, 3347 ice marginal lakes were identified in Greenland along the ice margin (<a href="https://www.nature.com/articles/s41598-021-83509-1">How et al., 2021</a>, see map figure for all mapped lakes). Globally, these ice marginal lakes hold up to 0.43 mm of sea level equivalent, which could have a marked impact on future predictions (<a href="https://www.nature.com/articles/s41558-020-0855-4">Shugar et al., 2021</a>). Therefore, they need to be monitored to understand how changes in ice marginal lake water storage affect melt contribution, and how their dynamics evolve under a changing climate.

**GrIML** proposes to examine ice marginal lake changes across Greenland using a multi-sensor and multi-method remote sensing approach to better address their influence on sea level contribution forecasting.

1. Greenland-wide inventories of ice marginal lakes will be generated for selected years during the satellite era, building upon established classification methods in a unified cloud processing workflow

2. Detailed time-series analysis will be conducted on chosen ice marginal lakes to assess changes in their flooding dynamics; focusing on lakes with societal and scientific importance

3. The findings from this work will be validated against in situ observations - namely hydrological measurements and terrestrial time-lapse images - to evaluate whether the remote sensing workflow adequately captures ice marginal lake dynamics


## Methodology

Ice marginal lakes will be detected using a remote sensing approach, based on offline workflows developed within the <a href="https://catalogue.ceda.ac.uk/uuid/7ea7540135f441369716ef867d217519">ESA Glaciers CCI</a> (Option 6, An Inventory of Ice-Marginal Lakes in Greenland) (see workflow below). Lake extents were defined through a multi-sensor approach, using multi-spectral indices classification from Sentinel-2 optical imagery, backscatter classification from Sentinel-1 SAR (synthetic aperture radar) imagery, and sink detection from ArcticDEM digital elevation models (<a href="https://www.nature.com/articles/s41598-021-83509-1">How et al., 2021</a>). 

<img src="https://github.com/PennyHow/pennyhow.github.io/blob/master/assets/images/griml_workflow.png?raw=true" alt="The proposed GrIML workflow." width="1500" align="aligncenter" />

The intent in GrIML is to build upon this pre-existing workflow with new and innovative solutions to form a unified and automated processing chain, with the option to integrate it into a cloud processing platform for efficient big data analysis. 

These developments will alleviate the current challenges associated with data-heavy processing (i.e. multi-sensor integration and data retrieval), and ensure detection accuracy with a merged and collated set of established methodologies. These developments will include:

1. Incorporation of the multi-spectral indices classification, backscatter classification, and sink detection methods into one unified processing chain

2. Integration of image analysis from additional sensors into the processing chain, such as Landsat 4-8

3. Automisation of post-processing filtering to remove detached water bodies and misclassifications, using the already-existing 2017 inventory (How et al., 2021) as a training dataset to automatically match and retain existing lakes 

4. Adaptation of the workflow for easy transference between offline and cloud processing platforms

## Links

- ESA <a href="https://eo4society.esa.int/projects/griml/">project outline</a> and <a href="https://eo4society.esa.int/lpf/penelope-how/">fellow information</a>

- Information about the <a href="https://eo4society.esa.int/communities/scientists/living-planet-fellowship/">ESA Living Planet Fellowship</a>

- <a href="https://pennyhow.github.io/blog/investigating-griml/">GrIML project description</a>

- 2017 ice marginal lake inventory <a href="https://www.nature.com/articles/s41598-021-83509-1">Scientific Reports paper</a> and <a href="https://catalogue.ceda.ac.uk/uuid/7ea7540135f441369716ef867d217519">dataset</a>
