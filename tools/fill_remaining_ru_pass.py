#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "localization" / "ru_rescue_with_signs.tsv"
MAP = ROOT / "localization" / "map_texts.tsv"


NOTE_TRANSLATIONS = {
    "86c5282f9db9": "Страница из рыцарского журнала",
    "bcd46fb28a14": "Тот высокий... Боги, смотреть на него тошно. Весь согнутый, будто висит на нитях. Я думал, мне конец: споткнулся о ящики, поднял грохот. Но он не дрогнул. Может, не слышит. Если переживу ночь, назову его Висельцем.",
    "cf8649703a8b": "Страница из рыцарского журнала",
    "f8f2fd70c3bc": "Сумерки пали на деревню, как крыло ворона. Я собирал кружки у таверны, когда снаружи раздались торопливые шаги. Открыл дверь и увидел тварь: будто человек, но скрюченный, ползущий на многих ногах. Она схватила меня и понесла во тьму. Рыцарь ударил ее клинком, и она выпустила меня. Хвала его храбрости.",
    "733d37c498bf": "Неизвестная рука",
    "04d66d781794": "Не хочу сегодня и пальцем шевелить. Пусть рыцари доделают. Я пытался, но видел мерзость: человек, рассеченный пополам, а посреди - пасть. Он приходит на шум: ящики, инструменты, кружки. Я всегда молчу, когда он рядом. Один раз кинул кружку, чтобы сбежать. Королю не скажу: решат, что я спятил.",
    "522a5fc49ff3": "Статуи все еще плачут. Думал, крыша течет, но теперь вижу их лица, когда рядом нет души. Отец говорит все тише, будто боится разбудить что-то. Один оруженосец клялся, что статуя чуть сдвинулась, словно вдохнула. Потом ушел в лес и твердил, что слышит их шепот.",
    "1e033cd2ded9": "Страница из рыцарского журнала",
    "082cd11f4d81": "Прошлой ночью я вышел и почувствовал, как воздух стал тяжелым. Будто за мной следят. Потом увидел его: человек в странной одежде, не из наших мест. Он бросился с малым ножом, но испугался и исчез. Я погнался, желая понять, что им движет.",
    "bb30f03cbef6": "Но скажу честно: долго бы я там не задержался. Гнаться за тенями и шепотом - дело дурное. Не узнаю, кто он был: безумец или что похуже. Лучше забыть, пока беда не проснулась.",
    "91f6993233e8": "Страница из рыцарского журнала",
    "aa368c9e9637": "Сколько бы нас ни было, отчаяние давит со всех сторон. Ночь точит рассудок братьев. Нас гонят на грязные задания, а твари пожирают тех, кто слабее. Некоторых ужас свел с ума, иных он просто разорвал. Честь, похоже, уже не вернуть.",
    "b259de6fc312": "Дорогой рыцарь",
    "55b13f08fd11": "Прости, милорд, за такую просьбу. Иного пути нет. Я оставлю гниль здесь еще на время, чтобы понять, откуда она берется. Если будет воля, скажи королю о моих находках. Он должен знать, как остановить эту чуму.",
    "a9f293dfa9ec": "II\n\nВ ночной дозор теперь шлют все больше рыцарей. Я уже не помню лиц: мальчишки, едва выросшие, руки как ветки, глаза полны страха. Раньше так не было. Теперь достаточно малого позора, чтобы оказаться здесь. Завтра пойду к ферме.",
    "574e39023312": "III\n\nПо землям ходит мерзкий слух: один из самых почтенных рыцарей, почти любимец короля, был опозорен. Его тоже, должно быть, отправили в дозор. Говорят, он часто бывал у деревенского аптекаря. Больше писать нельзя. Завтра к деревенским шахтам.",
    "e475889ad9f7": "IV\n\nПишу как человек, недостойный прежнего звания. Честь сняли с меня, как меч с пояса. Король сказал: \"Позор не заслуживает защиты\". Теперь мы покупаем то, что нам должны были дать. Я чую отчаяние короля даже отсюда. Завтра поднимусь к башне над деревней.",
    "14c894330491": "... У тебя чувство, что в комнате тебя что-то ждет ...",
    "ad4b502f2972": "Задания становятся все грязнее. Крестьяне уже смеют грозить, что пожалуются королю. Они не понимают, зачем нас держат здесь. Король сделал честь монетой, а нас - ночными псами. Зеленая жижа одна дает покой. Дальше - лесной пруд. Боги, помогите.",
    "8d5031c71df9": "Дражайший брат, замок мрачнеет. Рыцари уходят к стенам и не возвращаются. Новобранцев мало, а потери быстры. В отчаянии они делают рыцарей даже из крестьян. Хоть тебя поставили возле нашей старой деревни. Посмотри на руины за нас обоих.",
    "286e3ee06d06": "VII\n\nСлужба близится к концу. Честь почти возвращена: говорят, меня пустят за стены, и я предстану перед королем. Тогда, может, искуплю грехи. Хочу лишь увидеть старую деревню во всей красе... до гнили. Но не подойду. Уже почти дома.",
    "f2bb49954d10": "VIII\n\nОни лгали. Король никогда не пустит нас обратно. Сказали: \"зараза\". Будто мы принесем ее с собой. Я кровоточил, мерз и голодал ради них, а теперь должен гнить снаружи, как пес. Нет. Я уйду за лес, дальше плоти. Там должно быть место.",
    "4bcc5843ea4d": "IX\n\nЕсли ты читал прошлые записи, то понял: позор, исчезновения и гниль не случайны. Не проклятие. Не бог. Это воля. Его воля. Плоть питается кругом, дозор кормит плоть, король хранит круг. Молчи об этом. Даже братьям-рыцарям.",
    "bd1a894dd459": "Как ты сюда забрался???",
    "8af7582a7c34": "Основы аптекаря",
    "3784e69ad43a": "С некоторыми частями плоти можно говорить. В них есть разум, и они способны отвечать. Они редки и будто отделены от прочей гнили.",
    "80f3bffc9e32": "ЗАКРЫТО НАВСЕГДА",
    "ca0efedb5f96": "Стражников все режут и режут...",
    "bb9069234467": "Ты находишь запись в журнале...",
    "39ec18245019": "Товары приходят все реже, и не все прибывает прежним. Телеги везут муку, мясо, дерево, а возвращаются полупустыми, с чем-то мягким в мешках. Дороги зарастают плотью, деревни пустеют, поля будто дышат. Королевство еще держится, но плоть растет вокруг него.",
    "1d36c86bf216": "Записки аптекаря",
    "2ea868083622": "Гниль не слушает ни слов, ни молитв. Это не зверь и не человек: она просто растет. Я заметил: кровь замедляет ее. Плоть за плоть, быть может. Крестьян здесь больше всего, и лорды делают из них рыцарей - не истинных, а бесчестных людей в стали, чтобы купить нам время. Я больше не стану вмешиваться.",
    "c6f074fdf85d": "Краткая история ничего, ч. 1",
    "5aeec376108b": "В начале росли королевства, стены и честь. Потом пришла гниль: живая язва земли. Кто-то звал ее ведьмовством, кто-то карой богов. Великая война жгла страны, а после каждое королевство заперлось в себе. Летописи сгорели, память стерлась. Мы знаем лишь изоляцию и плоть за стенами.",
    "835d03f232e7": "Краткая история ничего, ч. 2",
    "a05054c2a7ea": "Чума расползлась по земле и дала новую жизнь: светящиеся грибы, синих светляков, деревья выше прежних. Но почти все, что рождено гнилью, враждебно. Реки пульсируют, звери искривлены, деревни стали пустыми оболочками. Порой люди видят глаза в почве. Страх это или воля гнили - никто не знает.",
    "334bb87bdecc": "Проверю, сколько жижи выдержу этой ночью. Побью свой рекорд в пять, даже если голова расколется...",
    "ac7bd6fdc951": "Тебе придется прятаться",
    "34be80a6697d": "Одни твари слышат, другие видят, третьи знают тебя слишком глубоко. Выясни, что действует на каждую.",
    "8ac657c2faba": "Советы новым рыцарям...\n\nТвари могут слышать. Твари могут видеть. Некоторые умеют лишь одно. Они слышат бег и видят свет фонаря.\n\nБудь бдителен.\n\nБрошенные после смерти вещи остаются в мире несколько дней.\n\nЕсли умрешь, тебя заменит новый рыцарь.",
    "e9a04e9f4807": "Советы новым рыцарям",
    "2cc200feb6f4": "Твари могут слышать. Твари могут видеть. Некоторые умеют лишь одно. Они слышат бег и видят свет фонаря.\n\nБудь бдителен.\n\nВещи после смерти остаются на земле несколько дней.\n\nЕсли умрешь, тебя заменит новый рыцарь.\n\nБег тревожит тех, кто слышит. Фонарь виден тем, у кого есть глаза.",
    "68a910b9b8e2": "Красные шляпки неправильные. Думаю, они говорят друг с другом не словами, а знаками и шевелением. С тех пор как их стало больше, путь к моей рыбацкой яме будто стал короче, словно сама земля услужливо гнется под ногами.",
}


def load_rows(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.reader(f, delimiter="\t"))


def save_rows(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, delimiter="\t", lineterminator="\n").writerows(rows)


def main() -> None:
    rows = load_rows(TSV)
    changed = 0

    for row in rows:
        if len(row) >= 8 and row[0] in NOTE_TRANSLATIONS:
            if row[7] != NOTE_TRANSLATIONS[row[0]]:
                row[7] = NOTE_TRANSLATIONS[row[0]]
                changed += 1

    # Short quest objectives are highly repetitive. Fill the common ones by
    # source text/pattern so the journal stops falling back to English.
    quest_exact = {
        "Fetch the Sword from the Blacksmiths in the Village": "Найди меч у деревенского кузнеца",
        "Return to the gate": "Вернись к воротам",
        "Return To gates": "Вернись к воротам",
        "Fetch Book from the Forest Pond": "Найди книгу у лесного пруда",
        "Fetch Book Forest Pond": "Найди книгу у лесного пруда",
        "Fetch the Book From Village Church": "Найди книгу в деревенской церкви",
        "Fetch Me Shield": "Принеси щит",
        "Fetch Shield from the Forest Ruins": "Найди щит в лесных руинах",
        "Fetch Shield Forest Ruins": "Найди щит в лесных руинах",
        "Return the Shield to the Gates": "Верни щит к воротам",
        "Fetch Me Precious": "Принеси драгоценность",
        "Fetch the Statue From Village Market": "Найди статуэтку на рынке",
        "Fetch the Statue from the Village Market": "Найди статуэтку на рынке",
        "Return the Statue to the Gates": "Верни статуэтку к воротам",
        "Return Statue To Gates": "Верни статуэтку к воротам",
        "Mine a Green Gem": "Добудь зеленый самоцвет",
        "Mine a Gem": "Добудь самоцвет",
        "Mine an Emerald Gem from a Green Crystal in a Forest Cave": "Добудь изумруд из зеленого кристалла в лесной пещере",
        "Mine an Sapphire Gem from a Blue Cyrstal in Caves near the Village": "Добудь сапфир из синего кристалла у деревни",
        "Return Emerald Gem to the Gates": "Верни изумруд к воротам",
        "Return Sapphire Gem to the Gates": "Верни сапфир к воротам",
        "Return Sapphire Gem to Gates": "Верни сапфир к воротам",
        "Fetch a chicken. Find them wandering around or at the Farm": "Поймай курицу. Ищи на ферме или рядом",
        "Fetch a Chicken. Find them wandering around or at the Farm": "Поймай курицу. Ищи на ферме или рядом",
        "Fishing for Me Bed": "Рыба для моей постели",
        "Catch a Fish from the Forest Pond": "Поймай рыбу в лесном пруду",
        "Feed yee Horses": "Накорми лошадей",
        "Feed the Hay to all the Horses in the Barn at the Farm": "Дай сено всем лошадям в фермерском сарае",
        "Feed the horses": "Накорми лошадей",
        "Light all the Village Beacons. You'll find one near the Pond, outside the Apothecary, and outside the Tavern": "Зажги все деревенские маяки: у пруда, аптеки и таверны",
        "Destroy All 3 Growths and Retrieve the Gold Cup": "Уничтожь 3 нароста и забери золотой кубок",
        "Fetch Gold Cup Market": "Найди золотой кубок на рынке",
        "Clear up Flesh Blobs.": "Очисти сгустки плоти",
        "Return Goldcup to Gates": "Верни золотой кубок к воротам",
        "Feth the Gold Cup from the Village Apothecary": "Найди золотой кубок в деревенской аптеке",
        "Fetch CUP APOTH": "Найди кубок в аптеке",
        "Return The Gold Cup To The Villager": "Верни золотой кубок жителю",
        "Feth the Gold Cup from the Village Inn": "Найди золотой кубок в деревенской таверне",
        "Fetch the Gold Cup In the Apothacy": "Найди золотой кубок в аптеке",
        "Return Gold Cup": "Верни золотой кубок",
        "Rid Flesh Pillars": "Искорени столпы плоти",
        "Find out how to make the stange Flesh go away at the Forest Pond": "Разберись с плотью у лесного пруда",
        "Find out how to make the stange Flesh go away at the Village Pond": "Разберись с плотью у деревенского пруда",
        "Return the Bucket to the Gates.": "Верни ведро к воротам",
        "I have a quest for you!": "У меня есть для тебя дело!",
        "What are Those?": "Что это за твари?",
        "Fetch Me Axe": "Принеси топор",
        "Find the Axe left behind in the Lumbermill": "Найди топор на лесопилке",
        "Return the Axe to the Gates": "Верни топор к воротам",
        "Fetch Me Skull": "Принеси череп",
        "Fetch the lost Skull from somewhere in the Graveyard": "Найди потерянный череп на кладбище",
        "Fetch the lost Skull from somewhere in the Village Apothecary": "Найди потерянный череп в деревенской аптеке",
        "Find the Skull": "Найди череп",
        "Return the Skull to the Gates": "Верни череп к воротам",
        "Return the SKULL the the Villager at the Castle": "Верни череп жителю у замка",
        "Finish Cauldron Apothecary": "Заверши смесь в аптеке",
        "Go to the Village Apothecary and Finsih the Mixture": "Иди в деревенскую аптеку и заверши смесь",
        "Return the Potion to the Gates": "Верни зелье к воротам",
        "Chop Logs": "Наруби бревна",
        "Chop all the Small Logs Inside the Lumbermill and Deposit them in the nearby Chest": "Наруби малые бревна на лесопилке и сложи в сундук",
        "Fill Fish Bucket": "Наполни ведро рыбой",
        "Catch Fish from the Forest Lake and Deposit them in the Bucket on the Bridge": "Поймай рыбу в лесном озере и сложи в ведро на мосту",
        "fill the bucket": "Наполни ведро",
        "Destroy the RED GROWTHS at the FOREST LAKE": "Уничтожь красные наросты у лесного озера",
        "Light Candles Church": "Зажги свечи в церкви",
        "Light all Six of the unlit Candles in the Village Church": "Зажги шесть погасших свечей в деревенской церкви",
        "Blow Out Candles Forest Ruins": "Погаси свечи в лесных руинах",
        "Blow Out All the Candles at the Forest Ruins": "Погаси все свечи в лесных руинах",
        "return gates": "Вернись к воротам",
        "Put Away Books Church": "Убери книги в церкви",
        "Pick Up Books and Deposit them into the Chest": "Собери книги и сложи их в сундук",
        "Mine Blood Gem Forest": "Добудь кровавый самоцвет в лесу",
        "Mine an Blood Gem from a Blood Cyrstal deep in the Forest past the Forest Ruins": "Добудь кровавый самоцвет за лесными руинами",
        "Return the Blood Gem to the Gates": "Верни кровавый самоцвет к воротам",
        "Break Death Totems": "Разбей тотемы смерти",
        "Destroy all Six Death Totems around the Forest Ruins": "Уничтожь шесть тотемов смерти у лесных руин",
        "Break Cultist Totems": "Разбей тотемы культистов",
        "Destroy all Five Death Totems around the Farm": "Уничтожь пять тотемов смерти у фермы",
        "Destroy all Four Death Totems around the Forest Pond": "Уничтожь четыре тотема смерти у лесного пруда",
        "Destroy all Five Death Totems around the Village": "Уничтожь пять тотемов смерти в деревне",
        "Fetch the Mace from the Blacksmiths in the Village": "Найди булаву у деревенского кузнеца",
        "Return the Mace to the Gates": "Верни булаву к воротам",
        "Fetch Meat Butcher": "Забери мясо у мясника",
        "Return the Meat to the Gates": "Верни мясо к воротам",
        "Catch Fish from the Village Pond and Deposit them in the Bucket on the Bridge": "Поймай рыбу в деревенском пруду и сложи в ведро на мосту",
        "Catch Fish from the Forest Pond and Deposit them in the Bucket on the Dock": "Поймай рыбу в лесном пруду и сложи в ведро у причала",
        "Fetch Carrot Farm": "Найди морковь на ферме",
        "Fetch the Carrot growing in Garden at the Farm": "Сорви морковь в фермерском огороде",
        "Return the Carrot the the Gates": "Верни морковь к воротам",
        "Fetch Cabbage Farm": "Найди капусту на ферме",
        "Fetch the Cabbage growing in Garden at the Farm": "Сорви капусту в фермерском огороде",
        "Return the Cabbage to the Gates": "Верни капусту к воротам",
        "Harvest Vegetables": "Собери овощи",
        "Deposit the Veggies into the Crates": "Сложи овощи в ящики",
    }
    for row in rows:
        if len(row) < 8 or row[7].strip() or "QuestSystem/DT_Quests" not in row[2]:
            continue
        source = row[6]
        lower = source.lower()
        translation = quest_exact.get(source)
        if translation is None and lower.startswith("click and hold interact on the red growth"):
            translation = "Удерживай взаимодействие на красном наросте"
        elif translation is None and lower.startswith("click and hold to light the beacon"):
            translation = "Удерживай взаимодействие, чтобы зажечь маяк"
        elif translation is None and lower.startswith("click and hold on the beacon"):
            translation = "Удерживай взаимодействие, чтобы зажечь маяк"
        elif translation is None and source in {"<QuestName>", "Description of the stage.", "ReturnStage", "Spawn Necessary Items"}:
            continue
        if translation is not None:
            row[7] = translation
            changed += 1

    # Keep this hint short enough for the small parchment widget.
    for row in rows:
        if len(row) >= 8 and row[6] == "Check your health and stamina in the top left corner":
            row[7] = "Здоровье и силы\nслева сверху."
            if len(row) >= 9:
                row[8] = "short hint translation"
            changed += 1

    # Add/refresh missing map hints.
    map_rows = load_rows(MAP)
    by_id = {row[0]: row for row in rows if row}
    map_hint_translations = {
        "Turn Back! Look back near the Castle Gates": "Назад!\nИщи у ворот.",
        "Check your health and stamina in the top left corner": "Здоровье и силы\nслева сверху.",
    }
    for source_row in map_rows:
        if len(source_row) < 7 or source_row[6] not in map_hint_translations:
            continue
        target = map_hint_translations[source_row[6]]
        if source_row[0] in by_id:
            row = by_id[source_row[0]]
            if row[7] != target:
                row[7] = target
                changed += 1
            if len(row) >= 9:
                row[8] = "short hint translation"
            else:
                row.append("short hint translation")
        else:
            new_row = source_row[:7] + [target, "short hint translation"]
            rows.append(new_row)
            by_id[source_row[0]] = new_row
            changed += 1

    save_rows(TSV, rows)
    print(f"changed {changed} rows {len(rows)}")


if __name__ == "__main__":
    main()
