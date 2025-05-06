import emoji

def meus_emojis(categoria):
    emojis = {
        'Smile': '😀😄😁😆😅🤣😂🙂🙃🫠😉😊😇🥰😍🤩😘😗😚😙🥲😋😛🤪😝🤑🤗🤭🫢🫣🤫🤔🫡🤐🤨😐😑😶‍️😏😒🙄😬🤥😌😔😪🤤😴😷🤒🤕🤢🤮🤧🥵🥶🥴😵🤯🤠🥳🥸😎🤓🧐😕🫤😟🙁😮😯😲😳🥺🥹😦😧😨😰😥😢😭😱😖😣😞😓😩😫🥱😤😡😠🤬😈👿💀💩🤡',
        'Corpo': '🤚🖐️✋🖖🫱🫲🫳🫴👌🤌🤏🤞🫰🤟🤘🤙👈👉👆🖕👇🫵👍👎✊👊🤛🤜👏🙌🫶👐🤲🤝🙏💅🤳💪',
        'Animais': '🐵🐒🦍🦧🐶🐕🦮🐕‍🦺🐩🐺🦊🦝🐱🐈🐈‍🦁🐯🐅🐆🐴🐎🦄🦓🦌🦦🦧🦘🐮🐂🐃🐄🐷🐖🐗🐽🐏🐑🐐🐪🐫🦙🦒🐘🦣🦏🦛🐭🐁🐀🐹🐰🐇🐿️🦫🦔🦇🐻🐨🐼🦥🦦🦨🦘🦡🐾🦃🐔🐓🐣🐤🐥🐦🐧🦅🦆🦢🦉🦤🪶🦩🦚🦜🐸🐊🐢🦎🐍🐲🐉🦕🦖🐳🐋🐬🦭🐟🐠🐡🦈🐙🐚🪸🐌',
        'Comida': '🍇🍈🍉🍊🍋🍌🍍🥭🍎🍏🍐🍑🍒🍓🫐🥝🍅🫒🥥🥑🍆🥔🥕🌽🌶️🫑🥒🥬🥦🧄🧅🍄🥜🫘🌰🍞🥐🥖🫓🥨🥯🥞🧇🧀🍖🍗🥩🥓🍔🍟🍕🌭🥪🥗🍿🧈🧂🥫🍱🍘🍙🍚🍛🦀🦞🦐🦑🦪🍦🍧🍨🍩🍪🎂🍰🧁🥧🍫🍬🍭🍮🍯🍼🥛☕🫖🍵🍶🍾🍷🍸🍹🍺🍻🥂🔪',
    }
    return emoji.demojize(emojis.get(categoria, ''))

if __name__ == '__main__':
    print(emoji.emojize(meus_emojis('Smile')), '\n')
    print(emoji.emojize(meus_emojis('Corpo')), '\n')
    print(emoji.emojize(meus_emojis('Animais')), '\n')
    print(emoji.emojize(meus_emojis('Comida')), '\n')
    print(emoji.emojize(meus_emojis('Pessoas')), '\n')
