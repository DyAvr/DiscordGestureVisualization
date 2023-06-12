import sys
import mediapipe as mp
import cv2
import discord
from PyQt6.QtWidgets import QApplication
from settings_control import GestureControlApp

# TOKEN = 'MTEwNTkxODcwMjYxODE2NTMyMQ.GGyKzP._HrO4hpZxfK8OaaHbufsB7cwB2p0Y1T53TswxY'
# VOICE_CHANNEL_ID = 1105722435594113145
#
# bot = discord.Client(intents=discord.Intents.all())
#
# emoji_dict = {
#     '👍': 'images/thumbs_up.png',
#     '👎': 'images/thumbs_down.png',
#     '✌️': 'images/victory_hand.png',
#     '👌': 'images/ok_hand.png',
#     '✋': 'images/raised_hand.png'
# }
#
#
# @bot.event
# async def on_ready():
#     global voice_client
#     await asyncio.sleep(5)
#     await bot.user.edit(avatar=None)
#     voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
#     voice_client = await join_voice_channel(voice_channel)
#     print(f'{bot.user} подключен Discord!')
#     with open(emoji_dict['👍'], 'rb') as f:
#         await bot.user.edit(avatar=f.read())
#     print(f'{bot.user} сменил аватарку!')
#     ctx = bot.get_channel(1105722435594113143)
#     await ctx.send(f'Пользователь отреагировал: 👍')
#     await asyncio.sleep(3)
#     await bot.user.edit(avatar=None)
#
# async def join_voice_channel(channel):
#     try:
#         voice_client = await channel.connect()
#         print(f'Бот присоединился к голосовому каналу {channel.name}')
#         return voice_client
#     except Exception as e:
#         print(f'Ошибка при подключении к голосовому каналу: {e}')
#
#
# async def gesture_recognition():
#     while True:
#         # Здесь можно добавить другие асинхронные задачи, которые не будут блокировать код
#         print("Другая задача выполняется...")
#         await asyncio.sleep(5)
#
#
# @bot.event
# async def on_shutdown():
#     print('Завершение программы...')
#     await bot.close()


# @bot.command(name='change_avatar')
# async def change_avatar(ctx, emoji: str):
#     if emoji in emoji_dict:
#         with open(emoji_dict[emoji], 'rb') as f:
#             await bot.user.edit(avatar=f.read())
#         await ctx.send(emoji)
#         await asyncio.sleep(3)
#         await bot.user.edit(avatar=None)
#     else:
#         await ctx.send('Invalid emoji. Please use one of the following: 👍, ✋, 😄, 😞, 👎')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = GestureControlApp()
    mainWin.showMaximized()
    sys.exit(app.exec())
    # loop = asyncio.get_event_loop()
    # try:
    #     loop.create_task(bot.start(TOKEN))
    #     # loop.create_task(gesture_recognition())
    #     loop.run_forever()
    # except KeyboardInterrupt:
    #     print('Программа была прервана пользователем')
    # finally:
    #     loop.run_until_complete(on_shutdown())
    #     loop.close()
    # mp_drawing = mp.solutions.drawing_utils
    # mp_hands = mp.solutions.hands
    #
    # # Захват видео с камеры
    # cap = cv2.VideoCapture(0)
    #
    # with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    #     while cap.isOpened():
    #         ret, frame = cap.read()
    #         if not ret:
    #             print("Ignoring empty camera frame.")
    #             continue
    #
    #
    #         # Перевод изображения в формат RGB
    #         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         image.flags.writeable = False
    #         results = hands.process(image)
    #
    #         # Возвращение изображения в формат BGR
    #         image.flags.writeable = True
    #         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #
    #         if results.multi_hand_landmarks:
    #             for hand_landmarks in results.multi_hand_landmarks:
    #                 landmarks = hand_landmarks.landmark
    #
    #                 # Жест "окей" (👌)
    #                 okay_sign = (
    #                         landmarks[8].x - 0.1 < landmarks[4].x < landmarks[8].x + 0.1 and
    #                         landmarks[8].y - 0.1 < landmarks[4].y < landmarks[8].y + 0.1 and
    #                         (landmarks[8].y - landmarks[12].y) ** 2 + (landmarks[8].x - landmarks[12].x) ** 2 > 0.02 and
    #                         (landmarks[8].y - landmarks[16].y) ** 2 + (landmarks[8].x - landmarks[16].x) ** 2 > 0.02 and
    #                         (landmarks[8].y - landmarks[20].y) ** 2 + (landmarks[8].x - landmarks[20].x) ** 2 > 0.02
    #                 )
    #
    #                 # Жест "открытая ладонь" (✋)
    #                 open_palm = (
    #                         landmarks[4].y < landmarks[3].y and landmarks[8].y < landmarks[6].y and
    #                         landmarks[12].y < landmarks[10].y and landmarks[16].y < landmarks[14].y and
    #                         landmarks[20].y < landmarks[18].y and
    #                         (landmarks[0].y - landmarks[12].y) ** 2 > 0.16
    #                 )
    #
    #                 # Жест "V" (✌️)
    #                 v_sign = (
    #                         landmarks[8].y < landmarks[6].y and
    #                         landmarks[12].y < landmarks[10].y and
    #                         (landmarks[4].y - landmarks[16].y) ** 2 + (landmarks[4].x - landmarks[16].x) ** 2 < 0.09 and
    #                         (landmarks[4].y - landmarks[20].y) ** 2 + (landmarks[4].x - landmarks[20].x) ** 2 < 0.09 and
    #                         (landmarks[16].y - landmarks[20].y) ** 2 + (landmarks[16].x - landmarks[20].x) ** 2 < 0.02 and
    #                         (landmarks[8].y - landmarks[12].y) ** 2 + (landmarks[8].x - landmarks[12].x) ** 2 > 0.01
    #                 )
    #
    #                 # Жест "палец вверх"
    #                 finger_up = (
    #                         landmarks[4].y < landmarks[3].y and landmarks[4].y < landmarks[2].y and landmarks[4].y <
    #                         landmarks[1].y and landmarks[4].y < landmarks[8].y and landmarks[4].y < landmarks[12].y
    #                         and landmarks[4].y < landmarks[16].y and landmarks[4].y < landmarks[20].y and
    #                         (landmarks[4].y - landmarks[8].y) ** 2 + (landmarks[4].x - landmarks[8].x) ** 2 > 0.04 and
    #                         (landmarks[0].x - landmarks[4].x) ** 2 < 0.09 and
    #                         (landmarks[8].y - landmarks[12].y) ** 2 + (landmarks[8].x - landmarks[12].x) ** 2 < 0.04 and
    #                         (landmarks[16].y - landmarks[12].y) ** 2 + (landmarks[16].x - landmarks[12].x) ** 2 < 0.04 and
    #                         (landmarks[16].y - landmarks[20].y) ** 2 + (landmarks[16].x - landmarks[20].x) ** 2 < 0.04
    #                 )
    #
    #                 # Жест "палец вниз"
    #                 finger_down = (
    #                         landmarks[4].y > landmarks[3].y and landmarks[4].y > landmarks[2].y and landmarks[4].y >
    #                         landmarks[1].y and landmarks[4].y > landmarks[8].y and landmarks[4].y > landmarks[12].y
    #                         and landmarks[4].y > landmarks[16].y and landmarks[4].y > landmarks[20].y and
    #                         (landmarks[4].y - landmarks[8].y) ** 2 + (landmarks[4].x - landmarks[8].x) ** 2 > 0.04 and
    #                         (landmarks[0].x - landmarks[4].x) ** 2 < 0.09 and
    #                         (landmarks[8].y - landmarks[12].y) ** 2 + (landmarks[8].x - landmarks[12].x) ** 2 < 0.04 and
    #                         (landmarks[16].y - landmarks[12].y) ** 2 + (landmarks[16].x - landmarks[12].x) ** 2 < 0.04 and
    #                         (landmarks[16].y - landmarks[20].y) ** 2 + (landmarks[16].x - landmarks[20].x) ** 2 < 0.04
    #                 )
    #
    #                 if okay_sign:
    #                     cv2.putText(image, 'Okay sign', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    #                 elif open_palm:
    #                     cv2.putText(image, 'Open palm', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    #                 elif v_sign:
    #                     cv2.putText(image, 'V sign', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    #                 elif finger_up:
    #                     cv2.putText(image, 'Finger up', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    #                 elif finger_down:
    #                     cv2.putText(image, 'Finger down', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    #
    #                 mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    #
    #         cv2.imshow('MediaPipe Hands', image)
    #         if cv2.waitKey(60) & 0xFF == 27:
    #             break
    #
    # cap.release()
    # cv2.destroyAllWindows()

