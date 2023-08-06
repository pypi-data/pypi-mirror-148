import unittest
from unittest import result
from urllib import response
from xmlrpc.client import ResponseError
import os
import time
#import sys
#sys.path.insert(0, '..')
from unsplashapi import UnsplashAPI


LOAD_FROM_ENV = True

if LOAD_FROM_ENV:
    access_keys = [os.environ['ACCESSKEY'], os.environ['ACCESSKEY2'], os.environ['ACCESSKEY3']]
else:
    with open('keys.txt', 'r') as txt_file:
        access_keys = [key.strip() for key in txt_file]


class TestAPICollections(unittest.TestCase):
    """
    This class implements test for collection endpoint.
    This class only tests responses from endpoints with read access.
    """
    # Params
    page_limit = 2
    items_per_page = 5
    # Dict keys to check
    check_keys = ['id', 'title', 'description', 'published_at']
    # Check collection IDS
    collection_id = 2001768
    collection_title = 'Life in the Deep'

    access_key_idx = 0

    # Init API
    api = UnsplashAPI(access_key=access_keys[access_key_idx])

    # General Test
    def test_init(self):
        self.assertIsInstance(self.api, UnsplashAPI)

    # Collections
    def test_list_collections_paginate(self):
        try:
            response = self.api.list_collections_paginate(page_limit=self.page_limit, 
                                                        items_per_page=self.items_per_page)            
            results = [element for element in response]
        except Exception:
            # Workaround for Rate Limits
            rate_limit = int(self.api.get_current_rate_limit())
            if rate_limit == 0:
                print('No Remaining Rate Limits.', rate_limit)
                while rate_limit == 0:
                    self.access_key_idx += 1
                    if self.access_key_idx == len(access_keys):
                        self.access_key_idx = 0
                    self.api.access_key = access_keys[self.access_key_idx]
                    rate_limit = int(self.api.get_current_rate_limit())

            response = self.api.list_collections_paginate(page_limit=self.page_limit, 
                                                        items_per_page=self.items_per_page)            
            # Perform request again
            results = [element for element in response]

        self.assertEqual(self.page_limit, len(results))
        self.assertEqual(self.items_per_page, len(results[0]))

    def test_list_collection(self):
        try:    
            response = self.api.list_collection(page=1, items_per_page=self.items_per_page)
        except Exception:
            # Workaround for Rate Limits
            rate_limit = int(self.api.get_current_rate_limit())
            if rate_limit == 0:
                print('No Remaining Rate Limits.', rate_limit)
                while rate_limit == 0:
                    self.access_key_idx += 1
                    if self.access_key_idx == len(access_keys):
                        self.access_key_idx = 0
                    self.api.access_key = access_keys[self.access_key_idx]
                    rate_limit = int(self.api.get_current_rate_limit())
            # Perform request again
            response = self.api.list_collection(page=1, items_per_page=self.items_per_page)

        self.assertEqual(self.items_per_page, len(response))
        element = response[0]
        self.assertIsInstance(element, dict)
        for ckey in self.check_keys:
            self.assertIn(ckey, element.keys())
    
    def test_get_collection_by_id(self):
        try:
            response = self.api.get_collection_by_id(collection_id=self.collection_id)
        except Exception:
            # Workaround for Rate Limits
            rate_limit = int(self.api.get_current_rate_limit())
            if rate_limit == 0:
                print('No Remaining Rate Limits.', rate_limit)
                while rate_limit == 0:
                    self.access_key_idx += 1
                    if self.access_key_idx == len(access_keys):
                        self.access_key_idx = 0
                    self.api.access_key = access_keys[self.access_key_idx]
                    rate_limit = int(self.api.get_current_rate_limit())
            # Perform request again
            response = self.api.get_collection_by_id(collection_id=self.collection_id)

        self.assertIsInstance(response, dict)
        self.assertEqual(response['id'], str(self.collection_id))
        self.assertEqual(response['title'], self.collection_title)
    
    def test_get_collection_photos(self):
        try:
            response = self.api.get_collection_photos(collection_id=self.collection_id,
                                                    page_limit=self.page_limit, 
                                                    per_page=self.items_per_page)
            results = [element for element in response]
        except Exception:
            # Workaround for Rate Limits
            rate_limit = int(self.api.get_current_rate_limit())
            if rate_limit == 0:
                print('No Remaining Rate Limits.', rate_limit)
                while rate_limit == 0:
                    self.access_key_idx += 1
                    if self.access_key_idx == len(access_keys):
                        self.access_key_idx = 0
                    self.api.access_key = access_keys[self.access_key_idx]
                    rate_limit = int(self.api.get_current_rate_limit())
            print('Current Rate Limit', self.api.get_current_rate_limit())
            # Perform request again
            results = [element for element in response]

        self.assertEqual(self.page_limit, len(results))
        self.assertEqual(self.items_per_page, len(results[0]))
        self.assertIsInstance(results[0][0], dict)
    
    def test_get_related_collections(self):
        try:
            response = self.api.get_related_collections(collections_id=self.collection_id)
        except Exception:
            # Workaround for Rate Limits
            rate_limit = int(self.api.get_current_rate_limit())
            if rate_limit == 0:
                print('No Remaining Rate Limits.', rate_limit)
                while rate_limit == 0:
                    self.access_key_idx += 1
                    if self.access_key_idx == len(access_keys):
                        self.access_key_idx = 0
                    self.api.access_key = access_keys[self.access_key_idx]
                    rate_limit = int(self.api.get_current_rate_limit())
            # Perform request again
            response = self.api.get_related_collections(collections_id=self.collection_id)

        self.assertIsInstance(response, list)

        # Check keys in one response
        element = response[0]
        for ckey in self.check_keys:
            self.assertIn(ckey, element.keys())

class TestAPIPhotos(unittest.TestCase):
    """
    This class implements test for photos endpoint.
    This class only tests responses from endpoints with read access.
    """
    # Params
    page_limit = 2
    items_per_page = 5
    # Dict keys to check
    check_keys = ['id', 'description', 'urls', 'likes']
    # Check collection IDS
    photo_id = 'tCyI0KY9jTs'


    access_key_idx = 0
    # Init API
    api = UnsplashAPI(access_key=access_keys[access_key_idx])

    # General Test
    def test_init(self):
        self.assertIsInstance(self.api, UnsplashAPI)

    def test_list_photos_paginate(self):
        try:
            response = self.api.list_photos_paginate(page_limit=self.page_limit, 
                                                    items_per_page=self.items_per_page)            
            results = [element for element in response]
        except Exception:
            # Workaround for Rate Limits
            rate_limit = int(self.api.get_current_rate_limit())
            if rate_limit == 0:
                print('No Remaining Rate Limits.', rate_limit)
                while rate_limit == 0:
                    self.access_key_idx += 1
                    if self.access_key_idx == len(access_keys):
                        self.access_key_idx = 0
                    self.api.access_key = access_keys[self.access_key_idx]
                    rate_limit = int(self.api.get_current_rate_limit())

            response = self.api.list_photos_paginate(page_limit=self.page_limit, 
                                                        items_per_page=self.items_per_page)            
            # Perform request again
            results = [element for element in response]

        self.assertEqual(self.page_limit, len(results))
        self.assertEqual(self.items_per_page, len(results[0]))
    
    def test_list_photos(self):
        try:
            response = self.api.list_photos(items_per_page=self.items_per_page)            
        except Exception:
            # Workaround for Rate Limits
            rate_limit = int(self.api.get_current_rate_limit())
            if rate_limit == 0:
                print('No Remaining Rate Limits.', rate_limit)
                while rate_limit == 0:
                    self.access_key_idx += 1
                    if self.access_key_idx == len(access_keys):
                        self.access_key_idx = 0
                    self.api.access_key = access_keys[self.access_key_idx]
                    rate_limit = int(self.api.get_current_rate_limit())

            response = self.api.list_photos(page_limit=self.page_limit, 
                                                        items_per_page=self.items_per_page)            
        self.assertEqual(self.items_per_page, len(response))
        for key in self.check_keys:
            self.assertIn(key, response[0].keys())
        
    
    def test_get_photo_by_id(self):
        try:
            response = self.api.get_photo_by_id(photo_id=self.photo_id)            
        except Exception:
            # Workaround for Rate Limits
            rate_limit = int(self.api.get_current_rate_limit())
            if rate_limit == 0:
                print('No Remaining Rate Limits.', rate_limit)
                while rate_limit == 0:
                    self.access_key_idx += 1
                    if self.access_key_idx == len(access_keys):
                        self.access_key_idx = 0
                    self.api.access_key = access_keys[self.access_key_idx]
                    rate_limit = int(self.api.get_current_rate_limit())

            response = self.api.get_photo_by_id(photo_id=self.photo_id)            
        
        self.assertIsInstance(response, dict)
        # Add more tests here
    
    def test_get_random_photo(self):
        try:
            response = self.api.get_random_photo()            
        except Exception:
            # Workaround for Rate Limits
            rate_limit = int(self.api.get_current_rate_limit())
            if rate_limit == 0:
                print('No Remaining Rate Limits.', rate_limit)
                while rate_limit == 0:
                    self.access_key_idx += 1
                    if self.access_key_idx == len(access_keys):
                        self.access_key_idx = 0
                    self.api.access_key = access_keys[self.access_key_idx]
                    rate_limit = int(self.api.get_current_rate_limit())

            response = self.api.get_random_photo()            
        
        self.assertIsInstance(response, dict)
        # Add more tests here

    def test_get_photo_statistics(self):
        try:
            response = self.api.get_photo_statistics(photo_id=self.photo_id)            
        except Exception:
            # Workaround for Rate Limits
            rate_limit = int(self.api.get_current_rate_limit())
            if rate_limit == 0:
                print('No Remaining Rate Limits.', rate_limit)
                while rate_limit == 0:
                    self.access_key_idx += 1
                    if self.access_key_idx == len(access_keys):
                        self.access_key_idx = 0
                    self.api.access_key = access_keys[self.access_key_idx]
                    rate_limit = int(self.api.get_current_rate_limit())

            response = self.api.get_photo_statistics(photo_id=self.photo_id)            
        
        self.assertIsInstance(response, dict)
        # Add more tests here

    def test_track_photo_download(self):
        try:
            response = self.api.track_photo_download(photo_id=self.photo_id)            
        except Exception:
            # Workaround for Rate Limits
            rate_limit = int(self.api.get_current_rate_limit())
            if rate_limit == 0:
                print('No Remaining Rate Limits.', rate_limit)
                while rate_limit == 0:
                    self.access_key_idx += 1
                    if self.access_key_idx == len(access_keys):
                        self.access_key_idx = 0
                    self.api.access_key = access_keys[self.access_key_idx]
                    rate_limit = int(self.api.get_current_rate_limit())

            response = self.api.track_photo_download(photo_id=self.photo_id)            
        
        self.assertIsInstance(response, dict)
        # Add more tests here

    

    

    
    


    
