# Horarios por sede v4

## Archivos
- `index.html` → app web
- `data.json` → base publicada
- `convert_xlsx_to_json.py` → conversor opcional si querés regenerar `data.json` fuera de la app

## Claves
- Ingreso general: `epavuelve`
- Admin: `epavuelve-admin`

## Cómo funciona el modo admin
1. Entrás a la web.
2. Tocás `Admin`.
3. Ponés la clave admin.
4. Subís un Excel nuevo.
5. La app lo convierte sola y lo guarda en ese navegador.

### Importante
Eso **solo actualiza ese dispositivo/navegador**.

## Cómo hacer que lo vean todos
Después de subir el Excel en modo admin:
1. Tocás `Descargar data.json`
2. Reemplazás `data.json` en GitHub
3. Listo

## Cómo publicar en GitHub Pages
1. Crear repo nuevo
2. Subir `index.html` y `data.json`
3. GitHub → Settings → Pages
4. Source: Deploy from a branch
5. Branch: `main` y carpeta `/ (root)`
6. Guardar

## Agregar a inicio
### iPhone
Safari → Compartir → Agregar a pantalla de inicio

### Android
Chrome → menú → Agregar a pantalla principal
