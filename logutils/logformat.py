def formatLog(player, meta):
    log = player.get('title') + ' - ' + player.get('uuid') + ' : ' + meta.get('type') + ' : ' + meta.get(
        'parentTitle') + ' - ' + meta.get('title')
    return log
