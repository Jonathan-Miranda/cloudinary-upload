import os
import cloudinary
import cloudinary.uploader
import pandas as pd

# Configuración de Cloudinary
cloudinary.config(
    cloud_name="name",
    api_key="api_key",
    api_secret="api_secret"
)

# Función para subir la imagen a Cloudinary con transformación
def upload_image_with_watermark(image_path, watermark_public_id):
    # Subir la imagen a Cloudinary con formato webp y aplicar transformación (marca de agua)
    result = cloudinary.uploader.upload(image_path,
                                        format='webp',  # Convertir la imagen a .webp
                                        transformation=[{
                                            'overlay': watermark_public_id,  # Aplicar la marca de agua
                                            'gravity': 'south_east',         # Posicionar la marca en la esquina inferior derecha
                                            'opacity': 60,                   # Opacidad de la marca de agua
                                            'width': 0.2,                    # Escalar la marca de agua (20% del tamaño original)
                                            'crop': 'scale'                  # Escalar la marca de agua
                                        }])
    # Obtener la URL segura y el public_id
    return result['secure_url'], result['public_id']

# Función para procesar todas las imágenes en la carpeta y guardar el resultado en Excel
def process_images(local_folder, watermark_public_id, excel_file="imagenes_subidas.xlsx"):
    image_data = []  # Lista para almacenar datos

    for image_name in os.listdir(local_folder):
        image_path = os.path.join(local_folder, image_name)

        # Verificar si es una imagen (puedes agregar más extensiones si lo deseas)
        if image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Procesando: {image_name}")
            
            # Subir la imagen a Cloudinary con la marca de agua
            cdn_url, public_id = upload_image_with_watermark(image_path, watermark_public_id)
            
            # Agregar los datos al registro
            image_data.append({"image_name": image_name, "cdn_url": cdn_url, "public_id": public_id})

    # Crear un DataFrame con los datos y guardarlo en un archivo Excel
    df = pd.DataFrame(image_data)
    df.to_excel(excel_file, index=False)

    print(f"Proceso completado. Los datos se guardaron en {excel_file}")

# Carpeta local donde tienes las imágenes
local_folder = "./"
# Public ID de la marca de agua (debe estar ya subida a Cloudinary)
watermark_public_id = "logotipo-brudifarma"  # Asegúrate de tener esta imagen cargada en Cloudinary
process_images(local_folder, watermark_public_id)
