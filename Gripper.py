from Module_Base_Async import Module
from Module_Base_Async import AsyncModuleManager
from pubsub import pub
import asyncio

class Gripper(Module):
    def __init__(self, address, speed):
        super().__init__()
        self.speed = speed
        self.address = address
        pub.subscribe(self.Listener, "gamepad.gripper")

    def run(self):
        pass

    def Listener(self, message):
        if message["extend"]:
            pub.sendMessage('can.send', message = {"address": eval(self.address), "data": [32, self.speed >> 8 & 0xff, self.speed & 0xff]})
        elif message["retract"]:
            pub.sendMessage('can.send', message = {"address": eval(self.address), "data": [32, -self.speed >> 8 & 0xff, -self.speed & 0xff]})
        else:
            pub.sendMessage('can.send', message = {"address": eval(self.address), "data": [32, 0x00, 0x00]})

class __Test_Case_Send__(Module):
    def __init__(self):
        super().__init__()
        pub.subscribe(self.Listener, "can.send")

    def run(self):
        pub.sendMessage("gamepad.gripper", message = {"extend": False, "retract": True})

    def Listener(self, message):
        print(message)

if __name__ == "__main__":

    Gripper = Gripper('0x21', 17000)
    Gripper.start(1)
    __Test_Case_Send__ = __Test_Case_Send__()
    __Test_Case_Send__.start(1)
    AsyncModuleManager = AsyncModuleManager()
    AsyncModuleManager.register_modules(Gripper, __Test_Case_Send__)

    try:
        AsyncModuleManager.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        print("Closing Loop")
        AsyncModuleManager.stop_all()
