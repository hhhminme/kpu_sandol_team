import json
PARAM = "ann"
PARAM_DATA = '공지'

JSON_DATA = {
    'body': {
        "intent": {
            "id": "ttc0v82yotpkittnmfpq9lcy",
            "name": "블록 이름"
        },
        "userRequest": {
            "timezone": "Asia/Seoul",
            "params": {
                "ignoreMe": "true"
            },
            "block": {
                "id": "ttc0v82yotpkittnmfpq9lcy",
                "name": "블록 이름"
            },
            "utterance": "발화 내용",
            "lang": 'null',
            "user": {
                "id": "616332",
                "type": "accountId",
                "properties": {}
            }
        },
        "bot": {
            "id": "5e0f180affa74800014bd33d",
            "name": "봇 이름"
        },
        "action": {
            "name": "o8fhv36eao",
            "clientExtra": 'null',
            "params": {
                PARAM : PARAM_DATA
            },
            "id": "koow1xlhycjsjacfcqy49w6w",
            "detailParams": {
                "weather": {
                    "origin": "정왕 날씨 궁금해",
                    "value": "정왕 날씨 궁금해",
                    "groupName": ""
                }
            }
        }
    }
}
TEST_EVENT = json.dumps(JSON_DATA)