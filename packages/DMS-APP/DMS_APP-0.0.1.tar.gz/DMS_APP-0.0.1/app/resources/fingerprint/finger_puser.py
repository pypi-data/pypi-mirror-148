from flask import request
from flask_restx import Resource, fields, reqparse
from ...namespace import api
from ...response_helper import get_response
import base64
import cv2
import os

createFingerPrint = api.model("CreateFingerprint", {
    "person_id": fields.String,
    "base64": fields.Raw([])
})

matchFingerPrint = api.model("MatchFingerprint", {
    "base64": fields.Raw([])
})

fingerPrintDelete = reqparse.RequestParser()
fingerPrintDelete.add_argument("fingerprint_id", type=int, required=True)


class AddFingerprint(Resource):
    @api.expect(createFingerPrint)
    def post(self):
        args = request.get_json()
        person_id = args['person_id']
        image_coll = args['base64']
        for i in range(0, len(image_coll)):
            try:
                image_binary = base64.decodebytes(bytes(image_coll[i], 'utf-8'))
                with open("app/fingerprint_img/" + str(person_id) + "_" + str(i + 1) + "_" + ".tif", 'wb') as f:
                    f.write(image_binary)
            except Exception:
                _response = get_response(404)
                _response['message'] = 'Unable to save file'
        return get_response(200)


class MatchFingerprint(Resource):
    @api.expect(matchFingerPrint)
    def post(self):
        args = request.get_json()
        for i in range(len(args["base64"])):
            image_coll = args['base64'][0]['base64str1']
            image_binary = base64.decodebytes(bytes(image_coll, 'utf-8'))
            with open("app/sample.tif", 'wb') as f:
                f.write(image_binary)
            test_original = cv2.imread("app/sample.tif")
            for file in [file for file in os.listdir("app/fingerprint_img")]:
                _image = cv2.imread("app/fingerprint_img/" + file)
                detector = cv2.SIFT_create()
                keypoints1, descriptors1 = detector.detectAndCompute(test_original, None)
                keypoints2, descriptors2 = detector.detectAndCompute(_image, None)
                matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
                knn_matches = matcher.knnMatch(descriptors1, descriptors2, 2)
                ratio_thresh = 0.7
                good_matches = []
                for m, n in knn_matches:
                    if m.distance < ratio_thresh * n.distance:
                        good_matches.append(m)
                if len(good_matches) > 100:
                    _response = get_response(200)
                    _response["person_id"] = file.split('_')[0:1]
                    return _response
            else:
                _response = get_response(404)
                _response['message'] = "No Match Found"
                return _response
