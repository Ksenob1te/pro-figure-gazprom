from fastapi_controllers import Controller, get, post


class AuthController(Controller):
    prefix = "/auth"
    tags = ["auth"]

    @get("")
    async def get_user_info(self):
        pass

    @post("/login")
    async def login(self):
        pass

    @post("/logout")
    async def logout(self):
        pass

    @post("/registration")
    async def registration(self):
        pass