import asyncio
import threading
import cv2
import discord
import mediapipe as mp

bot = discord.Client(intents=discord.Intents.all())
prev_string = None
count = 0
wait_msec = 0
need_to_change_avatar = True
emoji = None


async def gesture_recognition():
    global prev_string, count, wait_msec, need_to_change_avatar, emoji

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    # Захват видео с камеры
    cap = cv2.VideoCapture(camera_index)

    with mp_hands.Hands(min_detection_confidence=0.9, min_tracking_confidence=0.9) as hands:
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                print("Ignoring empty camera frame.")
                continue

            if wait_msec <= 0:
                if need_to_change_avatar:
                    # loop = asyncio.get_event_loop()
                    # loop.run_until_complete()
                    try:
                        await bot.user.edit(avatar=None)
                        need_to_change_avatar = False
                        print("avatar_cleared")
                    except discord.errors.HTTPException:
                        print("ошибочка 1")

                # Перевод изображения в формат RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)

                # Возвращение изображения в формат BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.multi_hand_landmarks:
                    emoji = get_emoji(results, image, mp_drawing, mp_hands)
                else:
                    emoji = None

                if emoji is not None:
                    print(emoji)
                    if emoji == prev_string:
                        count += 1
                    else:
                        prev_string = emoji
                        count = 1

                    if count == 3:
                        count = 0
                        wait_msec = 4000
                        need_to_change_avatar = True
                        try:
                            with open(emoji_dict[emoji], 'rb') as f:
                                await bot.user.edit(avatar=f.read())
                                print("avatar_changed")
                            channel = bot.get_channel(VOICE_CHANNEL_ID)
                            await channel.send(f'Пользователь отреагировал: {emoji}')
                            print("message")
                        except discord.errors.HTTPException as ex:
                            need_to_change_avatar = False
                            print(f"ошибочка {ex.text}")
                    wait_msec = wait_msec + 1000
                else:
                    count = 0
            else:
                wait_msec = wait_msec - 100

            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(100) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()


async def on_shutdown():
    print('Завершение программы...')
    await bot.close()


async def join_voice_channel(channel):
    try:
        voice_client = await channel.connect()
        print(f'Бот присоединился к голосовому каналу {channel.name}')
        return voice_client
    except Exception as e:
        print(f'Ошибка при подключении к голосовому каналу: {e}')


@bot.event
async def on_ready():
    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
    await join_voice_channel(voice_channel)
    await gesture_recognition()
    await on_shutdown()


class Bot:
    global emoji_dict

    emoji_dict = {
        '👍': 'images/thumbs_up.png',
        '👎': 'images/thumbs_down.png',
        '✌️': 'images/victory_hand.png',
        '👌': 'images/ok_hand.png',
        '✋': 'images/raised_hand.png'
    }

    def run_bot(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.create_task(bot.start(self.TOKEN))
            loop.run_forever()
        finally:
            loop.close()

    def __init__(self, T, V, i):
        global VOICE_CHANNEL_ID
        global camera_index
        self.TOKEN = T
        VOICE_CHANNEL_ID = int(V)
        camera_index = i

    def start(self):
        while True:
            bot_thread = threading.Thread(target=self.run_bot)
            bot_thread.start()
            bot_thread.join()
            print("ЦИКЛ")


def get_emoji(results, image, mp_drawing, mp_hands):
    for hand_landmarks in results.multi_hand_landmarks:
        landmarks = hand_landmarks.landmark

        # Жест "окей" (👌)
        okay_sign = (
                landmarks[8].x - 0.1 < landmarks[4].x < landmarks[8].x + 0.1 and
                landmarks[8].y - 0.1 < landmarks[4].y < landmarks[8].y + 0.1 and
                (landmarks[8].y - landmarks[12].y) ** 2 + (landmarks[8].x - landmarks[12].x) ** 2 > 0.02 and
                (landmarks[8].y - landmarks[16].y) ** 2 + (landmarks[8].x - landmarks[16].x) ** 2 > 0.02 and
                (landmarks[8].y - landmarks[20].y) ** 2 + (landmarks[8].x - landmarks[20].x) ** 2 > 0.02
        )

        # Жест "открытая ладонь" (✋)
        open_palm = (
                landmarks[4].y < landmarks[3].y and landmarks[8].y < landmarks[6].y and
                landmarks[12].y < landmarks[10].y and landmarks[16].y < landmarks[14].y and
                landmarks[20].y < landmarks[18].y and
                (landmarks[0].y - landmarks[12].y) ** 2 > 0.16
        )

        # Жест "V" (✌️)
        v_sign = (
                landmarks[8].y < landmarks[6].y and
                landmarks[12].y < landmarks[10].y and
                (landmarks[4].y - landmarks[16].y) ** 2 + (landmarks[4].x - landmarks[16].x) ** 2 < 0.09 and
                (landmarks[4].y - landmarks[20].y) ** 2 + (landmarks[4].x - landmarks[20].x) ** 2 < 0.09 and
                (landmarks[16].y - landmarks[20].y) ** 2 + (landmarks[16].x - landmarks[20].x) ** 2 < 0.02 and
                (landmarks[8].y - landmarks[12].y) ** 2 + (landmarks[8].x - landmarks[12].x) ** 2 > 0.01
        )

        # Жест "палец вверх"
        finger_up = (
                landmarks[4].y < landmarks[3].y and landmarks[4].y < landmarks[2].y and landmarks[4].y <
                landmarks[1].y and landmarks[4].y < landmarks[8].y and landmarks[4].y < landmarks[12].y
                and landmarks[4].y < landmarks[16].y and landmarks[4].y < landmarks[20].y and
                (landmarks[4].y - landmarks[8].y) ** 2 + (landmarks[4].x - landmarks[8].x) ** 2 > 0.04 and
                (landmarks[0].x - landmarks[4].x) ** 2 < 0.09 and
                (landmarks[8].y - landmarks[12].y) ** 2 + (landmarks[8].x - landmarks[12].x) ** 2 < 0.04 and
                (landmarks[16].y - landmarks[12].y) ** 2 + (landmarks[16].x - landmarks[12].x) ** 2 < 0.04 and
                (landmarks[16].y - landmarks[20].y) ** 2 + (landmarks[16].x - landmarks[20].x) ** 2 < 0.04
        )

        # Жест "палец вниз"
        finger_down = (
                landmarks[4].y > landmarks[3].y and landmarks[4].y > landmarks[2].y and landmarks[4].y >
                landmarks[1].y and landmarks[4].y > landmarks[8].y and landmarks[4].y > landmarks[12].y
                and landmarks[4].y > landmarks[16].y and landmarks[4].y > landmarks[20].y and
                (landmarks[4].y - landmarks[8].y) ** 2 + (landmarks[4].x - landmarks[8].x) ** 2 > 0.04 and
                (landmarks[0].x - landmarks[4].x) ** 2 < 0.09 and
                (landmarks[8].y - landmarks[12].y) ** 2 + (landmarks[8].x - landmarks[12].x) ** 2 < 0.04 and
                (landmarks[16].y - landmarks[12].y) ** 2 + (landmarks[16].x - landmarks[12].x) ** 2 < 0.04 and
                (landmarks[16].y - landmarks[20].y) ** 2 + (landmarks[16].x - landmarks[20].x) ** 2 < 0.04
        )

        if okay_sign:
            gesture = '👌'
            # cv2.putText(image, 'Okay sign', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif open_palm:
            gesture = '✋'
            # cv2.putText(image, 'Open palm', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif v_sign:
            gesture = '✌️'
            # cv2.putText(image, 'V sign', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif finger_up:
            gesture = '👍'
            # cv2.putText(image, 'Finger up', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif finger_down:
            gesture = '👎'
            # cv2.putText(image, 'Finger down', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            gesture = None

        # mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        return gesture
