if __name__ == '__main__':
    # main 파일을 엔트리포인트로 사용할 경우, path에 폴더 경로를 추가해 절대 경로로 임포트가 가능하게 함
    from sys import path
    import os
    path.append(os.path.dirname(__file__))

import json
import base64
# import pprint
# JSON_DATA =  {
#     'body':{
#   "intent": {
#     "id": "ttc0v82yotpkittnmfpq9lcy",
#     "name": "블록 이름"
#   },
#   "userRequest": {
#     "timezone": "Asia/Seoul",
#     "params": {
#       "ignoreMe": "true"
#     },
#     "block": {
#       "id": "ttc0v82yotpkittnmfpq9lcy",
#       "name": "블록 이름"
#     },
#     "utterance": "발화 내용",
#     "lang": 'null',
#     "user": {
#       "id": "616332",
#       "type": "accountId",
#       "properties": {}
#     }
#   },
#   "bot": {
#     "id": "5e0f180affa74800014bd33d",
#     "name": "봇 이름"
#   },
#   "action": {
#     "name": "o8fhv36eao",
#     "clientExtra": 'null',
#     "params": {
#       "weather": "정왕 날씨 궁금해"
#     },
#     "id": "koow1xlhycjsjacfcqy49w6w",
#     "detailParams": {
#       "weather": {
#         "origin": "정왕 날씨 궁금해",
#         "value": "정왕 날씨 궁금해",
#         "groupName": ""
#       }
#     }
#   }
# }
# }
# TEST_EVENT = json.dumps(JSON_DATA)
def lambda_handler(context, event):
    # request_body = json.loads(base64.b64decode(event))
    request_body = json.loads(event)
    param = request_body['body']['action']['params']
    key = list(param.keys())
    try:
        function_params = key[1:]
    except Exception as e:
        print(e)
        pass

    return_string = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    'simpleText': {
                        "text": f"{str(param)}\n\n산돌이 기능개선중입니다 금방 돌아올게요!"
                    }
                }
            ],
            "quickReplies": [
                {
                    "messageText": "도움말",
                    "action": "message",
                    "label": "도움말"
                }
            ]
        }
    }

    return {
        'statusCode': 200,
        'body': json.dumps(return_string),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }
# pprint.pprint(lambda_handler(".", TEST_EVENT))