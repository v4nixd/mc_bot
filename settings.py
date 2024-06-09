import json

settings_json = open('settings.json')
settings = json.load(settings_json)

guild_id = settings['guild_id']
readonly_id = settings['readonly_id']
clown_id = settings['clown_id']
concussion_id = settings['concussion_id']
archive_id = settings['archive_id']
achievements_id = settings['achievements_id']
bot_use_id = settings['bot_use_id']