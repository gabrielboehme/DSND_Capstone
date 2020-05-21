# Data Science NanoDegree Capstone Project

![Intro Pic](images/main_page.png)

## Table of Contents
1. [Project Motivation](#Motivation)
2. [Getting Started](#getting_started)
	1. [Dependencies](#dependencies)
	2. [Installing](#installing)
	3. [Executing Program](#executing)
3. [Authors & Licensing](#authors)
4. [Acknowledgement](#acknowledgement)
5. [Screenshots](#screenshots)

<a name="Motivation"></a>
## Problem Statement

This project has the motivation of helping the City of Detroit solving one of the most pressing problems facing Detroit - blight.
Blight violations are issued by the city to individuals who allow their properties to remain in a deteriorated condition. 
Every year, the city of Detroit issues millions of dollars in fines to residents and every year, many of these fines remain unpaid. 
Enforcing unpaid blight fines is a costly and tedious process, so the city wants to know: how can we increase blight ticket compliance?
The first step in answering this question is understanding when and why a resident might fail to comply with a blight ticket. 
This is where predictive modeling comes in.

As the deliverable for this project, it will be an API, as Chicago can integrate their systems with this API and fight against
blight violations

## Metrics
The evaluation metric for this project is the Area Under the ROC Curve (AUC).
The result with this model was 0.789571648559 

<a name="getting_started"></a>
## Getting Started

<a name="dependencies"></a>
### Dependencies
* Python 3.5+ (I used Python 3.6.2)
* Machine Learning Libraries: NumPy, SciPy, Pandas, Sciki-Learn
* System Librarie: sys
* Binary files: pickle
* Web App: Flask

<a name="installing"></a>
### Installing
Clone this GIT repository:
```
git clone https://github.com/gabrielboehme/DSND_Capstone.git
```
<a name="executing"></a>
### Executing Program:
1. Run the following commands in the project's root directory to set up your machine learning model.
  
  `python train_model.py`

2. Run the following command in the app's directory to run your web app.

  `python app.py`

3. Go to http://0.0.0.0:5000/

Note: Fitting the model may take some hours.

<a name="Author"></a>
## Authors

* [Gabriel Boehme](https://github.com/gabrielboehme/)

<a name="acknowledgement "></a>
## Acknowledgements

* [Udacity](https://www.udacity.com/) for providing such a complete Data Science Nanodegree Program
* [Detroit Open Data Portal](https://data.detroitmi.gov/) for providing the dataset to train the model.

<a name="screenshots"></a>
## Screenshots

1. This is an example of a message you can type to test Machine Learning model performance and see
what categories he classified that message

![Sample Input](images/sample_output.png)



2. The main page shows some graphs about training dataset:

Distribution of Message Genres:
![Main Page](images/genres.png)


Correlation heatmap between categories:
![Main Page](images/corr.png)


Distribution of text lenght:
![Main Page](images/txt_lenght.png)
