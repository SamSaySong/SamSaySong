from .models import Claim
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ClaimSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from operator import itemgetter
import requests
import os
import inspect
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
os.environ["CUDA_VISIBLE_DEVICES"]="0"

# Path to the data directory

characters = ['A', 'W', '8', 'J', 'N', 'V', 'T', '3', 'F', '6', 'X', 'P', 'H', 'Y', 'D', '4', 'E', 'U', 'C', 'B', '9', 'G', '2', 'L', 'R', 'M', 'K', '7']

img_width = 200
img_height = 50
downsample_factor = 4
# Maximum length of any captcha in the dataset
max_length = 4

# Mapping characters to integers
char_to_num = layers.StringLookup(vocabulary=list(characters), mask_token=None)

# Mapping integers back to original characters
num_to_char = layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), mask_token=None, invert=True
)
#load model
model = keras.models.load_model(CurDir+'/model_V1')
# Get the prediction model by extracting layers till the output layer
prediction_model = keras.models.Model(
    model.get_layer(name="image").input, model.get_layer(name="dense2").output
)
prediction_model.summary()

def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
@csrf_exempt 
def OCR_VINA(request):
    try:
        # Imaginary function to handle an uploaded file.
        handle_uploaded_file(request.FILES['media'])
        img = tf.io.read_file(request.FILES['media'].name)
        # 2. Decode and convert to grayscale
        img = tf.io.decode_png(img, channels=1)
        # 3. Convert to float32 in [0, 1] range
        img = tf.image.convert_image_dtype(img, tf.float32)
        # 4. Resize to the desired size
        img = tf.image.resize(img, [img_height, img_width])
        # 5. Transpose the image because we want the time
        # dimension to correspond to the width of the image.
        img = tf.transpose(img , perm=[1, 0, 2])
        img=tf.expand_dims(img, axis=0)
        pred = prediction_model.predict(img)
        input_len = np.ones(pred.shape[0]) * pred.shape[1]
        # Use greedy search. For complex tasks, you can use beam search
        results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
            :, :max_length
        ]
        res = tf.strings.reduce_join(num_to_char(results[0])).numpy().decode("utf-8")
        return JsonResponse({'data': 'success','result': res })
    except Exception as e:
        return JsonResponse({'data': 'error','result': e })


class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all().order_by('id')
    serializer_class = ClaimSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company_claim']