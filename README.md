# An-lisis-De-Algoritmos-Python
Programas en Python para análisis de algoritmos mediante gráficas, módulos de análisis de complejidad temporal y de manera gráfica.


Crear ejecutable:

Opcion 1:
pyinstaller AnalisisAlgoritmos.spec

Opcion 2:
pyinstaller --onefile ^
    --windowed ^
    --name="AnalisisDeAlgoritmos" ^
    --add-data "AnalisisDeAlgoritmos;AnalisisDeAlgoritmos" ^
    --add-data "AnalisisDeAdO;AnalisisDeAdO" ^
    --hidden-import="matplotlib.backends.backend_tkagg" ^
    --hidden-import="numpy" ^
    main.py
