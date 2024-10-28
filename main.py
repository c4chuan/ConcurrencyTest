from locust import HttpUser, SequentialTaskSet, task, between
import random,datetime
from sql_reset import sql_reset
# 重置数据库
sql_reset()
class UserBehavior(SequentialTaskSet):
    def on_start(self):
        self.user_id = self.generate_id_number()
        self.user_name = self.user_id[-4:]
        self.password = "testpass"
        self.turn = 0
        self.register()
        self.f_login()
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
    def register(self):
        # 实现用户注册逻辑
        response = self.client.post("/register", json={
            "user_id": self.user_id,
            "user_password": self.password
        })
        # 处理响应，存储用户信息
        if response.status_code == 200:
            print(f"用户{self.user_name}注册成功")
        else:
            print(f"用户{self.user_name}注册失败")
    def f_login(self):
        # 实现用户登录逻辑
        response = self.client.post("/login", json={
            "user_name": self.user_id,
            "password": self.password
        })
        if response.status_code == 200:
            print(f"用户{self.user_name}首次登录成功")
        else:
            print(f"用户{self.user_name}首次登录失败")
    @task(1)
    def login(self):
        # 实现用户登录逻辑
        response = self.client.post("/login", json={
            "user_name": self.user_id,
            "password": self.password
        })
        if response.status_code == 200:
            print(f"用户{self.user_name}登录成功")
        else:
            print(f"用户{self.user_name}登录失败")

        # 实现获取聊天记录逻辑
        response = self.client.post("/getHistoryChat", json={
            "user_name": self.user_id
        })
        if response.status_code == 200:
            print(f"用户{self.user_name}获取聊天记录成功")
        else:
            print(f"用户{self.user_name}获取聊天记录失败")


    @task(10)
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
            # 从结果中获取返回的文本消息
            text_message = response.json()["data"]
            self.turn+=1
            print(f"用户{self.user_name}收到回复：", text_message,"第",self.turn,"/30次")

class WebsiteUser(HttpUser):
    host = "http://47.108.135.99"
    tasks = [UserBehavior]
    wait_time = between(3, 4)  # 设置用户之间的等待时间

