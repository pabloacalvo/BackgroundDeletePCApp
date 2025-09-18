import flet as ft
from pathlib import Path
from utils.backgroud_remove import BackgroundRemove

class BackgroundRemoverApp:
    
    def __init__(self, page:ft.Page):
        self.page = page
        self.directory_path = None
        self.filename_list = []
        # Inicializacion de ventana
        self._setup_page()
        self._create_components()
        self._build_ui()
        
    def _setup_page(self):
        self.page.title = ('Backgroud Remover PC')
        self.page.bgcolor = "#1e2c53"
        self.page.window.height = 900
        self.page.window.width = 700
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.vertical_alignment = ft.MainAxisAlignment.START
    
    def _create_components(self):
        #Checkbox
        self.default_folder_check = ft.Checkbox(
            label="Usar carpeta por defecto",
            value=False,
            on_change=self._checkbox_changed,
            check_color="#16213e",
            label_style=ft.TextStyle(color="#ffffff", size=14)
        )
        # Text input para ingreso de dato
        self.output_folder_textfield = ft.TextField(
            label="Carpeta de salida personalizada",
            autofocus=False,
            bgcolor="#16213e",
            border_color="#0f3460",
            focused_border_color="#e9450",
            width=350,
            height=60,
            border_radius=10,
            content_padding=ft.padding.all(5)    
        )
        # Boton de ingreso de archivos
        self.btn_pick_files = ft.ElevatedButton(bgcolor="#f18100",
                                width=250,
                                height=50,
                                content=ft.Row([
                                ft.Icon(ft.Icons.CLOUD_UPLOAD, color='#ffffff'),
                                ft.Text('Seleccionar Imagen',color="#131313",weight=ft.FontWeight.BOLD)
                                ], alignment=ft.MainAxisAlignment.CENTER),
                                style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=12),
                                    elevation=12),
                                on_click=lambda _ : file_picker.pick_files(allow_multiple=True,
                                                                        allowed_extensions=["png","bmp","jpg","jpeg"]
                                                                )
                                )
        
        # Label del boton para adjuntar archivos
        select_file_icon = ft.Icon(name=ft.Icons.ATTACH_FILE,color="#b9b9b9",size=16,)
        self.select_file_text = ft.Text("Nigun archivo seleccionado",color="#b9b9b9",size=16,)
        self.select_file_info = ft.Row([select_file_icon,self.select_file_text])
        
        # Boton de accion
        self.btn_extract = ft.ElevatedButton(content=ft.Row([
                                            ft.Icon(ft.Icons.AUTO_FIX_HIGH, color='#ffffff'),
                                            ft.Text("Remover fondos",color="#131313",weight=ft.FontWeight.BOLD)
                                        ], 
                                        alignment=ft.MainAxisAlignment.CENTER),
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=15),
                                            elevation=12),
                                        on_click= self._process_images_ui,
                                        #disabled=True,
                                        width=300,
                                        height=60,
                                        bgcolor="#e94560",
                                        color="#ffffff"
                                        )
        # Crea el elemento en el overlay
        file_picker = ft.FilePicker(on_result=self._pick_files_result)
        
        self.progress_bar = ft.ProgressBar(width=500,
                                           visible=False,
                                           color="#e49560",
                                           bgcolor="#16213e",
                                           height=8)

        self.text_progress_bar = ft.Text("",
                                         visible=False,
                                         color="#ffffff",
                                         size=14,
                                         text_align=ft.TextAlign.CENTER)
        
        self.page.overlay.append(file_picker)
          
    def _checkbox_changed(self,e: ft.ControlEvent):
        self.output_folder_textfield.disabled = e.control.value
        self.output_folder_textfield.bgcolor = "#2a2a40" if e.control.value else "#16213e"
        self.page.update()
        
    def _pick_files_result(self,e:ft.FilePickerResultEvent):
        if e.files:
            file_count = len(e.files)
            first_file_path = Path(e.files[0].path)
            self.directory_path = first_file_path.parent
            
            self.filesname_list = [file.name for file in e.files]
                

            self.select_file_text.value = f"{file_count} Archivo(s) seleccionados\nde {self.directory_path}"
            self.select_file_text.color = "#4caf50"
        else:
            self.select_file_text.value = "Nigun archivo seleccionado"
            self.select_file_text.color = "#b9b9b9"
            
        self.page.update()
 
    def _process_images_ui(self, e:ft.ControlEvent):
        self.progress_bar.visible = True
        self.progress_bar.value = 0
        self.text_progress_bar.visible =True
        self.text_progress_bar.value = "Iniciando procesamiento..."
        self.progress_bar.color = "#e94640"
        self.btn_extract.disabled = True
        self.btn_extract.bgcolor = "#666666"
        self.page.update()
        try:
            output_folder = self.output_folder_textfield.value if not self.default_folder_check.value else 'Carpeta_Stream'
            if not output_folder.strip():
                self._show_error("Por favor especifica un carpeta de salida")
                return
            remover = BackgroundRemove(self.directory_path, output_folder)
            remover.process_images(self.filesname_list,self._update_progress)
            self._show_succces("EXITO")
            self._reset_ui_process_ok()

        except Exception as e:
            self._show_error("Ocurrio un error")
        finally:
            self._reset_ui()
             
    def _build_ui(self):
        
        title = ft.Container(
            content= ft.Text(
                "Background Remover",
                size=32,
                weight=ft.FontWeight.BOLD,
                color="#ffffff",
                text_align=ft.TextAlign.CENTER
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(bottom=2)
        )
        
        subtitle = ft.Text(
            "Elimina fondos de imagenes de forma rapida y sencilla",
            size=16,
            text_align=ft.TextAlign.CENTER,
            italic=True
        )
        
        config_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.SETTINGS, color="#ffffff"),
                            ft.Text(
                                "Configuración",
                                color="#131313",
                                weight=ft.FontWeight.BOLD,
                                size=18
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Container(height=10),# para crear un espacio
                    self.default_folder_check,
                    ft.Container(height=10), # para crear un espacio
                    self.output_folder_textfield,
                ],
                spacing=5
            ),
            # atributos del container
            bgcolor="#16213e",
            padding=ft.padding.all(20),
            border_radius=15,
            border=ft.border.all(1, "#0f3460"),
            width=600
        )

        files_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.IMAGE, color="#e94560", size=20),
                            ft.Text(
                                "Seleccionar Archivos",
                                weight=ft.FontWeight.BOLD,
                                color="#ffffff",
                                size=18
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Container(height=15),
                    ft.Row(
                        [
                            self.btn_pick_files,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Container(height=10),
                    self.select_file_info,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor="#16213e",
            padding=ft.padding.all(20),
            border_radius=15,
            border=ft.border.all(1, "#0f3460"),  # corregido
            width=600
        )
        
        process_card = ft.Container(
            content= ft.Column(
                [
                    ft.Row([ft.Icon(ft.Icons.EXPLICIT_ROUNDED,color="#ff2e12",size=20),
                            ft.Text(
                                "Ejecucion",
                                weight=ft.FontWeight.BOLD,
                                color="#ffffff",
                                size=18
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Row([
                            self.btn_extract,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        self.progress_bar,
                        ft.Container(height=10),
                        self.text_progress_bar    
                ]
            ),            bgcolor="#16213e",
            padding=ft.padding.all(20),
            border_radius=15,
            border=ft.border.all(1, "#0f3460"),  # corregido
            width=600
        )
        
        self.page.add(title)
        self.page.add(subtitle)
        self.page.add(config_card)
        self.page.add(files_card)
        self.page.add(process_card)

    def _update_progress(self,processed, total,current_file):
        progress = processed / total
        self.progress_bar.value = progress
        self.text_progress_bar.value = f"Procesando {current_file} ({processed}/{total})"
        self.page.update()

    def _reset_ui(self):
        self.btn_extract.disabled = False
        self.btn_extract.bgcolor = "#e94640"
        self.page.update()

    def _reset_ui_process_ok(self):
        self.output_folder_textfield.value = ''
        self.progress_bar.visible = False
        self.progress_bar.value = 0
        self.text_progress_bar.visible = False
        self.text_progress_bar.value = ''
        self.select_file_text.value='Ningun archivo seleccionado'
        self.default_folder_check.value = False
        self.btn_extract.disabled = False
        self.btn_extract.bgcolor = "#e94640"
        self.page.update()
        
    def _show_error(self,message):
        dlg = ft.AlertDialog(
            title=ft.Text("Error", color="#f44336"),
            content=ft.Text(message, color="#ffffff"),
            bgcolor="#12213e",
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: self.page.close(dlg),
                    style=ft.ButtonStyle(color="#e94560")
                )
            ]
        )
        self.page.open(dlg)
        
    def _show_succces(self,message):
        dlg = ft.AlertDialog(
            title=ft.Text("Tarea concluida", color="#4CAF50"),
            content=ft.Text(message, color="#ffffff"),
            bgcolor="#16213e",
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: self.page.close(dlg),
                    style=ft.ButtonStyle(color="#4CAF50")
                )
            ]
        )
        self.page.open(dlg)

def main(page: ft.Page):
    obj = BackgroundRemoverApp(page)
    

ft.app(target=main)