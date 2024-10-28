from locust import HttpUser, SequentialTaskSet, task, between
import random
import datetime

class UserBehavior(SequentialTaskSet):
    def on_start(self):
        # 生成随机的中国大陆身份证号作为用户名
        self.user_id = "110000198607221435"
        self.password = "password123"  # 假设密码固定

    def generate_id_number(self):
        # 生成随机的身份证号
        # 地址码(6位)
        addr_code = random.choice(['110000', '120000', '130000', '140000', '150000'])  # 示例省份代码
        # 出生日期(8位)
        start_date = datetime.date(1970, 1, 1)
        end_date = datetime.date(2000, 12, 31)
        days_between_dates = (end_date - start_date).days
        random_days = random.randint(0, days_between_dates)
        birth_date = start_date + datetime.timedelta(days=random_days)
        birth_date_str = birth_date.strftime('%Y%m%d')
        # 顺序码(3位)
        seq_code = str(random.randint(100, 199))
        # 前17位
        id_number_17 = addr_code + birth_date_str + seq_code
        # 计算校验码
        check_code = self.calculate_checksum(id_number_17)
        # 完整身份证号
        id_number = id_number_17 + check_code
        return id_number

    def calculate_checksum(self, id17):
        # 计算身份证校验码
        weight_factors = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
        validate_codes = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')
        sum_total = sum(int(id17[i]) * weight_factors[i] for i in range(17))
        mod_value = sum_total % 11
        return validate_codes[mod_value]

    @task
    def chat(self):
        # 步骤4：用户调用文本安全检测接口
        response = self.client.post("/text_content_check", json={
            "text": "你好"
        })
        # 如果返回结果为成功，则继续发送聊天消息
        if response.status_code == 200:
            response = self.client.post("/textchat", json={
                "user_name": self.user_id,
                "text": "你好"
            })
            print(response)

class WebsiteUser(HttpUser):
    host = "http://47.108.135.99"
    tasks = [UserBehavior]
    wait_time = between(1, 3)
