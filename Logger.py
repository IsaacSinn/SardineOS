from pubsub import pub
from Module_Base_Async import Module
import yaml
import logging

AllTopics = {"Gamepad": 'gamepad',
             "ControlProfile": 'command',
             "Thruster_Power": 'Thruster',
             "Thruster": 'can',
             "CAN_Handler": 'log'
             }

class Logger(Module):
    def __init__(self, Print, Log, Topics):
        super().__init__()
        logging.basicConfig(filename='console.log', filemode='w', format='%(levelname)s - %(message)s')
        '''try:
            content = yaml.load(open('config.yaml', 'r'), Loader = yaml.FullLoader)
            for key,value in content.items():
                for key, value in value.items():
                    if key == 'varclass':
                        Topics.append(value)
        except FileNotFoundError:
            pass'''
        self.Print = Print
        self.Log = Log
        self.Topics = tuple(map(str, Topics.split(',')))
        #print(self.Topics)
        for topic in self.Topics:
            #print(topic)
            exec(f'pub.subscribe(self.message_listener, "{topic}")')

    def message_listener(self, message):
        if self.Print:
            print(message)
        if self.Log:

    def run(self):
        pass


if __name__ == "__main__":
    Logger = Logger(Print = True, Topics = "gamepad,command")

    pub.sendMessage("gamepad.sdfs", message = {"Ricky": "dehydrtion"})
