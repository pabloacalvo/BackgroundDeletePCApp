from pathlib import Path
import shutil
from rembg import remove
import datetime


class BackgroundRemove():
    SUPPORTED_EXTENCION = ('.png', '.png','.jpeg','.bmp')
    
    def __init__(self,input_folder,output_folder):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        
    def process_images(self, filename_list, process_callback=None): #output/2025-09-15_00_00
        today_date = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M-%S')
        self._processed_folder = self.output_folder / today_date
        self._processed_folder.mkdir(parents=True, exist_ok=True)# Crea las carpeta padre si no existen, y si existe no arroja error FileExistsError
        
        total_file = len(filename_list)
        processed = 0
        
        if total_file > 0:
            for file in filename_list:
                if self._is_supported_image(file):
                    input_path = self.input_folder / file
                    output_path = self._processed_folder / file
                    try:
                        self._remove_background(input_path, output_path)
                        self._move_original_file(input_path)
                        processed += 1
                        if process_callback is not None:
                            process_callback(processed,total_file,file)
                    except Exception as e:
                        print(f"Error procesando archivo {input_path}: {e}")
                        if process_callback is not None:
                            process_callback(processed,total_file,file)
                            print(f"Error en el archivo {file}")
                else:
                    continue
         
    def _is_supported_image(self, filename:str):
        return filename.lower().endswith(self.SUPPORTED_EXTENCION)
           
    def _remove_background(self,input_path,output_path): 
        with open(input_path, 'rb') as f_in, open(output_path,'wb') as f_out:
            output = remove(f_in.read()) # remove -> metodo de rembg para eliminar el fondo
            f_out.write(output)
        
    def _move_original_file(self,input_path): #-> output/originals/image.png
        original_folder:Path = self._processed_folder / 'originals' # output/originals
        original_folder.mkdir(exist_ok=True) # Crea la carpeta aunque exista
        
        new_path = original_folder / input_path.name # output/originals/imagen.png
        input_path.rename(new_path)


        

"""obj = BackgroundRemove(Path("C:\\Users\\Pablo\\OneDrive\\Escritorio\\"),Path('C:\\Users\\Pablo\\OneDrive\\Escritorio\\Output_folder'))
obj.process_images(['images.png'])"""

