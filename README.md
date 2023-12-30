# Weather Forecast Project with Web Scraped Data

This project aims to create a weather forecast application using web scraped data and a recursive Lasso model. The main objective is to develop deployment skills while providing a practical foundation for similar tasks.

## 🔧 Technologies Used

- DVC for version control of datasets and machine learning models.
- Python for backend logic and ML model training.

## 🚀 Quick Start
Step 1: Clone the repository:

```bash
git clone https://github.com/olaaumari/web-scraping-short-forecasting-temperature.git
```
## Step 2: Set up a Python environment:
Using conda, create and activate an environment:


```bash
conda create -n weather-forecast python=3.8 -y
```
```bash
conda activate weather-forecast
```

## Step 3: Install dependencies:
```bash
pip install -r requirements.txt
```

## Step 4: Run the DVC pipeline:
```bash
dvc repro
```


# DVC Commands:
Execute these commands if you're making changes or want to track data:
```bash
    dvc init
    dvc repro
    dvc dag
```

# 📚 Further Reading
Data Version Control [DVC Documentation](https://dvc.org/doc)


# 🤝 Contribution & Feedback
Feedback, issues, and pull requests are always welcome. For major changes, please open an issue first to discuss what you would like to change. Your contributions will help enhance the project further.

