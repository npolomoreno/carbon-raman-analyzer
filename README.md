# carbon-raman-analyzer

**Raman Analysis App**: aplicación de escritorio para el análisis por lotes de espectros Raman de materiales de carbono (grafeno, grafito y afines). Detecta las bandas D, G y 2D, calcula las razones de intensidad y el tamaño de cristalito, y muestra los resultados en una tabla con promedio y desviación estándar.

Desarrollada por **Natalia Polo-Moreno** (2024–2025) 

## Qué hace

- Carga varios espectros a la vez en formato `.csv` o `.txt` (dos columnas: desplazamiento Raman en cm⁻¹ e intensidad).
- Busca el máximo de cada banda en su ventana: D (1300–1400 cm⁻¹), G (1500–1600 cm⁻¹) y 2D (2600–2800 cm⁻¹).
- Reporta la intensidad y la posición de cada banda, las razones ID/IG e I2D/IG, y el tamaño de cristalito La según Cançado et al. (2006) para un láser de 532 nm.
- Calcula el promedio y la desviación estándar de todos los archivos cargados.
- Grafica cada espectro con las bandas detectadas marcadas.

## Uso

Con el ejecutable para Windows (sección *Releases*): abrirlo, pulsar **Select files**, elegir los espectros y pulsar **Generar análisis**.

Desde el código (Python 3.10 o superior):

```
pip install -r requirements.txt
python App_RAMAN_npolo.py
```

Para generar el ejecutable: `pip install pyinstaller` y luego `pyinstaller App_RAMAN_npolo.spec`.

## Limitaciones conocidas

- No resta línea base: un fondo de fluorescencia altera las intensidades y las razones.
- Usa la altura del máximo, sin ajuste de curvas; no reporta anchos (FWHM) ni áreas.
- Si en una ventana no hay banda real, reporta el máximo local del ruido.
- La longitud de onda del láser está fija en 532 nm.
- La fórmula de La es válida para grafito nanocristalino, no para defectos puntuales en grafeno.
- La primera fila del archivo se lee como encabezado.

## Cómo citar

Si usas esta aplicación en un curso, una publicación o un trabajo académico, cítala como se indica en `CITATION.cff` (en GitHub, botón *Cite this repository*).

## Licencia

PolyForm Noncommercial License 1.0.0 (ver `LICENSE.md`). Se permite el uso con fines no comerciales, incluidos la docencia y la investigación en instituciones educativas y públicas. Para cualquier uso comercial, contactar a la autora.

## Referencia

Cançado, L. G., Takai, K., Enoki, T., Endo, M., Kim, Y. A., Mizusaki, H., Jorio, A., Coelho, L. N., Magalhães-Paniago, R., & Pimenta, M. A. (2006). General equation for the determination of the crystallite size La of nanographite by Raman spectroscopy. *Applied Physics Letters*, 88, 163106. https://doi.org/10.1063/1.2196057
