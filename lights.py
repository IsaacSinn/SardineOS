from Module_Base import Module, Async_Task
from pubsub import pub
import asyncio

class Light(Module):
    def __init__(self, device, address):
        super().__init__()
        self.device = device
        self.address = address
        exec(f'pub.subscribe(self.Listener, "gamepad.{self.device}")')
        pub.subscribe(self.Listener, "can.send")

    @Async_Task.loop(1)
    async def run(self):
        pass

    def Listener(self, message):
        if message["Light"]:
            pub.sendMessage('can.send', message = {"address": eval(self.address), "data": [0x60, 0xFF, 0xFF, 0xFF]})
        elif not message["Light"]:
            pub.sendMessage('can.send', message = {"address": eval(self.address), "data": [0x61]})

        

class __Test_Case_Send__(Module):
    def __init__(self):
        super().__init__()
        pub.subscribe(self.Listener, "can.send")

    def run(self):
        pub.sendMessage("gamepad.Light", message = {"ON": False})

    def Listener(self, message):
        print(message)


if __name__ == "__main__":

    Light = Light('Light', '0x61')
    Light.start(1)
    __Test_Case_Send__ = __Test_Case_Send__()
    __Test_Case_Send__.start(1)
    AsyncModuleManager = AsyncModuleManager()
    AsyncModuleManager.register_modules(Light, __Test_Case_Send__)

    try:
        AsyncModuleManager.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        print("Closing Loop")
        AsyncModuleManager.stop_all()
