if __name__ == '__main__':
    # main 파일을 엔트리포인트로 사용할 경우, path에 폴더 경로를 추가해 절대 경로로 임포트가 가능하게 함
    from sys import path
    import os

    path.append(os.path.dirname(__file__))

import json
import base64
import settings
from settings import DEBUGGING as debugging



def lambda_handler(event, context):
    try:
        if settings.DEBUG:
            req = "None"  # request body
            func = "feedback_upload"  # 테스트할 함수
            params = ["BYE!!"]  # 파라미터
            params = {func: params[0]}
            access_id = 'd367f2ec55f41b4207156f4b8fce5ce885b05d8c3b238cf8861c55a9012f6f5895'  # 접근 ID

            return_json = function_handler(func, req, params, access_id)

        else:
            request_body = event['body']
            request_body = json.loads(base64.b64decode(request_body))  # base64로 디코딩해야 제대로된 값을 받음

            param = request_body['action']['params']  # request json 접근용
            key = list(param.keys())
            func = key[0]  # 함수 호출시 사용할 값
            ACCESS_ID = str(request_body['userRequest']['user']['id'])  # 접근 권한을 가진 ID 확인용
            return_json = function_handler(func, request_body, param, ACCESS_ID)


    except Exception as e:
        return_json = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": f"{settings.DEBUGGING('debug', 'main.lambda_handler', e)}"
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


def function_handler(func, req, param, access_id):
    vals = list(param.values())  # 함수에 파라미터에 사용할 값
    return_json = ''
    if func == 'weather':  # 날씨 관련
        from weather import Weather
        return_json = Weather().weather()

    elif func == "covid":  # 코로나 관련
        from covid import Covid
        return_json = Covid().today_covid()

    elif func == "feedback_upload" or func == "read_feedback":  # 피드백 관련
        from feedback import Feedback
        feedback_class = Feedback()

        if func == "feedback_upload":
            return_json = feedback_class.upload_feedback(vals[0])

        elif func == "read_feedback":
            if str(vals[0]) == '2':  # 삭제
                return_json = feedback_class.delete_feedback(access_id)

            else:  # 접근
                return_json = feedback_class.read_feedback(access_id)


    elif func in ["store_name", "read_meal", "reset_meal", "time_meal", "payment_meal"]:
        import restaurant
        meal_class = restaurant.AboutMeal()

        if func == "store_name":  # 학식 업로드
            upload_date = json.loads(vals[3])['date']
            return_json = meal_class.upload_meal(vals[0], vals[1], vals[2], upload_date, access_id)

        elif func == "read_meal":  # 식단 읽기
            return_json = meal_class.read_meal(access_id)

        elif func == "reset_meal":  # 학식 초기화
            upload_date = json.loads(vals[3])['date']
            return_json = meal_class.reset_meal(access_id, upload_date)

        elif func == "time_meal":  # 영업시간
            return_json = restaurant.time_meal()

        else:  # 결제 시스템 (사용에 어려울 수도 있음 => kakao pay 송금 제한)
            return_json = restaurant.payment_meal()

    elif func == "ann":  # 공지사항
        from announcement import Announcement
        return_json = Announcement().announce()

    elif func in ["subway", "last_subway"]:
        import subway
        if func == "subway":
            from return_type_generator import ReturnType
            time = json.loads(req['action']['detailParams']['date_time']['value'])
            return_json = ReturnType().set_text(str(type(time)))

        else:
            return_json = subway.LastTraffic().real_time_traffic()

    elif func == "commerce":
        import test_block
        return_json = test_block.commerce_test()

    elif func == "perm_chk":
        from return_type_generator import ReturnType as GEN
        return_json = GEN().set_text(access_id)

    else:
        from return_type_generator import ReturnType as GEN
        GEN().set_text(text=debugging("error", "main.function_handler", "전달된 파라미터가 잘못되었습니다."))

    return {
        'statusCode': 200,
        'body': json.dumps(return_json, ensure_ascii=False),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }

# if __name__ == "__main__":  # Deploy 할때 무조건 주석처리 하기
#     import pprint
#     func_call: json = lambda_handler("event", "context")
#     pprint.pprint(func_call)  # 디버깅용 함수 호출
    # print(json.loads(func_call['body']))  # json 유니코드 -> UTF 확인용
