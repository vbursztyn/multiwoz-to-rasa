from rasa_sdk import Action
from rasa_sdk.events import SlotSet


import os, json


class RestaurantAPI:

    restaurant_db = None

    def load_db(self):
        db_path = os.path.join(os.getcwd(), "dataset", "MultiWOZ_2.1", "restaurant_db.json")
        with open(db_path) as f_in:
            self.restaurant_db = json.load(f_in)

    def search(self, params):
        self.load_db()

        partial_results = []

        for k,v in params.items():
            if v:
                try:
                    partial_results.append(set(map(lambda x: x["name"],\
                        filter(lambda x: x[k] == v, self.restaurant_db))))
                except:
                    pass

        results = list(set.intersection(*partial_results))
        n_results = len(results)
        if not n_results:
            return "I couldn't find a restaurant matching all of your preferences."
        if n_results > 5:
            return "I found %s restaurants. Would you like to add more filters?" %(n_results)
        return "Here's what I found: %s" %(", ".join(results))


class ActionSearchRestaurants(Action):
    def name(self):
        return "action_search_restaurants"

    def run(self, dispatcher, tracker, domain):
        search_params = dict()
        params = ["name", "people", "price", "day", "food", "time", "area"]
        for param in params:
            try:
                search_params[param] = tracker.get_slot(param)
            except:
                pass

        restaurant_api = RestaurantAPI()
        restaurants = restaurant_api.search(search_params)
        dispatcher.utter_message(text="Okay. %s" %(restaurants))
        return []


class ActionSuggest(Action):
    def name(self):
        return "action_suggest"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Here's what I found.")
        dispatcher.utter_message(text=tracker.get_slot("matches"))
        return []

