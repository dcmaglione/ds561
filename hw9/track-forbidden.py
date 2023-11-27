#!env python3
# -*- coding: utf-8 -*-
# Author: Dominic Maglione (dcmag@bu.edu)
# Date: 2023-11-27 (date modified)

# ------ Imports ------- #
import os

from google.cloud import pubsub_v1

# ------ Constants ------- #
GOOGLE_CLOUD_PROJECT = 'unique-epigram-398918'

# ------- Subscriber ------- #
subscriber = pubsub_v1.SubscriberClient()
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=GOOGLE_CLOUD_PROJECT,
    topic='forbidden-countries-topic'
)
subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=GOOGLE_CLOUD_PROJECT,
    sub='forbidden-countries-subscription'
)

# ------- Callback Function ------- #


def callback(message):
    print('Received message: {}'.format(message))
    message.ack()


with pubsub_v1.SubscriberClient() as subscriber:
    future = subscriber.subscribe(subscription_name, callback)
    future.result()
