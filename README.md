## CS 496 - Statistical Learning
## Integrating MultiWoz 2.1 to Rasa.ai

#### Steps:
1. Unzip data.zip
2. Run `pip install -r requirements.txt`
3. Run `jupyter notebook`
4. Notebook `parse_restaurant_domain.ipynb` takes in data.json, selects stories from the restaurants domain, and transforms these stories to the format of Rasa's annotated utterances.
5. TO-DO: Now that the restaurants domain is fully covered (we're generating both nlu.md and stories.md), scale this ETL process to the entire MultiWoZ 2.1 dataset, including the stories that span multiple domains.

------
Current authors: v-bursztyn@u.northwestern.edu
