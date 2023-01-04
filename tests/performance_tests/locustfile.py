from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    @task
    def home(self):
        response = self.client.get("/")

    @task
    def boardpoints(self):
        response = self.client.get("/boardpoints")

    @task
    def show_summary(self):
        response = self.client.post("/show_summary",
                                    {"email": "john@simplylift.co"})

    @task
    def book(self):
        response = self.client.get("/book/Spring%20Festival/Simply%20Lift")

    @task
    def purchase_places(self):
        response = self.client.post("/purchase_places",
                                    {"club": "Simply Lift",
                                     "competition": "Spring Festival",
                                     "places": 1})
