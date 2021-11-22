import boto3
import alphaSandol as settings
import datetime



class Feedback:
    def __init__(self):
        if not settings.DEBUG:  # 디버그모드가 아닌경우 S3를 import함
            self.S3 = boto3.resource('s3')
            self.S3_client = boto3.client('s3')
            self.bucket = self.S3.Bucket(settings.BUCKET_NAME)

        self.data = ""

    def upload_feedback(self, data):
        self.data = f"[{str(datetime.datetime.today())}] : {data}\n"
        if not settings.DEBUG:
            try:
                self.bucket.download_file(settings.FEEDBACK_FILE, settings.LOCAL_FEEDBACK_FILE)

            except Exception as e:
                return settings.GEN.set_text(
                    f"[File-Open-Error #101] 서버에서 피드백 파일을 불러오는 중 오류가 발생했어요{settings.IMOGE('emotion', 'sad')}\n{e}")

            try:
                with open(settings.LOCAL_FEEDBACK_FILE, "a", encoding="UTF-8") as f:
                    f.writelines(self.data)

            except Exception as e:
                return settings.GEN.set_text(
                    f"[File-Open-Error #102] 파일을 저장 중 오류가 발생했습니다{settings.IMOGE('emotion', 'sad')}\n{e}")

            try:
                self.S3_client.upload_file(settings.LOCAL_FEEDBACK_FILE, settings.BUCKET_NAME, settings.FEEDBACK_FILE)

            except Exception as e:
                return settings.GEN.set_text(
                    f"[File-Open-Error #103] 파일을 서버에 업로드 하는 중 오류가 발생했습니다{settings.IMOGE('emotion', 'sad')}\n{e}")

        else:   # 디버그 모드일때 발생하는 분기
            with open("../test_stored_data/feedback.txt", "a", encoding='UTF-8') as f:
                f.writelines(self.data)

        return settings.GEN.set_text(f"피드백 주셔서 감사해요! 빠른 시일내에 검토 후 적용해볼게요!{settings.IMOGE('emotion','love')}")

    def read_feedback(self, uid):
        if uid not in (settings.SANDOL_ACCESS_ID.values()):
            return settings.GEN.set_text("권한이 없습니다")

        if not settings.DEBUG:
            try:
                self.bucket.download_file(settings.FEEDBACK_FILE, settings.LOCAL_FEEDBACK_FILE)

            except Exception as e:
                settings.GEN.set_text(f"[File-Open-Error #111] 서버에서 피드백 파일을 불러오는 중 오류가 발생했어요\n{e}")

            try:
                with open(settings.LOCAL_FEEDBACK_FILE, 'r', encoding='UTF-8') as f:
                    txt = ''.join(f.readlines())

            except Exception as e:
                return settings.GEN.set_text(f"[File-Open-Error #112] 파일을 읽는 중 오류가 발생했습니다\n{e}")

            return settings.GEN.set_text(txt)

        else:   # 디버그 모드일때 발생하는 분기
            with open("../test_stored_data/feedback.txt", encoding='UTF-8') as f:
                txt = ''.join(f.readlines())
            return settings.GEN.set_text(txt)

    def delete_feedback(self, uid):
        if uid not in (settings.SANDOL_ACCESS_ID.values()):
            return settings.GEN.set_text("권한이 없습니다")

        basic_text = "#feedbacks\n"
        if not settings.DEBUG:
            try:
                self.bucket.download_file(settings.FEEDBACK_FILE, settings.LOCAL_FEEDBACK_FILE)
            except Exception as e:
                return settings.GEN.set_text(f"[File-Open-Error #113] 서버에서 피드백 파일을 불러오는 중 오류가 발생했어요\n{e}")

            try:
                with open(settings.LOCAL_FEEDBACK_FILE, 'w', encoding="UTF-8") as f:
                    f.writelines(basic_text)

            except Exception as e:
                return settings.GEN.set_text(f"[File-Open-Error #114] 파일 데이터를 삭제 중 오류가 발생했습니다{e}")

            try:
                s3 = boto3.client('s3')
                s3.upload_file(settings.LOCAL_FEEDBACK_FILE, settings.BUCKET_NAME, settings.FEEDBACK_FILE)

            except Exception as e:
                return settings.GEN.set_text(f"[File-Open-Error #115] 파일을 서버에 업로드 하는 중 오류가 발생했습니다{e}")

        else:   # 디버그 모드일때
            with open("../test_stored_data/feedback.txt", "w", encoding='UTF-8') as f:
                f.writelines(basic_text)

        return settings.GEN.set_text("성공적으로 파일 내용을 삭제했습니다")
