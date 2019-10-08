from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import os
import sys
import time

if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ and 'COMPUTER_VISION_ENDPOINT' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    remote_image_printed_text_url = 'https://scottie-io.s3.amazonaws.com/vslive-whiteboard.jpg'
    recognize_printed_results = computervision_client.batch_read_file(remote_image_printed_text_url, raw=True)
    operation_location_remote = recognize_printed_results.headers["Operation-Location"]
    operation_id = operation_location_remote.split("/")[-1]
    while True:
        get_printed_text_results = computervision_client.get_read_operation_result(operation_id)
        if get_printed_text_results.status not in ['NotStarted', 'Running']:
            break
        time.sleep(1)
    if get_printed_text_results.status == TextOperationStatusCodes.succeeded:
        for text_result in get_printed_text_results.recognition_results:
            for line in text_result.lines:
                print(line.text)
                print(line.bounding_box)
else:
    print('You must set both COMPUTER_VISION_SUBSCRIPTION_KEY and COMPUTER_VISION_ENDPOINT as environment variables.')
    sys.exit(1)
