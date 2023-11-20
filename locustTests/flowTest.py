from locust import HttpUser, task, between
from locust.env import Environment
from locust.runners import LocalRunner


class PizzaUser(HttpUser):
    host = "http://localhost:3000"
    wait_time = between(1, 2)
    headers = {"Content-Type": "application/json", "ProfileName": "Mateus", "From": 'whatsapp:85999171902',
               "WaId": "85985743958473"}
    messageFlow = ["Oii", "Vou querer uma pizza meia calabresa meia margherita e uma pizza de frango",
                   "Sim", "Vou querer dois sucos de laranja", "Pix"]

    @task
    def send_messages(self):
        for message in self.messageFlow:
            self.headers["body"] = message
            self.client.post("/twilioSandbox",
                             data=message,
                             headers=self.headers)


def __main():
    env = Environment(user_classes=[PizzaUser])
    runner = LocalRunner(env)
    env.create_local_runner()

    # Start the test
    runner.start(user_count=1, spawn_rate=1)

    # Wait for the specified time and then stop
    runner.greenlet.join(timeout=60)
    runner.stop()

    # No need to call quit on the runner as stop will ensure all users are stopped


if __name__ == "__main__":
    __main()
