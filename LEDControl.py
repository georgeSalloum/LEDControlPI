from gpiozero import LED
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory



pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-b27bafae-b390-11e7-8f6d-3a18aff742a6"
pnconfig.publish_key = "pub-c-b5098184-8741-481d-918f-6e08c2116ce0"
pnconfig.ssl = False
pubnub = PubNub(pnconfig)

led = LED(4)
led.off()

def publish_callback(result,status):
    pass

def publish_status():
    if(led.value == 1):
        LED_STATUS = "ON"
    else:
        LED_STATUS = "OFF"
    pubnub.publish().channel('LED_STATUS_CHANNEL').message(LED_STATUS).async(publish_callback)
    
def received_callback(message, channel):
    print(message + " " + channel)
    
publish_status()

class MyListener(SubscribeCallback):
    def status(self, pubnub, status):
        print("status changed: %s" % status)

    def message(self, pubnub, message):
        next_led_status = message.message
        if(next_led_status == "ON"):
            led.on()
        else:
            led.off()
        publish_status()

    def presence(self, pubnub, presence):
        pass


my_listener = MyListener()


pubnub.add_listener(my_listener)

pubnub.subscribe().channels('LED_COMMAND_CHANNEL').execute()