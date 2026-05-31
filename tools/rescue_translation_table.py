import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "localization" / "ru_working.tsv"
OUTPUT = ROOT / "localization" / "ru_rescue.tsv"


MANUAL = {
    # Core gameplay/UI
    '"Okay"': '"Ладно"',
    "Drop/Throw": "Бросить/метнуть",
    "Journal": "Журнал",
    "Interact": "Взаимодействовать",
    "Honor : ": "Честь: ",
    "Night : ": "Ночь: ",
    "Night": "Ночь",
    "Night ": "Ночь ",
    "Quest Journal": "Журнал заданий",
    "Quest Completed!": "Задание выполнено!",
    "Quest Tasks": "Цели задания",
    "Page 1/1": "Стр. 1/1",
    "Page {current} / {total}": "Стр. {current} / {total}",
    "You Died": "Ты погиб",
    "You Have Died": "Ты погиб",
    "Lost To The Night": "Поглощен ночью",
    "You Have Perished": "Ты сгинул",
    "Death Has Come": "Смерть пришла",
    "Quests Completed": "Заданий выполнено",
    "Knight Deaths": "Смертей рыцарей",
    "Knights Deaths": "Смертей рыцарей",
    "Nights Survived": "Ночей пережито",
    "Game Over": "Игра окончена",
    "cost!": "цена!",
    "1000 Honor": "1000 чести",
    "100 Honor": "100 чести",
    "725 Honor": "725 чести",
    "Total Fail Cost": "Общая цена провала",
    "Remaining If Failed": "Останется при провале",
    "Current": "Сейчас",
    "Sleeping now will skip to the next day": "Сон сейчас перенесет к следующему дню",
    "Cost of Missing Players": "Цена отсутствующих рыцарей",
    "Cost to Skip Unfinished Quests": "Цена пропуска незавершенных заданий",
    "No! I Must Persevere!": "Нет! Я должен выстоять!",
    "Yes, Take the Penalty": "Да, принять кару",
    "Resulting in ": "Итог: ",
    "Honor": "Честь",
    "Thank Yee for Playin!": "Спасибо за игру, рыцарь!",
    "Your Watch Is Over": "Твоя стража окончена",
    "Everyone has": "У всех есть",
    "Sleep in your bed to start a new day!": "Ляг в кровать, чтобы начать новый день!",
    "This is a hint!": "Это подсказка!",
    "You're a Dishonored Knight Ya Dingus!": "Ты обесчещенный рыцарь, болван!",
    "You have brought shame upon your King for the last time.": "Ты опозорил короля.",
    "By his decree, you are cast to the night shift. ": "Его указом тебя сослали на ночную стражу. ",
    "Do Everything to Reclaim your honor.": "Сделай все, чтобы вернуть честь.",
    "Do not perish to the night.": "Не сгинь во тьме.",
    "Summary": "Итог",
    "Honor Spent": "Чести потрачено",
    "Total Honor": "Всего чести",
    "Bonus Honor": "Бонус чести",
    "< player name >": "< имя игрока >",
    "You Earned": "Получено",
    "Quest Complete": "Задание выполнено",
    "Next Player": "Следующий игрок",
    "Finish Quest": "Завершить задание",
    "Use": "Использовать",
    "Swing": "Удар",
    "Next Page": "След. страница",
    "Lantern": "Фонарь",

    # Menus/lobby/settings
    "Face": "Лицо",
    "Shirt Color": "Цвет рубахи",
    "Helmet": "Шлем",
    "Pants Color": "Цвет штанов",
    "Hair Color": "Цвет волос",
    "Hair": "Волосы",
    "Prev": "Назад",
    "Next": "Дальше",
    "Honor:": "Честь:",
    "Night:": "Ночь:",
    "Customize Character": "Настроить рыцаря",
    "Invite Friends": "Позвать друзей",
    "Close Lobby": "Закрыть лобби",
    "Start Game": "Начать игру",
    "Player Name": "Имя игрока",
    "Kick": "Выгнать",
    "Players": "Игроки",
    "Created By:": "Создано:",
    "Attributions": "Благодарности",
    "BACK": "НАЗАД",
    "Back": "Назад",
    "Demo": "Демо",
    "Invite From": "Приглашение от",
    "Accept": "Принять",
    "Decline": "Отклонить",
    "link text here": "текст ссылки",
    "Wishlist On Steam": "В желаемое Steam",
    "Use Item": "Использовать предмет",
    "Sprint": "Бег",
    "Toggle Lantern": "Фонарь",
    "Crouch": "Красться",
    "Jump": "Прыжок",
    "Toggle VOIP": "Голос",
    "Right HotBar": "Правый слот",
    "Left HotBar": "Левый слот",
    "Controls": "Управление",
    "Drop ": "Бросить ",
    "[Hold To Throw]": "[удерживать, чтобы метнуть]",
    "HOST": "СОЗДАТЬ",
    "JOIN": "ВОЙТИ",
    "PHOTOSENSITIVITY WARNING": "ОСТОРОЖНО: ВСПЫШКИ",
    "A Game By ": "Игра от ",
    "You may encounter flashing lights or visuals while playing this game.": "В игре могут встречаться вспышки света и резкие визуальные эффекты.",
    "Server Name": "Имя сервера",
    "L.A.N": "Локальная сеть",
    "Join Game": "Войти в игру",
    "REFRESH": "ОБНОВИТЬ",
    "LOADING": "ЗАГРУЗКА",
    "\"Running isn't always the best option\nBut its a pretty good one\"": "\"Бег не всегда лучший выбор\nНо часто он спасает\"",
    "Friends Only": "Только друзья",
    "Permanently Delete Save?": "Удалить сохранение навсегда?",
    "Max Players": "Макс. игроков",
    "[ Saving is Disabled in Demo ]": "[ сохранение отключено в демо ]",
    "Load Game": "Загрузить игру",
    "SOLO": "СОЛО",
    "No, Go Back": "Нет, назад",
    "Delete": "Удалить",
    "Save 01": "Слот 01",
    "Save 02": "Слот 02",
    "Save 03": "Слот 03",
    "Load": "Загрузить",
    "Save 0": "Слот 0",
    "Yes, QUIT": "Да, выйти",
    "VOIP": "Голос",
    "Mic Gain": "Громкость микрофона",
    "Mic Gate": "Порог микрофона",
    "Device": "Устройство",
    "Game": "Игра",
    "Mic Input": "Вход микрофона",
    "Render Scale": "Масштаб рендера",
    "Framerate Limit": "Лимит кадров",
    "Resolution": "Разрешение",
    "V-Sync": "Верт. синхр.",
    "OFF": "ВЫКЛ",
    "Fullscreen": "Полный экран",
    "Camera Shake": "Тряска камеры",
    "Mouse Sensitivity": "Чувствительность мыши",
    "Music": "Музыка",
    "Brightness": "Яркость",
    "Quality": "Качество",
    "Sound": "Звук",
    "HIGH": "ВЫСОКО",
    "CUSTOM": "СВОЕ",
    "low": "низко",
    "MEDIUM": "СРЕДНЕ",

    # Interactables/items
    "OnlyClockwise": "Только по часовой",
    "OnlyCounterClockwise": "Только против часовой",
    "BothDirections": "В обе стороны",
    "OpenClockwise": "Открыто по часовой",
    "Closed": "Закрыто",
    "OpenCounterClockwise": "Открыто против часовой",
    "IT BURNS!": "ЖЖЕТ!",
    "Sleep (Save Game)": "Спать (сохранить игру)",
    "Bear Trap": "Медвежий капкан",
    "Just another ancle biter...": "Еще один кусачий капкан...",
    "Bone": "Кость",
    "Humorous": "Забавно",
    "Bottle": "Бутыль",
    "I really shouldn't": "Не стоит мне это...",
    "Bread": "Хлеб",
    "Stale as a Rock": "Черствый, как камень",
    "Cabbage": "Капуста",
    "Raw and tasteless, unless steamed or in a stew": "Сырая и безвкусная, разве что сварить в похлебке",
    "Chicken": "Курица",
    "I Must": "Надо",
    "Crystal": "Кристалл",
    "The Power": "Сила",
    "Gold Cup": "Золотая чаша",
    "How did you find me?": "Как ты меня нашел?",
    "Dough": "Тесто",
    "Egg": "Яйцо",
    "What came first": "Что было первым",
    "Fang": "Клык",
    "Tooth": "Зуб",
    "Fish": "Рыба",
    "It stank...": "Воняет...",
    "FishingPole": "Удочка",
    "I can hardly swing it...": "Я едва могу этим махать...",
    "FLESH": "ПЛОТЬ",
    "I hear something": "Я что-то слышу",
    "Gemerald": "Самоцвет",
    "Its so lovely": "Какой милый",
    "Hammer": "Молот",
    "WOW! ITS A FUCKING HAMMER!": "ОГО! ЭТО ЧЕРТОВ МОЛОТ!",
    "Hand Axe": "Ручной топор",
    "Used to chop things in twain": "Годится рубить надвое",
    "Scratchy": "Колючее",
    "A nice chunk of log, freshly chopped": "Добрый кусок свежего бревна",
    "Mace": "Булава",
    "WOW! ITS A FUCKING MACE!": "ОГО! ЭТО ЧЕРТОВА БУЛАВА!",
    "Flame on": "Пламя, явись",
    "MeatLeg": "Окорок",
    "Mug": "Кружка",
    "Mushroom": "Гриб",
    "Mushy": "Склизкий",
    "Pick Axe": "Кирка",
    "WOW! ITS A FUCKING PICKAXE!": "ОГО! ЭТО ЧЕРТОВА КИРКА!",
    "Rat Tail": "Крысиный хвост",
    "Um okay": "Эм... ладно",
    "Skull": "Череп",
    "Who do I belong to?": "Кому я принадлежу?",
    "Sword": "Меч",
    "Green": "Зеленый",
    "Blue": "Синий",
    "Red": "Красный",

    # Early quest/dialogue strings seen during testing.
    "What Are Those Rocks?": "Что это за камни?",
    "Find out how to make the stange Glowing Flesh go away out front of the Gates": "Узнай, как убрать странную светящуюся плоть перед воротами",
    "Get the rooooocks": "Добудь кааамни",
    "Return to the Gates": "Вернись к воротам",
    "Speak to Villager at the Castle Gates": "Поговори с жителем у замковых ворот",
    "Talk to Villager at the Castle Gates": "Поговори с жителем у замковых ворот",
    "Rid That Growth": "Избавься от нароста",
    "Click and Hold Interact on the Red Growth outside the Castle Walls": "Зажми взаимодействие на красном наросте за стенами замка",
    "Get the mushrooooom": "Добудь гриииб",
    "Return to the Castle Gates": "Вернись к замковым воротам",
    "Fetch Me Sword": "Принеси мой меч",
    "Fetch the Sword from somewhere inside the Barn on the Farm.": "Найди меч где-то в амбаре на ферме.",
    "Fetch test sword": "Найди меч",
    "Return the Sword to the Gates": "Верни меч к воротам",
    "Fetch the Sword from somewhere in the Village Inn.": "Найди меч где-то в деревенской таверне.",
    "Fetch sword": "Найди меч",
    "Fetch the Sword that's by the Forest Pond.": "Найди меч у лесного пруда.",
    "Fetch Me Cup": "Принеси мою чашу",
    "Grab the Gold Cup in the Village Tavern": "Забери золотую чашу в деревенской таверне",
    "Grab the gold cup in the village tavern": "Забери золотую чашу в деревенской таверне",
    "Return the Gold Cup to the Gates": "Верни золотую чашу к воротам",
    "Find the Fang in the Forest Ruins near the Abandoned Village": "Найди клык в лесных руинах у покинутой деревни",
    "Light the Beacon deep in the Forest near the Outer Gates": "Зажги маяк в глубине леса у внешних ворот",
    "Light the BEACON deep in the FOREST near the OUTER GATES": "Зажги МАЯК в глубине ЛЕСА у ВНЕШНИХ ВОРОТ",
    "Light the Beacon deep in the Forest at the Forest Ruins": "Зажги маяк в глубине леса, у лесных руин",
    "Fetch a piece of Meat from the Village Butcher": "Принеси кусок мяса из деревенской бойни",
    "Compendium": "Бестиарий",
}


LONG_MANUAL = {
    "*Many knights have begun compiling their knowledge within these pages, a growing record meant to aid any who dare endure the night.*\n\nFollowers\n\nA hooded figure has been sulking around outside the gates at night. While they are easy to startle and run away, they have a proclivity to stab any who get too close. They seem to love stabbing in the back.\nMany Knights claim they are easy to slay while other Knights claim it to be difficult. \nKeep an ear out for heavy breathing in the shadows. . . You may be getting followed.\nChasing them seems to only anger them further. Best keep your distance if poorly armed.\n":
        "*Многие рыцари начали собирать свое знание на этих страницах: растущая летопись для всякого, кто осмелится пережить ночь.*\n\nПоследователи\n\nФигура в капюшоне по ночам шатается у ворот. Ее легко вспугнуть, и она часто обращается в бегство, но всякого, кто подойдет слишком близко, она охотно ударит ножом. Кажется, больше всего ей по нраву бить в спину.\nОдни рыцари уверяют, что таких тварей легко зарубить; другие клянутся, что это нелегкое дело.\nПрислушивайся к тяжелому дыханию в тенях... возможно, за тобой уже идут.\nПогоня лишь распаляет их сильнее. Если вооружен худо, держись на расстоянии.\n",
    "Meatman\n\nMany Knights have grown accustomed to calling it the Meatman. A many legged crawling abomination.\nThis creature will try and grab and steal any Knight unfortunate enough to cross its path. Pulling them away from any other brothers. It does not ask for consent.\nSome Knights have claimed that hitting this monster while carrying someone will force it to drop said person. If you get grabbed it will drop your lantern making your path back to safety even more treacherous.\nIts appearance is unsightly, but some Knights have claimed it can be slain . . . ":
        "Мясник\n\nМногие рыцари привыкли звать его Мясником. Ползучая многоногая мерзость.\nЭта тварь хватает и утаскивает всякого рыцаря, которому не повезло оказаться на ее пути, отрывая его от братьев по страже. Согласия она не спрашивает.\nРыцари утверждают: если ударить чудовище, пока оно несет добычу, оно отпустит несчастного. Если схватит тебя, фонарь выпадет, и путь назад к свету станет еще опаснее.\nВид его мерзок, но некоторые рыцари клянутся, что его можно убить...",
    "Hollowman \n\nThis creature is taller than most . . . A tall split man.\nA swift and fearsome foe, many knights run in fear, but the rustling alerts the beast. \nSome have written about this beast in notes found on the farm.\nKnights have claimed to have slain it, but at great cost . . .\nSome Knights claim it is blind, but can hear all the better.\nIf you hear it's moaning you must stay silent . . .":
        "Полый\n\nЭта тварь выше большинства... высокий рассеченный человек.\nБыстрый и страшный враг: многие рыцари бегут от него, но шорох только выдает их зверю.\nО нем писали в записках, найденных на ферме.\nРыцари клялись, что убивали его, но страшной ценой...\nОдни говорят, что он слеп, зато слышит куда лучше.\nЕсли услышишь его стон, замри и молчи...",
    "I. Gain honor by completeing quests each day\n\nII. Use honor to buy items from merchant\n\nIII. Each death loses 100 honor\n\nIV. If Knights are left outside the gates when sleeping, thy are presumed DEAD and will loose 100 honor\n\nV. If you reach zero honor and fail the quest you will fail\n\nVI. If all deaths result in zero honor you will fail\n":
        "I. Получай честь, выполняя задания каждый день\n\nII. Трать честь у торговца на припасы\n\nIII. Каждая смерть отнимает 100 чести\n\nIV. Если рыцари останутся за воротами во время сна, их сочтут МЕРТВЫМИ, и стража потеряет 100 чести\n\nV. Если честь упадет до нуля и задание будет провалено, стража падет\n\nVI. Если все смерти сведут честь к нулю, стража падет\n",
    "I’ve gone and lost me blessed amulet somewhere in the heart of the forest. It’s been a charm of fortune to me all these years, and I fear what may come without it. Would ye be so kind as to seek it out for me? I dare not tread those woods meself—too many eyes in the dark, watchin’ from the trees, and I’m no fool to tempt fate alone.":
        "Потерял я свой благословенный амулет где-то в сердце леса. Все эти годы он хранил мою удачу, и без него мне неспокойно. Будь добр, сыщи его для меня. Сам я в те чащи не сунусь: слишком много глаз во тьме, слишком много взглядов с деревьев, а я не дурак один искушать судьбу.",
    "Aye . . . wait who be you? A new Knight, gods help us . . .        \nTHREE PILLARS of FLESH have broke up from outside the GATES!             \nNow yee gotta go figure out howda get rid of em! They just popped back up when I tried pokin em with a stick, its creeping all us out . . .                                                                                                \nHurry up now! They must be up to no good. I can feel it . . .":
        "Эй... постой, ты кто таков? Новый рыцарь? Боги, сжальтесь над нами... У ВОРОТ поднялись ТРИ СТОЛБА ПЛОТИ! Теперь тебе разбираться, как от них избавиться. Я ткнул один палкой, а он снова вылез. Всех от этого воротит... Шевелись. Добра от них не жди, нутром чую.",
    "Oi, look at thee new, untested, and scrawny. Yee must pass me test . . .            \nThere’s another BIG FLESHY GROWTH near these CASTLE WALLS.       \nIt's got TENTACLES and GLOWIN' RED! Hurry before it makes more . . .                              \nTo remove it you go touch an hold it for a second or two . . .                                                         \nBut don’t you dare come close to me till you’ve washed yourself clean!":
        "Гляньте-ка: новенький, непроверенный и тощий. Пройдешь мое испытание... У ЗАМКОВЫХ СТЕН вырос еще один БОЛЬШОЙ МЯСНОЙ НАРОСТ. С щупальцами, красным светится! Торопись, пока он не расплодился. Чтобы убрать его, подойди и удерживай руку пару секунд... Но ко мне не приближайся, пока не отмоешься!",
}


def corrupt_translation(text: str) -> bool:
    if not text:
        return False
    question_marks = text.count("?")
    alpha = sum(ch.isalpha() for ch in text)
    cyrillic = sum("А" <= ch <= "я" or ch == "ё" or ch == "Ё" for ch in text)
    return question_marks >= 3 and cyrillic == 0


def main() -> None:
    with INPUT.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)
        fields = reader.fieldnames or []

    fixed = 0
    blanked = 0
    filled = 0
    for row in rows:
        source = row.get("source", "")
        translation = row.get("translation", "")
        replacement = LONG_MANUAL.get(source) or MANUAL.get(source)

        if replacement:
            if translation != replacement:
                row["translation"] = replacement
                filled += 1
            continue

        if corrupt_translation(translation):
            row["translation"] = ""
            blanked += 1
            continue

        if translation:
            fixed += 1

    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {OUTPUT}")
    print(f"kept_valid={fixed} manual_filled={filled} blanked_corrupt={blanked}")


if __name__ == "__main__":
    main()
