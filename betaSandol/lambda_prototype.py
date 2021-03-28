import json
import lambda_prototype_module as Module
import base64

def lambda_handler(event, context):
    request_body = json.loads(event['body'])
    request_body = json.loads(base64.b64decode(request_body))
    param = request_body['action']['params']
    key = list(param.keys())  # 입력으로 들어오는 값을 여기서 처리함
    # 여러개 들어오는 경우 필수 파라미터 명이 key[0]에 들어감

    result_value = None
    try:
        if key[0] == "location":  # 날씨 관련 함수로 넘어감

            result_value = Module.CrawlingFunction.weather(Module.CrawlingFunction, param[key[0]])

        elif key[0] == 'station':  # 지하철 정보
            result_value = Module.CrawlingFunction.subway(Module.CrawlingFunction, station=str(param[key[0]]))

        elif key[0] == 'meal':  # 랜덤 식사
            result_value = Module.CrawlingFunction.random_meal(Module.CrawlingFunction)

        elif key[0] == 'suid':
            result_value = Module.s3IOEvent.read_feedback(Module.CrawlingFunction, str(param[key[0]]))

        elif key[0] == 'up_feedback':  # 피드백 업로드
            result_value = Module.s3IOEvent.upload_feedback(Module.CrawlingFunction, params=str(param[key[0]]))

        elif key[0] == 'upload_date':  # 학식 등록
            result_value = Module.s3IOEvent.upload_meal(Module.s3IOEvent, str(json.loads(param[key[0]])["date"]),
                                                        param[key[1]], param[key[2]], param[key[3]], str(
                    request_body['userRequest']['user']['properties']['botUserKey']))

        elif key[0] == 'restaurant_name':  # 학식 출력
            result_value = Module.s3IOEvent.read_meal(Module.s3IOEvent, str(param[key[0]]))

        else:
            raise Exception
            # raise Exception("[Parameter Error] 잘못된 파라미터가 전달되었습니다.")

        result = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": str(result_value)
                        }
                    }
                ]
            }
        }



    except Exception as e:
        result = "산돌이가 작업을 마무리하지 못했어요ㅠㅠ\n 피드백을 통해 어떤 기능에서 오류가 발생했는지 알려주시면 빠른 시일 내에 작동 하도록 할게요" + str(e)

    return {
        'statusCode': 200,
        'body': json.dumps(result),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }

