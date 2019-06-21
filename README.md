# 2019-NYT-comments
Analysis of the NYT comments in 2017. [José Berrocal, Raúl Cid, Ignacio Machuca. Grupo 5]

# Resumen
El propósito de este proyecto es realizar un análisis de artículos y comentarios del periódico New York Times durante el periodo de enero y mayo del 2017. 
Se busca contestar preguntas como cuáles fueron las keywords (tags) mas comentadas durante cada mes, la evolución de ciertas keywords durante el periodo completo, o que tan popular es Donald Trump. 
Además, se buscó la forma de asignarle un puntaje a cada comentario (sentiment analysis) con el fin de relacionar keywords con la positividad/negatividad de los comentarios.

# Data
El dataset utilizado se descargo del sitio "https://www.kaggle.com/aashita/nyt-comments/", viene separado por mes y por artículo/comentario (por ejemplo: ArticlesApril2017), y el formato utilizado para almacenar los archivos son tablas '.csv'. 
Solo se utilizó la mitad del dataset, correspondiente a los datos de 2017, y que pesa 286 MB comprimido, y 892,7 MB descomprimido. El resto de los datos fueron omitidos para simplificar el análisis y mantener los resultados cohesionados (no tener un salto de 7 meses entre unos datos y otros). Además, este periodo coincide con los primeros meses del mandato de Donald Trump.
Los datos de los artículos son pequeños en comparación a los coentarios, no contiene tantas columnas y tampoco contiene el cuerpo del articulo. De todas las columnas consideraremos los siguientes atributos: (articleID, headline, keywords). En promedio, por mes se tienen entre 800 y 1200 artículos.
Por su parte, los comentarios son bastante más extensos, ya que estos contienen el comentario completo y varios otros atributos de los que usaremos: (commentBody, commentID, articleID). En promedio, por mes se tienen entre 210.000 y 250.000 comentarios.

# Metodología

