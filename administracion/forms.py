# administracion/forms.py
from django import forms
from menu.models import Categoria, Subcategoria, AtributoSubcategoria
import json

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'modern-input',
                'placeholder': 'Nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'modern-input',
                'placeholder': 'Descripción',
                'rows': 3
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'modern-checkbox'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['activo'].initial = self.instance.activo
        else:
            self.fields['activo'].initial = True

    def clean_activo(self):
        activo = self.cleaned_data.get('activo')
        if isinstance(activo, str):
            return activo.lower() == 'true'
        return bool(activo)

class SubcategoriaForm(forms.ModelForm):
    categoria_id = forms.ChoiceField(
        label="Categoría",
        widget=forms.Select(attrs={'class': 'modern-input'})
    )
    
    class Meta:
        model = Subcategoria
        fields = ['categoria_id', 'nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'modern-input',
                'placeholder': 'Nombre de la subcategoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'modern-input',
                'placeholder': 'Descripción',
                'rows': 3
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'modern-checkbox'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Poblar opciones de categoría
        categorias = Categoria.objects.filter(activo=True)
        choices = [('', 'Selecciona una categoría')]
        for categoria in categorias:
            choices.append((str(categoria.id), categoria.nombre))
        self.fields['categoria_id'].choices = choices
        
        if self.instance and self.instance.pk:
            self.fields['activo'].initial = self.instance.activo
            if self.instance.categoria_id:
                self.fields['categoria_id'].initial = str(self.instance.categoria_id)
        else:
            self.fields['activo'].initial = True

    def clean_activo(self):
        activo = self.cleaned_data.get('activo')
        if isinstance(activo, str):
            return activo.lower() == 'true'
        return bool(activo)

class AtributoSubcategoriaForm(forms.ModelForm):
    categoria_id = forms.ChoiceField(
        label="Categoría",
        widget=forms.Select(attrs={'class': 'modern-input'})
    )
    
    subcategoria_id = forms.ChoiceField(
        label="Subcategoría",
        widget=forms.Select(attrs={'class': 'modern-input'})
    )
    
    TIPO_CHOICES = [
        ('', 'Selecciona un tipo'),
        ('texto', 'Texto'),
        ('numero', 'Número'),
        ('boolean', 'Booleano'),
        ('fecha', 'Fecha'),
        ('lista', 'Lista de opciones'),
    ]
    
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        widget=forms.Select(attrs={'class': 'modern-input'})
    )
    
    opciones_text = forms.CharField(
        label="Opciones",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'modern-input',
            'placeholder': 'Opciones separadas por coma (ej: Rojo, Verde, Azul)'
        }),
        help_text='Solo necesario para tipo "Lista de opciones"'
    )
    
    class Meta:
        model = AtributoSubcategoria
        fields = ['subcategoria_id', 'nombre', 'tipo', 'requerido']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'modern-input',
                'placeholder': 'Nombre del atributo'
            }),
            'requerido': forms.CheckboxInput(attrs={
                'class': 'modern-checkbox'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Poblar opciones de categoría
        categorias = Categoria.objects.filter(activo=True)
        choices_categoria = [('', 'Selecciona una categoría')]
        for categoria in categorias:
            choices_categoria.append((str(categoria.id), categoria.nombre))
        self.fields['categoria_id'].choices = choices_categoria
        
        # Poblar opciones de subcategoría (todas inicialmente)
        subcategorias = Subcategoria.objects.filter(activo=True)
        choices_subcategoria = [('', 'Primero selecciona una categoría')]
        for subcategoria in subcategorias:
            choices_subcategoria.append((str(subcategoria.id), subcategoria.nombre))
        self.fields['subcategoria_id'].choices = choices_subcategoria
        
        if self.instance and self.instance.pk:
            self.fields['requerido'].initial = self.instance.requerido
            if self.instance.subcategoria_id:
                self.fields['subcategoria_id'].initial = str(self.instance.subcategoria_id)
                
                # Obtener la categoría de la subcategoría seleccionada
                try:
                    subcategoria = Subcategoria.objects.get(id=self.instance.subcategoria_id)
                    self.fields['categoria_id'].initial = str(subcategoria.categoria_id)
                except Subcategoria.DoesNotExist:
                    pass
                    
            if self.instance.tipo:
                self.fields['tipo'].initial = self.instance.tipo
            if self.instance.opciones:
                if isinstance(self.instance.opciones, list):
                    self.fields['opciones_text'].initial = ', '.join(self.instance.opciones)
                else:
                    self.fields['opciones_text'].initial = self.instance.opciones
        else:
            self.fields['requerido'].initial = False

    def clean_requerido(self):
        requerido = self.cleaned_data.get('requerido')
        if isinstance(requerido, str):
            return requerido.lower() == 'true'
        return bool(requerido)

    def clean_opciones_text(self):
        opciones_text = self.cleaned_data.get('opciones_text', '')
        tipo = self.cleaned_data.get('tipo')
        
        if tipo == 'lista' and not opciones_text.strip():
            raise forms.ValidationError('Las opciones son requeridas para el tipo "Lista de opciones"')
        
        return opciones_text

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Procesar opciones
        opciones_text = self.cleaned_data.get('opciones_text', '')
        if opciones_text.strip():
            opciones_list = [opcion.strip() for opcion in opciones_text.split(',') if opcion.strip()]
            instance.opciones = opciones_list
        else:
            instance.opciones = []
        
        if commit:
            instance.save()
        return instance