"""
filename: restaurant_data_api.py

description:
This module provides a class to interact with a MongoDB database to perform operations on a "restaurants" collection.
It contains methods to perform various operations on the "restaurants" collection, such as finding restaurants in a specific borough,
finding the top N restaurants by their latest grade, counting the number of restaurants in each borough, and more.


Author: Yinzheng Xiong
Date: 10/28/2024
"""

from pymongo import MongoClient


class RestaurantDataAPI:
    '''
    A class to interact with a MongoDB database to perform operations on a "restaurants" collection.

    Attributes:
        client (MongoClient): A MongoClient object to connect to MongoDB.
        db: The database instance connected to.
        restaurants: The collection instance for "restaurants".
    '''
    def __init__(self, uri="mongodb://localhost:27017/", db_name="hw3"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.restaurants = self.db.restaurants

    def find_restaurants_in_borough(self, borough_name):
        '''
        Find restaurants in a specific borough.
        :param borough_name:  Name of the borough
        :return:  List of restaurants in the specified borough
        '''
        return list(self.restaurants.find({"borough": borough_name}))

    def bottom_n_restaurants_by_latest_inspection_score(self, n=5):
        '''
        Retrieves the top N restaurants with the worst health inspection scores.
        This is determined by their most recent health inspection grade, where a higher score indicates more violations.
        :param n:  Number of restaurants to return
        :return:  List of the top N restaurants by their latest grade
        '''
        pipeline = [
            {"$addFields": {"latestGrade": {"$arrayElemAt": ["$grades", -1]}}}, # Add a field for the latest grade of each restaurant
            {"$sort": {"latestGrade.score": -1}},  # Sort by latest grade score in descending order
            {"$limit": n}
        ]
        return list(self.restaurants.aggregate(pipeline))

    def count_restaurants_in_each_borough(self):
        '''
        Count the number of restaurants in each borough.
        :return:  List of dictionaries containing the count of restaurants in each borough
        '''
        pipeline = [
            {"$group": {"_id": "$borough", "count": {"$sum": 1}}}
        ]
        return list(self.restaurants.aggregate(pipeline))

    def find_restaurants_in_geo_area(self, polygon):
        '''
        Find restaurants in a specified geographical area, defined by a polygon
        :param polygon:  List of coordinates for the polygon
        :return:  List of restaurants in the specified area
        '''
        query = {
            "address.coord": {
                "$geoWithin": {
                    "$geometry": {
                        "type": "Polygon",
                        "coordinates": [polygon]
                    }
                }
            }
        }
        return list(self.restaurants.find(query))


    def find_restaurants_sorted_by_cuisine(self, cuisine, order=1):
        '''
        Find restaurants of a specific cuisine, sorted by name.
        :param cuisine:  Name of the cuisine
        :param order:  Sort order (1 for ascending, -1 for descending)
        :return:  List of restaurants of the specified cuisine, sorted by name
        '''
        return list(self.restaurants.find({"cuisine": cuisine}).sort("name", order))

    def find_restaurants_with_low_score(self, score_threshold=10):
        '''
        Find restaurants with a score below a specified threshold.
        :param score_threshold:  Minimum score threshold
        :return:  List of restaurants with a score below the specified threshold
        '''
        return list(self.restaurants.find({"grades.0.score": {"$lt": score_threshold}}))

    def count_restaurants_high_score(self, score_threshold=20):
        '''
        Count the number of restaurants with a score above a specified threshold.
        :param score_threshold:  Minimum score threshold
        :return:  Number of restaurants with a score above the specified threshold
        '''
        return self.restaurants.count_documents({"grades.score": {"$gt": score_threshold}})

    def average_score_by_cuisine(self):
        '''
        Calculate the average score for each cuisine.
        :return:  List of dictionaries containing the average score for each cuisine
        '''
        pipeline = [
            {"$unwind": "$grades"},
            {"$group": {"_id": "$cuisine", "averageScore": {"$avg": "$grades.score"}}}
        ]
        return list(self.restaurants.aggregate(pipeline))


    def find_restaurants_never_below_threshold(self, criteria_field, prohibited_values):
        """
        A filter for finding documents in the "restaurants" collection that have never
        recorded a submission where the array of a field of metrics fell outside a
        critical window of expectations

        :param criteria_field: The structure of the field inside the patient documents. Example: 'grades.grade'
        :param prohibited_values: The upper and nonpermissible out-of-bounds slates. A sample could be ['B', 'C', 'D', 'E', 'F'].
        :return: A list of the restaurants that have never received any of the non-desirable (herewith, under-curve) declared stamps.
        """
        condition = {criteria_field: {"$nin": prohibited_values}}
        return list(self.restaurants.find(condition))

    def specific_borough_restaurants_with_grade(self, borough, grade):
        '''
        Find restaurants in a specific borough with a specific grade.
        :param borough:  Name of the borough
        :param grade:  Grade to search for
        :return:  List of restaurants in the specified borough with the specified grade
        '''
        return list(self.restaurants.find({"borough": borough, "grades.grade": grade}))





