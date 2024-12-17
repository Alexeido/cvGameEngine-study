import cv2
import numpy as np
import os
import concurrent.futures

def preprocess_video(input_path, output_path, max_height=180):
    # Abrir el video
    video = cv2.VideoCapture(input_path)
    if not video.isOpened():
        raise Exception(f"Error: No se pudo abrir el video: {input_path}")
    
    # Obtener propiedades del video
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calcular la nueva resolución manteniendo la relación de aspecto
    aspect_ratio = width / height
    if height > max_height:
        height = max_height
        width = int(aspect_ratio * height)
    
    # Definir el codec y crear el writer con la nueva resolución
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')  # Codec FFV1 para AVI sin pérdida
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=True)
    
    # Colores
    black = [0, 0, 0]
    white = [255, 255, 255]
    light_blue_exact = [250, 250, 0]  # Azul claro específico (#0FFAF4)

    frame_count = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
            
        # Redimensionar el frame a la nueva resolución
        resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_LINEAR)
        
        # Crear un nuevo frame con los colores específicos (negro, blanco, azul claro)
        processed_frame = np.zeros_like(resized_frame)

        # Convertir a escala de grises para detectar negros y blancos
        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

        # Definir máscaras para los colores
        # Píxeles negros (intensidad baja)
        processed_frame[np.all(resized_frame <= [50, 50, 50], axis=-1)] = black

        # Píxeles blancos (intensidad alta)
        white_mask = np.all(resized_frame >= [200, 200, 200], axis=-1)
        processed_frame[white_mask] = white
        
        # Píxeles azul claro exacto (RGB: 15, 250, 244)
        lower_blue = np.array([100, 100, 10])  # Ligeramente inferior al color exacto
        upper_blue = np.array([255, 255, 100])  # Ligeramente superior al color exacto
        blue_mask = cv2.inRange(resized_frame, lower_blue, upper_blue)
        processed_frame[blue_mask > 0] = light_blue_exact

        # --- Suavizado de las máscaras (eliminación de ruido) ---
        # Dilatar las máscaras para agrandar áreas
        white_mask_dilated = cv2.dilate(white_mask.astype(np.uint8), np.ones((3, 3), np.uint8))
        blue_mask_dilated = cv2.dilate(blue_mask.astype(np.uint8), np.ones((3, 3), np.uint8))

        # Si un píxel blanco está rodeado de azul, convertirlo a azul
        white_to_blue = (white_mask_dilated == 1) & (blue_mask_dilated == 1)
        processed_frame[white_to_blue] = light_blue_exact

        # Si un píxel azul está rodeado de blanco, convertirlo a blanco
        blue_to_white = (blue_mask_dilated == 1) & (white_mask_dilated == 1)
        processed_frame[blue_to_white] = white

        # Guardar el frame procesado
        out.write(processed_frame)
        
        # Mostrar progreso
        frame_count += 1
        if frame_count % 30 == 0:
            progress = (frame_count / total_frames) * 100
            print(f"Progreso: {progress:.1f}%")
    
    # Liberar recursos
    video.release()
    out.release()
    print(f"Procesamiento completado: {input_path}")

def process_video_file(filename, input_folder='./ataques/papyrus/'):
    input_path = os.path.join(input_folder, filename)
    output_name = f"{os.path.splitext(filename)[0]}_processed.avi"  # Cambiado a .avi
    output_path = os.path.join(input_folder, output_name)
    
    print(f"Procesando: {filename}")
    preprocess_video(input_path, output_path)
    print(f"Completado: {output_name}")

def process_all_videos(input_folder='./ataques/papyrus/', max_workers=4):
    # Asegurarse de que la carpeta existe
    if not os.path.exists(input_folder):
        raise Exception(f"La carpeta {input_folder} no existe")
    
    # Obtener la lista de archivos de video a procesar
    video_files = [f for f in os.listdir(input_folder) if f.endswith('.mp4') and not f.endswith('_processed.avi')]
    
    # Usar un ThreadPoolExecutor para procesar varios videos en paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_video_file, filename, input_folder) for filename in video_files]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Capturar cualquier excepción que ocurra en los hilos
            except Exception as exc:
                print(f"Error al procesar un video: {exc}")

if __name__ == "__main__":
    try:
        process_all_videos()
    except Exception as e:
        print(f"Error: {str(e)}")
