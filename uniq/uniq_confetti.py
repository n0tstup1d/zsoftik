import cv2
import asyncio
import numpy as np
import random
import os
import shutil
import subprocess
import data.db_helper as db
import other.generate as generate_photo
import time
import data.db_helper as db_helper

#FFMPEG_PATH = r'C:\\Users\\Administrator\\Desktop\\ffmpeg\\bin\\ffmpeg'  # Укажите путь к ffmpeg
FFMPEG_PATH = "C:\\Windows\\ffmpeg"

def safe_subprocess_run(command):
    """Запускаем subprocess с ожиданием завершения и проверкой ошибок"""
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {command}\n{e}")
        raise


def add_confetti_effect(u_info, input_video_path, output_video_path, num_particles=100, speed=5, particle_size=5):
    cap = cv2.VideoCapture(input_video_path)
    try:
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        outt = cv2.VideoWriter(output_video_path, fourcc, fps, (video_width, video_height))
        if u_info[8] == 1:
            speed = u_info[10]
            particles = [{
                'position': [np.random.randint(0, video_width), np.random.randint(0, video_height)],
                'direction': [np.random.choice([-1, 1]) * speed, np.random.choice([-1, 1]) * speed]
            } for _ in range(int(u_info[9]))]

            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

            frame_count = 0
            while frame_count < total_frames:
                ret, frame = cap.read()
                if not ret:
                    break

                for particle in particles:
                    x, y = particle['position']
                    dx, dy = particle['direction']

                    x = int(x + dx)
                    y = int(y + dy)

                    if x <= 0 or x >= video_width - particle_size:
                        particle['direction'][0] *= -1
                    if y <= 0 or y >= video_height - particle_size:
                        particle['direction'][1] *= -1

                    particle['position'] = [x, y]

                    color = random.choice(colors)
                    cv2.rectangle(frame, (x, y), (x + particle_size, y + particle_size), color, -1)

                outt.write(frame)
                frame_count += 1

        else:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                outt.write(frame)

    finally:
        cap.release()
        outt.release()

    if not os.path.exists(output_video_path):
        raise FileNotFoundError(f"Файл не был создан: {output_video_path}")

    print(f"Видео успешно сохранено в {output_video_path}")


async def init_db():
    database_bot = db.DatabaseBot("DataBase//bd.db")
    await database_bot.connect()
    return database_bot


def add_fade_effect(input_video_path, output_video_path, fade_duration, total_duration):
    fade_in_start = 0
    fade_in_duration = int(fade_duration * 25)
    fade_out_duration = int(fade_duration * 25)
    fade_out_start = int(total_duration * 25) - fade_out_duration

    fade_command = [
        FFMPEG_PATH, '-i', input_video_path,
        '-vf', f'fade=in:{fade_in_start}:{fade_in_duration},fade=out:{fade_out_start}:{fade_out_duration}',
        '-c:v', 'libx264', '-c:a', 'copy', '-preset', 'ultrafast', '-crf', '28', '-y', output_video_path
    ]
    print(f"Running fade effect command: {' '.join(fade_command)}")
    safe_subprocess_run(fade_command)

    if not os.path.exists(output_video_path):
        raise FileNotFoundError(f"Файл с эффектом fade не был создан: {output_video_path}")

    if os.path.exists(input_video_path):
        os.remove(input_video_path)


def combine_audio_with_video(input_video_path, original_video_path, output_video_path):
    combine_command = [
        FFMPEG_PATH, '-i', input_video_path, '-i', original_video_path, '-c:v', 'copy', '-c:a', 'aac',
        '-map', '0:v:0', '-map', '1:a:0', '-shortest', '-y', output_video_path
    ]
    print(f"Combining audio and video: {' '.join(combine_command)}")
    subprocess.run(combine_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.exists(output_video_path):
        raise FileNotFoundError(f"Файл с объединенным аудио и видео не был создан: {output_video_path}")

    os.remove(input_video_path)


def apply_darkness_effect(input_video_path, output_video_path, darkness_level):
    darkness_command = [
        FFMPEG_PATH, '-i', input_video_path,
        '-vf', f'eq=brightness=-{darkness_level}',
        '-c:v', 'libx264', '-c:a', 'copy', '-preset', 'ultrafast', '-crf', '28', '-y', output_video_path
    ]
    print(f"Running darkness effect command: {' '.join(darkness_command)}")
    safe_subprocess_run(darkness_command)

    if not os.path.exists(output_video_path):
        raise FileNotFoundError(f"Файл с эффектом darkness не был создан: {output_video_path}")

    if os.path.exists(input_video_path):
        os.remove(input_video_path)


def move_creo(creo_frame, bg_width, bg_height, x_pos, y_pos, x_dir, y_dir, speed):
    x_pos += x_dir * speed
    y_pos += y_dir * speed

    if x_pos <= 0 or x_pos + creo_frame.shape[1] >= bg_width:
        x_dir *= -1
    if y_pos <= 0 or y_pos + creo_frame.shape[0] >= bg_height:
        y_dir *= -1

    return x_pos, y_pos, x_dir, y_dir


def overlay_creo_on_background(bg, creo, x, y, transparency):
    overlay = creo[:, :, :3]
    mask = creo[:, :, 3:] / 255.0
    mask = np.repeat(mask, 3, axis=2)

    h, w, _ = overlay.shape

    # Ensure y, h, x, w are integers
    h = int(h)
    w = int(w)
    y = int(y)
    x = int(x)

    if y + h > bg.shape[0]:
        h = bg.shape[0] - y
        overlay = overlay[:h, :, :]
        mask = mask[:h, :, :]

    if x + w > bg.shape[1]:
        w = bg.shape[1] - x
        overlay = overlay[:, :w, :]
        mask = mask[:, :w, :]

    background_section = bg[y:y + h, x:x + w]

    if overlay.shape[:2] != background_section.shape[:2]:
        return bg

    blended = (background_section * (1 - mask * transparency) + overlay * (mask * transparency)).astype(np.uint8)
    bg[y:y + h, x:x + w] = blended

    return bg


def apply_brightness_effect(input_video_path, output_video_path, brightness_level):
    brightness_command = [
        FFMPEG_PATH, '-i', input_video_path,
        '-vf', f'eq=brightness={brightness_level}',
        '-c:v', 'libx264', '-c:a', 'copy', '-preset', 'ultrafast', '-crf', '28', '-y', output_video_path
    ]
    print(f"Running brightness effect command: {' '.join(brightness_command)}")
    safe_subprocess_run(brightness_command)

    if not os.path.exists(output_video_path):
        raise FileNotFoundError(f"Файл с эффектом brightness не был создан: {output_video_path}")

    if os.path.exists(input_video_path):
        os.remove(input_video_path)


def add_audio_noise(input_video_path, output_video_path, noise_level):
    print(noise_level)
    audio_noise_command = [
        FFMPEG_PATH, '-i', input_video_path,
        '-filter_complex',
        f'[0:a]volume=1.0[aud];anoisesrc=color=white:amplitude={noise_level}[noise];[aud][noise]amix=inputs=2:duration=first:dropout_transition=2',
        '-c:v', 'copy', '-c:a', 'aac', '-y', output_video_path
    ]
    print(f"Running audio noise command: {' '.join(audio_noise_command)}")
    safe_subprocess_run(audio_noise_command)

    if not os.path.exists(output_video_path):
        raise FileNotFoundError(f"Файл с добавленным шумом не был создан: {output_video_path}")

    if os.path.exists(input_video_path):
        os.remove(input_video_path)


def combine_audio_with_video(input_video_path, original_video_path, output_video_path):
    combine_command = [
        FFMPEG_PATH, '-i', input_video_path, '-i', original_video_path, '-c:v', 'copy', '-c:a', 'aac',
        '-map', '0:v:0', '-map', '1:a:0', '-shortest', '-y', output_video_path
    ]
    print(f"Combining audio and video: {' '.join(combine_command)}")
    safe_subprocess_run(combine_command)

    if not os.path.exists(output_video_path):
        raise FileNotFoundError(f"Файл с объединенным аудио и видео не был создан: {output_video_path}")

    os.remove(input_video_path)


def compress_video(input_video_path, output_video_path):
    compress_command = [
        FFMPEG_PATH, '-i', input_video_path,
        '-vcodec', 'libx264', '-crf', '30', '-preset', 'medium',
        '-b:v', '800k',  # Ограничиваем битрейт для уменьшения размера
        '-c:a', 'aac', '-b:a', '128k',
        '-y', output_video_path
    ]
    print(f"Running compression command: {' '.join(compress_command)}")
    safe_subprocess_run(compress_command)

    if not os.path.exists(output_video_path):
        raise FileNotFoundError(f"Файл сжатого видео не был создан: {output_video_path}")

    print(f"Видео успешно сжато и сохранено в {output_video_path}")


async def process_video(video_names, i):
    '''async with db.DatabaseBot("DataBase/bd.db") as db_bot:
        u_info = await db_bot.uniq_info()'''
    try:
        u_info = await db_helper.get_confetti_info()


        try:
            scale = u_info[3]
        except Exception as e:
            print(e)
        transparency = u_info[2]
        transparency = float(transparency)
        speed = u_info[1]
        speed = float(speed)
        yty = random.randint(1,111111111111111)
        prompt = "Create a dynamic and vibrant scene featuring a celebration with colorful confetti falling from the sky. The confetti is diverse in shape and size, with varying speeds and opacities, some pieces large and others small, scattering in all directions. The scene should have bright and dark lighting elements to highlight both the lighter and darker tones of the confetti. Include elements like sparkling lights or glowing effects around the confetti to enhance the festive atmosphere. The confetti should vary in density across the image, with some areas showing more intense bursts, while other areas have fewer pieces floating down. Make sure the image conveys a sense of motion and excitement, as if the celebration is in full swing, with confetti swirling through the air."
        background_path = f'temp/photo_{yty}.jpg'
        background_image = await generate_photo.generate_image(video_names[0], i, prompt, background_path)
        output_path = f'temp/unique_{video_names}'

        background = cv2.imread(background_path, cv2.IMREAD_UNCHANGED)
        bg_height, bg_width = background.shape[:2]
        print(video_names)
        creo_path = f'videos//{video_names}'
        cap = cv2.VideoCapture(creo_path)

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        if fps == 0:
            fps = 30



        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if fps == 0:
            fps = 30
        duration = total_frames / fps
        output_video_path = creo_path.replace(".mp4", "_overlay.mp4")
        temp_video_path = output_video_path.replace(".mp4", "_temp.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        outt = cv2.VideoWriter(temp_video_path, fourcc, fps, (bg_width, bg_height))



        x_pos, y_pos = random.randint(0, bg_width - int(bg_width * scale)), random.randint(0, bg_height - int(
            bg_height * scale))
        x_dir, y_dir = random.choice([-1, 1]), random.choice([-1, 1])

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            scaled_width = int(bg_width * scale)
            scaled_height = int((scaled_width / frame.shape[1]) * frame.shape[0])
            frame = cv2.resize(frame, (scaled_width, scaled_height))

            if scale < 1.0:
                x_pos, y_pos, x_dir, y_dir = move_creo(frame, bg_width, bg_height, x_pos, y_pos, x_dir, y_dir, speed)
            background_frame = background.copy()
            bg_with_creo = overlay_creo_on_background(background_frame, frame, x_pos, y_pos, transparency)
            outt.write(cv2.cvtColor(bg_with_creo, cv2.COLOR_BGRA2BGR))

        cap.release()
        outt.release()

        if not os.path.exists(temp_video_path):
            raise FileNotFoundError(f"Файл с наложенным крео не был создан: {temp_video_path}")

        # Комбинируем оригинальную аудиодорожку с новым видео
        combine_audio_with_video(temp_video_path, creo_path, output_video_path)

        final_video_path = output_video_path
        if u_info[5] == 1:
            fade_duration = u_info[4]
            print("Применение эффекта fade...")
            faded_video_path = output_video_path.replace(".mp4", "_faded.mp4")
            add_fade_effect(output_video_path, faded_video_path, fade_duration, duration)
            final_video_path = faded_video_path

        darkness_level = 0.05
        brightness_level = 0.15

        if u_info[7] == 1:
            print("Применение эффекта затемнения...")
            darkened_video_path = final_video_path.replace(".mp4", "_darkened.mp4")
            apply_darkness_effect(final_video_path, darkened_video_path, darkness_level)
            final_video_path = darkened_video_path

        if u_info[6] == 1:
            print("Применение эффекта повышения яркости...")
            brightened_video_path = final_video_path.replace(".mp4", "_brightened.mp4")
            apply_brightness_effect(final_video_path, brightened_video_path, brightness_level)
            final_video_path = brightened_video_path

            # Добавляем случайный FPS и шум
        random_fps = random.randint(30, 40)
        random_noise_leve = float(random.uniform(0.01, 0.1))
        random_noise_level = round(random_noise_leve, 2)
        final_video_with_noise = final_video_path.replace(".mp4", f"_fps{random_fps}_noise.mp4")
        add_audio_noise(final_video_path, final_video_with_noise, random_noise_level)

        # Перезаписываем существующий файл если он уже есть
        try:
            if os.path.exists(output_path):
                os.remove(output_path)
        except Exception as e:
            '''requests.get(
                f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id=646534367&text=[{user_id}]: Не удалось уникализовать \n{e} ')'''
            time.sleep(30)
            try:
                if os.path.exists(output_path):
                    os.remove(output_path)
            except Exception as e:
                '''requests.get(
                        f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id=646534367&text=[{user_id}]: Не удалось уникализовать \n{e} ')'''
                time.sleep(30)
                if os.path.exists(output_path):
                    os.remove(output_path)

        # Переименовываем файл с шумом как финальное видео
        os.rename(final_video_with_noise, output_path)

        # Теперь добавляем конфетти и объединяем аудиодорожку заново
        confetti_video_path = output_path.replace(".mp4", "_confetti.mp4")
        print(u_info[8])

        add_confetti_effect(u_info, output_path, confetti_video_path)

        # Финальный путь для видео (то же имя, что и output_path)
        final_video_with_audio = output_path

        # Применяем эффекты и сохраняем видео с аудио
        combine_audio_with_video(confetti_video_path, creo_path, final_video_with_audio)

        # Определяем путь для сжатого видео (можно сделать резервную копию или использовать другой путь, чтобы избежать перезаписи)
        compressed_video_path = output_path.replace(".mp4", "_compressed.mp4")

        # Сжимаем видео и сохраняем в новый файл
        compress_video(final_video_with_audio, compressed_video_path)  # Вызываем сжатие

        try:
            if os.path.exists(output_path):
                os.remove(output_path)
        except Exception as e:
            '''requests.get(
                f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id=646534367&text=[{user_id}]: Не удалось уникализовать \n{e} ')'''
            time.sleep(30)
            try:
                if os.path.exists(output_path):
                    os.remove(output_path)
            except Exception as e:
                '''requests.get(
                    f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id=646534367&text=[{user_id}]: Не удалось уникализовать \n{e} ')'''
                time.sleep(30)
                if os.path.exists(output_path):
                    os.remove(output_path)


        try:
            shutil.move(compressed_video_path, output_path)
        except Exception as e:
            '''requests.get(
                f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id=646534367&text=[{user_id}]: Не удалось уникализовать \n{e} ')'''
            time.sleep(30)
            try:
                shutil.move(compressed_video_path, output_path)
            except Exception as e:
                '''requests.get(
                    f'https://api.telegram.org/bot{config.bot_token}/sendMessage?chat_id=646534367&text=[{user_id}]: Не удалось уникализовать \n{e} ')'''
                time.sleep(30)
                shutil.move(compressed_video_path, output_path)


        # Удаляем временные файлы, если они существуют
        if os.path.exists(confetti_video_path):
            os.remove(confetti_video_path)
            os.remove(f'temp/photo_{yty}.jpg')

        print(f"Видео с конфетти и оригинальным звуком успешно сохранено в {output_path}")
    except Exception as e:
        print(e)