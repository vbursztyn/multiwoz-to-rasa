# -*- coding: utf-8 -*-
"""
MultiWOZ to Rasa
"""

import json
import string
import nltk
import os

def loadDomainStories(readFile):
    with open(readFile, 'r') as f_in:
        data = json.load(f_in)
    
    domainStories = []
    for story in data:
        domainStories.append(data[story])
        
    return domainStories

    
def generateRasaDomain(domainStories, writeFile):
    print('  Domain generation: getting entities...\n')
    entities = getAllEntities(domainStories)
    print('  Domain generation: getting intents...\n')
    intents = getAllIntents(domainStories)
    print('  Domain generation: getting actions...\n')
    actions = getAllActions(domainStories)
    # to-do: figure out response generation.
    
    print('  Domain generation: writing to file...\n')
    buildRasaDomain(entities, intents, actions, writeFile)

def buildRasaDomain(entities, intents, actions, writeFile):
    with open(writeFile, 'w') as f_out:
        f_out.write('slots:\n')
        for entity in entities:
            f_out.write('  ' + entity + ':\n')
            f_out.write('    type: text\n')
        f_out.write('\n' + 'entities:\n')
        for entity in entities:
            f_out.write('- ' + entity + '\n')
        f_out.write('\n' + 'intents:\n')
        for intent in intents:
            f_out.write(' - ' + intent + '\n')
        f_out.write('\n' + 'actions:\n')
        for action in actions:
            f_out.write('- ' + action + '\n')
        f_out.write('\n' + 'responses:\n')
        for action in actions:
            f_out.write('  ' + action + ':\n' + '  - text: \"TEMP: NEED TO FIGURE OUT RESPONSES.\"\n')
        f_out.write('\n' + 'session_config:\n  session_expiration_time: 60\n  carry_over_slots_to_new_session: true')
            

def getAllActions(domainStories):
    actionsList = []
    for story in domainStories:
        for turn in story['log']:
            if turn['metadata']:
                actionsList = actionsList + intentsFromTurn(turn)
    
    return list(dict.fromkeys(actionsList))

def getAllEntities(domainStories):
    entitiesList = []
    for story in domainStories:
        for turn in story['log']:
            if not turn['metadata']:
               entitiesList = entitiesList + entitiesFromTurn(turn)
               
    return list(dict.fromkeys(entitiesList))
    
            
def entitiesFromTurn(turn):
    entities = []   
    try:
        for slot in turn['span_info']:
            entities.append(slot[1].lower())
    except:
        pass   
    return entities

def getAllIntents(domainStories):
    intentsList = []
    for story in domainStories:
        for turn in story['log']:
            if not turn['metadata']:
                intentsList = intentsList + intentsFromTurn(turn)
    
    return list(dict.fromkeys(intentsList))

def intentsFromTurn(turn):
    intents = []
    try:
        for intent in list(turn['dialog_act'].keys()):
            intents.append(intent.lower())
    except:
        pass
    return intents

def generateRasaStories(domainStories, writeFile):
    with open(writeFile, 'w') as f_out:
        for i, story in enumerate(domainStories):
            f_out.write('## path nr %s\n' %i)
            intents = constructRasaStory(story)
            try:
                for intent in intents:
                    f_out.write(intent + '\n')
            except:
                pass
            f_out.write('\n')
        
def constructRasaStory(story):
        intents = []
        for turn in story['log']:
            try:
                for intent in list(turn['dialog_act'].keys()):
                    if not turn['metadata']:
                        intents.append(" * " + intent.lower())
                    else:
                        intents.append("  - " + intent.lower())
            except:
                pass
        return intents

def generateUtterances(domainStories, writeFile):
    utterancesByIntent = getAllUtterances(domainStories)
    
    with open(writeFile, 'w') as f_out:
        for intent in utterancesByIntent:
            f_out.write('## intent:%s\n' %intent.lower())
            for utter in utterancesByIntent[intent]:
                f_out.write('- %s\n' %utter)
            f_out.write('\n')
    
def getAllUtterances(domainStories):
    utterancesByIntent = {}
    
    for story in domainStories:
        for turn in story['log']:
            if not turn['metadata']:
                try:
                    intents = list(turn['dialog_act'].keys())
                    for intent in intents:
                        if intent not in utterancesByIntent:
                            utterancesByIntent[intent] = []
                        utterancesByIntent[intent].append(annotate_utterance(turn['text'], turn['span_info']))
                except:
                    pass
    
    return utterancesByIntent
            
def annotate_utterance(utter, spans):
    utter = ' '.join(nltk.word_tokenize(utter.lower()))
    
    for span in spans:
        normalized_token = span[2].lower()
        
        if ' %s ' %(normalized_token) not in utter\
            and not utter.endswith(' %s' %(normalized_token))\
            and not utter.startswith('%s ' %(normalized_token)):
            
            tokens = nltk.word_tokenize(utter)
            tokens[span[-2]] = '[%s' %(tokens[span[-2]])
            tokens[span[-1]] = '%s](%s:%s)' %(tokens[span[-1]], span[1].lower(), normalized_token)
            utter = ' '.join(tokens)
    
    for span in spans:
        normalized_token = span[2].lower()
        annotation = ' [%s](%s) ' %(normalized_token, span[1].lower())
        
        token_match = ' %s ' %(normalized_token)
        if token_match in utter:
            utter = utter.replace(token_match, annotation)
        
        token_match = ' %s' %(normalized_token)
        if utter.endswith(token_match):
            utter = utter.replace(token_match, annotation)
        
        token_match = '%s ' %(normalized_token)
        if utter.startswith(token_match):
            utter = utter.replace(token_match, annotation)
    
    tokens = nltk.word_tokenize(utter)
    detokenized = nltk.tokenize.treebank.TreebankWordDetokenizer().detokenize(tokens)
    fixed_markers = detokenized.replace('] (', '](').replace('[ ','[').replace(': ',':')
    fixed_punctuation = string.punctuation.translate(str.maketrans('', '', ':()[]'))
    return fixed_markers.translate(str.maketrans('', '', fixed_punctuation)).replace(' ]',']').replace('  ',' ')
    
def main():
    readFile = 'data.json'
    rasaStoriesFile = 'stories.txt'
    rasaDomainFile = 'domain.txt'
    rasaUtterancesFile = 'nlu.txt'
    
    print('Reading file...\n')
    domainStories = loadDomainStories(readFile)
    print('Generating stories file...\n')
    generateRasaStories(domainStories, rasaStoriesFile)
    print('Generating domain file...\n')
    generateRasaDomain(domainStories, rasaDomainFile)
    print('Generating utterances file...\n')
    generateUtterances(domainStories, rasaUtterancesFile)
    print('Done (:\n')

if __name__ == "__main__":
    main()