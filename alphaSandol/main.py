import json
import base64
import alphaSandol as constant

if __name__ == '__main__':
    # main 파일을 엔트리포인트로 사용할 경우, path에 폴더 경로를 추가해 절대 경로로 임포트가 가능하게 함
    from sys import path
    import os

    path.append(os.path.dirname(__file__))
    constant.DEBUG = True  # 디버깅모드 트리거


def lambda_handler(event, context):
    try:
        if constant.DEBUG:
            func = "delete_feedback"  # 테스트할 함수
            params = ["안뇽!"]  # 파라미터
            access_id = 'd367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895'  # 접근 ID

            return_json = function_handler(func, params, access_id)

        else:
            return_json = ''
            request_body = event['body']
            request_body = json.loads(base64.b64decode(request_body))  # base64로 디코딩해야 제대로된 값을 받음

            param = request_body['action']['params']  # request json 접근용
            key = list(param.keys())
            func = key[0]  # 함수 호출시 사용할 값
            key_values = list(param.values())  # 함수에 파라미터에 사용할 값
            ACCESS_ID = str(request_body['userRequest']['user']['id'])  # 접근 권한을 가진 ID 확인용
            return_json = function_handler(func, key_values, ACCESS_ID)

    except Exception as e:
        return_json = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": f"{constant.DEBUGGING('debug', 'main.lambda_handler', e)}"
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

    return return_json


def function_handler(func, key, access_id):
    return_json = ''
    if func == 'weather':   # 날씨 관련
        import weather
        return_json = weather.Weather().weather()

    elif func == "covid":   # 코로나 관련
        import covid
        return_json = covid.Covid().today_covid()

    elif func == "feedback_upload" or func == "read_feedback" or func == "delete_feedback":     # 피드백 관련
        import feedback
        feedback_class = feedback.Feedback()

        if func == "feedback_upload":
            return_json = feedback_class.upload_feedback(key[0])

        elif func == "read_feedback":
            return_json = feedback_class.read_feedback(access_id)

        else:
            return_json = feedback_class.delete_feedback(access_id)

    elif func == "store_name" or func == "read_meal" or func == "reset_meal" or func == "time_meal" or "payment_meal":
        import restaurant

    return {
        'statusCode': 200,
        'body': json.dumps(return_json),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }


if __name__ == "__main__":      # Deploy 할때 무조건 주석처리 하기
    func_call = lambda_handler("event", "context")
    print(func_call)  # 디버깅용 함수 호출
    print(json.loads(func_call['body']))  # json 유니코드 -> UTF 확인용
