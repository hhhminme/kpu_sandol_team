import json
# import lambda_prototype_module as Module
def lambda_handler(event, context):
    parameter_error = "[Parameter Error] 잘못된 파라미터가 전달되었습니다."
    try:
        if event.get('body') is None:
            raise Exception(parameter_error)
        request_body = json.loads(event['body'])
        param = request_body['action']['params']
        key = list(param.keys())  # 키가 여러개 들어올 경우는 생각해봐야 함. -> 그런 경우가 있을지부터 의문

        result_value = None
        if key[0]  == 'station':
            result_value = Module.CrawlingFunction.subway(Module.CrawlingFunction, station=str(param[key[0]]))
        elif key[0]  == 'meal':
            result_value = Module.CrawlingFunction.random_meal(Module.CrawlingFunction)
        elif key[0]  == 'suid':
            if 'd38639b2a8ede3ff7f3ae424e41a38acf7b05d8c3b238cf8861c55a9012f6f5895' == str(request_body['userRequest']['user']['properties']['botUserKey']):
                result_value = '권한이 있어요'
            else:
                result_value = '권한이 없어요'
        elif key[0]  == 'up_feedback':
            result_value = Module.CrawlingFunction.upload_feedback(Module.CrawlingFunction, params=str(param[key[0]]))
        elif key[0]  == 'upload_date':
            result_value = Module.s3IOEvent.upload_meal(Module.s3IOEvent, str(json.loads(param[key[0]])["date"]), param[key[1]], param[key[2]], param[key[3]], str(request_body['userRequest']['user']['properties']['botUserKey']))

        elif key[0] == 'restaurant_name':
            result_value = Module.s3IOEvent.read_meal(Module.s3IOEvent,str(param[key[0]]))

        elif key[0] == 'get_id':
            result_value = str(request_body['userRequest']['user']['properties']['botUserKey'])

        else:
            raise Exception(parameter_error)
    except Exception as e:
        result_value = str(e)
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

    return {
        'statusCode':200,
        'body': json.dumps(result),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }
import pprint
def lambda_handler2():
    result_value = None
    key = 'test'
    try:
        if key == 'station':
            result_value = Module.CrawlingFunction.subway(Module.CrawlingFunction, station=str(param[key]))
        elif key == 'meal':
            result_value = Module.CrawlingFunction.random_meal(Module.CrawlingFunction)
        elif key == 'feedback':
            result_value = Module.s3IOEvent.upload_feedback(Module.CrawlingFunction, params=str(param[key]))
        elif key == 'upload_date':
            result_value = Module.s3IOEvent.upload_meal(Module.s3IOEvent,"미가식당","d38639b2a8ede3ff7f3ae424e41a38acf7b05d8c3b238cf8861c55a9012f6f5895","2018-11-23","순대 김치찌개 햄구이", "김치 계란 만두")
        elif key == 'test':
            result_value = Module.s3IOEvent.read_meal(Module.s3IOEvent,"미가식당")
        else:
            raise Exception("[Parameter Error] 잘못된 파라미터가 전달되었습니다.")

    except Exception as e:
            result_value = str(e)

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
    return {
        'statusCode':200,
        'body': json.dumps(result),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }

print(lambda_handler2())
