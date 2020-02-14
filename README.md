## CS 496 - Statistical Learning
------
## Integrating MultiWoz 2.1 to Rasa.ai

#### Steps:
1. Unzip data.zip
2. pip install -r requirements.txt
3. jupyter notebook
4. Notebook `parse_restaurant_domain.ipynb` takes in data.json, selects stories from the restaurants domain, and transforms these stories to the format of Rasa's annotated utterances.
5. TO-DO: Besides converting the format to Rasa NLU, do the same for Rasa Core. That is, keep focus on the restaurants domain and go from stories in MultiWoz to Rasa stories.
