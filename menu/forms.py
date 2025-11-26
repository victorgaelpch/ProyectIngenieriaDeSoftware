# menu/forms.py
from django import forms
from .models import Producto, Categoria, Subcategoria
from decimal import Decimal

class ProductoForm(forms.ModelForm):
    categoria_id = forms.ChoiceField(
        label="Categoría",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    subcategoria_id = forms.ChoiceField(
        label="Subcategoría",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    imagen = forms.ImageField(
        label="Imagen del Producto",
        required=False, # Puede ser opcional
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*', # Solo imágenes
        }),
        help_text="Selecciona una imagen para el producto."
    )
 

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria_id', 'subcategoria_id', 'imagen', 'stock', 'activo', 'puntos_extra']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del producto',
                'rows': 3
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
        
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'puntos_extra': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Puntos extra otorgados',
                'min': '0'
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            
            'stock': 'Stock disponible',
            'activo': 'Producto activo',
            'puntos_extra': 'Puntos Extra',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Poblar opciones de categoría
        categorias = Categoria.objects.filter(activo=True)
        choices_categoria = [('', 'Selecciona una categoría')]
        for categoria in categorias:
            choices_categoria.append((str(categoria.id), categoria.nombre))
        self.fields['categoria_id'].choices = choices_categoria
       
        subcategorias = Subcategoria.objects.filter(activo=True)
        choices_subcategoria = [('', 'Selecciona una subcategoría (opcional)')]
        for subcategoria in subcategorias:
            choices_subcategoria.append((str(subcategoria.id), subcategoria.nombre))
        self.fields['subcategoria_id'].choices = choices_subcategoria
        
        if self.instance and self.instance.pk:
            if self.instance.categoria_id:
                self.fields['categoria_id'].initial = str(self.instance.categoria_id)
            if self.instance.subcategoria_id:
                self.fields['subcategoria_id'].initial = str(self.instance.subcategoria_id)
            self.fields['activo'].initial = self.instance.activo
         
        else:
         
            self.fields['activo'].initial = True
            self.fields['stock'].initial = 0
            self.fields['puntos_extra'].initial = 0

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and int(precio) < 0:
            raise forms.ValidationError('El precio no puede ser negativo')
        return Decimal(str(precio)) if precio is not None else None

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        # Verificar si stock es una cadena vacía o None
        if stock == '' or stock is None:
            return None
        try:
            stock_int = int(stock)
        except (ValueError, TypeError):
            # Si no se puede convertir a entero, lanza un error
            raise forms.ValidationError('El stock debe ser un número entero válido.')

        if stock_int < 0:
            raise forms.ValidationError('El stock no puede ser negativo')
        return stock_int # Retornar el valor entero ya validado

    def clean_activo(self):
        activo = self.cleaned_data.get('activo')
        if isinstance(activo, str):
            return activo.lower() == 'true'
        return bool(activo)

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')

        # Si llega como string (ruta guardada), no es archivo → ignorar
        if isinstance(imagen, str):
            return imagen

        # Si no hay archivo subido → permitir
        if imagen is None:
            return None

        # A partir de aquí, ES UN ARCHIVO
        # Validar tamaño
        MAX_SIZE_MB = 30
        if imagen.size > MAX_SIZE_MB * 1024 * 1024:
            raise forms.ValidationError(f'La imagen no debe pesar más de {MAX_SIZE_MB}MB.')

        # Validar extensión
        import os
        ext = os.path.splitext(imagen.name)[1].lower()
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        if ext not in valid_extensions:
            raise forms.ValidationError('Formato de imagen no permitido. Use JPG, JPEG, PNG o GIF.')

        return imagen

    def clean(self):
        """
        Limpia y prepara los datos del formulario antes de la validación final.
        """
        cleaned_data = super().clean()
        imagen_file = cleaned_data.get('imagen')

            # Si hay un archivo de imagen, lo quitamos temporalmente de cleaned_data
            # para que no se intente asignar al campo imagen del modelo Cassandra
            # durante form.save(commit=False). Lo manejaremos en la vista.
        if imagen_file is not None:
                # Guardamos el archivo en una variable temporal del formulario
            self.cleaned_imagen_file = imagen_file
                # Removemos el archivo de cleaned_data
            cleaned_data.pop('imagen', None) # pop con default para evitar KeyError si no existe
        return cleaned_data