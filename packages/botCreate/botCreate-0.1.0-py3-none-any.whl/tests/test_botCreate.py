import botCreate

def test_client():
    botCreate.create(
        name='bot_client',
        token='OTY4NjA3OTA2NjEyMjczMjQy.YmhUaA.WyAgnLY1RGF8tDjoEDokvtF7bIE',
        prefix='?',
        type=botCreate.CLIENT,
        launch=False
    )

def test_bot():
    botCreate.create(
        name='bot_bot',
        token='OTY4NjA3OTA2NjEyMjczMjQy.YmhUaA.WyAgnLY1RGF8tDjoEDokvtF7bIE',
        prefix='?',
        type=botCreate.BOT,
        launch=False
    )

def test_sharded_bot():
    botCreate.create(
        name='bot_sharded_bot',
        token='OTY4NjA3OTA2NjEyMjczMjQy.YmhUaA.WyAgnLY1RGF8tDjoEDokvtF7bIE',
        prefix='?',
        type=botCreate.SHARDED_BOT,
        launch=False
    )