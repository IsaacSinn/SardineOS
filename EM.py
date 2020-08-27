from Module_Base_Async import Module
from Module_Base_Async import AsyncModuleManager
from pubsub import pub
import asyncio
'''
EMLRcommand = {
                "EM_L": 0x30,
                "EM_R": 0x31,

}'''

class EM(Module):
    def __init__(self, name, address):
        super().__init__()
        self.name = name
        self.address = address
        exec(f'pub.subscribe(self.Listener, "gamepad.{self.name}")')

    def run(self):
        pass

    def Listener(self, message):
        if message["EM_L"]:
            pub.sendMessage("can.send", message = {"address": self.address, "data": [0x30, 0x10]})
        else:
            pub.sendMessage("can.send", message = {"address": self.address, "data": [0x30, 0x00]})

        if message["EM_R"]:
            pub.sendMessage("can.send", message = {"address": self.address, "data": [0x31, 0x10]})
        else:
            pub.sendMessage("can.send", message = {"address": self.address, "data": [0x31, 0x00]})


class __Test_Case_Send__(Module):
    def __init__(self):
        super().__init__()
        pub.subscribe(self.Listener, "can.send")

    def run(self):
        pub.sendMessage("gamepad.EM2", message = {"EM_L": 0, "EM_R": 1})

    def Listener(self, message):
        print(message)

if __name__ == "__main__":

    EM1 = EM("EM1", 0x31)
    EM2 = EM("EM2", 0x32)
    EM1.start(1)
    EM2.start(1)
    __Test_Case_Send__ = __Test_Case_Send__()
    __Test_Case_Send__.start(1)
    AsyncModuleManager = AsyncModuleManager()
    AsyncModuleManager.register_modules(EM1, EM2, __Test_Case_Send__)

    try:
        AsyncModuleManager.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        #print("Closing Loop")
        AsyncModuleManager.stop_all()