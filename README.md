# CS 496 - Rasa Deployments
## Problem statement.
Domain-specific chatbot deployments have risen as companies and other service providers have shifted towards AI systems for customer interaction in order to save money and human resources. This has created a need for targeted and domain-specific chatbots that can be trained and deployed through a framework that is easily accessible and deployable in a variety of contexts. Rasa (Bocklisch et al., 2017) is a framework for building domain-specific chatbots by means of two interconnected ML-based modules:
1. Rasa NLU, which takes in utterances to (i) classify user intent, (ii) extract associated entities, and (iii) uses said entities to fill intent-related slots; and
2. Rasa Core, which takes in the last states of a conversation to predict the most likely next dialogue step.
Our goal is to apply Rasa to new task-oriented domains. We do that by resorting to MultiWOZ (Eric et al., 2019), a recently published data set that contains both single- and multi-domain stories.

## Deliverables.
The deliverables for our project are as follows:
1. An ETL process that converts raw data from MultiWOZ to a format that is fully adherent to Rasa.
2. A docker image containing a pretrained fully functional single-domain application: a restaurant booking bot that spans Rasa NLU, Rasa Core, and effectively return query results through our implementation of Rasa Actions.
3. A pretrained model spanning all data from MultiWOZ, deployed with Rasa X.
4. Configuration files deploying the built-in "restaurantbot" (not our version from MultiWOZ) to Facebook Messenger.
5. Configuration files and source code deploying our custom restaurant bot to Google Assistant as a Google Skill.

Deliverables #4 and #5 require custom steps for network configuration, ranging from network funneling through ngrok to the adherence to platform-specific requirements and standards (e.g., providing a custom "data privacy policy" in the case of Facebook or registering custom utterances to call a skill in Google Assistant).

## Set-up steps.

Requirements: Python 3.6, Tensorflow 2.1.0

1. Clone and set up this repository.
```
git clone https://github.com/vbursztyn/multiwoz-to-rasa.git
cd multiwoz-to-rasa
```

2. Install Rasa X, as well as the listed requirements in `requirements.txt `.
```
pip install rasa-x -i https://pypi.rasa.com/simple
pip install -r requirements.txt
```

You should now be able to replicate the processes for each of the mentioned deliverables.

## 1: ETL pipeline.

Steps to replicate:

1. Enter the corresponding folder in the repository.

```
cd etl-pipeline
```

2. Unzip the folder `data.zip`.

3. Run the python script `multidomain_rasa.py`.

The script takes in data.json, a copy of the MultiWOZ dataset, and transforms all stories in the dataset to the format of Rasa's annotated utterances. It also generates a `domain.yml` file that contains a list of all possible actions, entities and intents that can be detected and/or performed by the chatbot. It dumps all of this information into the folder `converted_files`.

## 2: Docker image.



## 3: Rasa X pre-trained model.

Steps to replicate:

1. Enter the corresponding directory.

```
cd rasa-x-deployment
```

2. Unzip folder `model.zip`, and extract the `tar.gz` file into the subdirectory `rasa-x-deployment/models`.

3. Start Rasa X with the command `rasa x`.

## 4: Facebook messenger restaurantbot deployment.

[![FB messenger demo](https://j.gifs.com/XL0gVo.gif)](https://www.youtube.com/watch?v=35YqSL8Oimg)

## 5: Restaurant bot Google Assistant deployment.

[![Google Assistant demo](https://j.gifs.com/Mw2RWR.gif)](https://www.youtube.com/watch?v=niHGCLBaflc)

## References
* Bocklisch, T., Faulkner, J., Pawlowski, N., & Nichol, A. (2017). Rasa: Open source language understanding and dialogue management. arXiv preprint arXiv:1712.05181.

* Eric, M., Goel, R., Paul, S., Sethi, A., Agarwal, S., Gao, S., & Hakkani-Tur, D. (2019). Multiwoz 2.1: Multi-domain dialogue state corrections and state tracking baselines. arXiv preprint arXiv:1907.01669.

