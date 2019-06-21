# 2019-NYT-comments
Analysis of the NYT comments in 2017. [José Berrocal, Raúl Cid, Ignacio Machuca. Grupo 5]

# Resumen
El propósito de este proyecto es realizar un análisis de artículos y comentarios del periódico New York Times durante el periodo de enero y mayo del 2017. 

Se busca contestar preguntas como cuáles fueron las keywords (tags) mas comentadas durante cada mes, la evolución de ciertas keywords durante el periodo completo, o que tan popular es Donald Trump. 
Además, se buscó la forma de asignarle un puntaje a cada comentario (sentiment analysis) con el fin de relacionar keywords con la positividad/negatividad de los comentarios.

# Data
El dataset utilizado se descargo del sitio "https://www.kaggle.com/aashita/nyt-comments/", viene separado por mes y por artículo/comentario (por ejemplo: ArticlesApril2017), y el formato utilizado para almacenar los archivos son tablas '.csv'. 


Solo se utilizó la mitad del dataset, correspondiente a los datos de 2017, y que pesa 286 MB comprimido, y 892,7 MB descomprimido. El resto de los datos fueron omitidos para simplificar el análisis y mantener los resultados cohesionados (no tener un salto de 7 meses entre unos datos y otros). Además, este periodo coincide con los primeros meses del mandato de Donald Trump.


Los datos de los artículos son pequeños en comparación a los comentarios, no contiene tantas columnas y tampoco contiene el cuerpo del articulo. De todas las columnas consideraremos los siguientes atributos: (articleID, headline, keywords). En promedio, por mes se tienen entre 800 y 1200 artículos.


Por su parte, los comentarios son bastante más extensos, ya que estos contienen el comentario completo y varios otros atributos de los que usaremos: (commentBody, commentID, articleID). En promedio, por mes se tienen entre 210.000 y 250.000 comentarios.

# Metodología

Para realizar el procesamiento y análisis de los datos de utilizó Spark. Para el tamaño de los datos considerados fue posible realizar la unión de las tablas de artículos y comentarios, realizar el conteo de comentario por artículo y luego realizar el conteo de comentario por cada una de la keywords asociadas a los comentarios.

Para realizar el análisis de opinión, en primer lugar se contruyó un analizador que contaría la cantidad de palabras negativas y positivas en un texto, dado un mapeo de palabras hacia un valoración positiva, negativa o neutral (ver [lexicon](http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/)). La simplicidad de esta herramienta permite realizar un procesamiento rápido pero no entrega buenos resultados, por lo que se decidió utilizar una librería para calcular una valoración para cada comentario. La librería usada fue [nltk](https://www.nltk.org/). Sin embargo, el costo de la mejora en la precisión de la valoración obtenida para cada comentario fue un aumento considerable del tiempo de procesamiento, tanto que no fue posible realizar la valoración de opinión de todos los comentarios del dataset. La opción tomada finalmente fue escoger manualmente artículos de distintas temáticas, que a priori deberían tener una distribución de valoración muy diferente entre ellos, para luego observar experimentalmente si esto es cierto o no.

Cabe destacar en este caso al dificultad de poder suplir a todos los nodos de un sistema distribuido la información y herramientas necesarias para procesar la información, específicamente al momento de disponibilizar la librería utilizada en todos los nodos, y más aún cuando esta librería necesita actualizar desde fuentes externas los diccionarios que utiliza antes de utilizarla por primera vez.

# Resultados
Se calcularon los keywords que más generaban comentarios por año, resultados que estan en <a href= 	"top10_comments.txt">top10_comments.txt</a>, en la Fig. 1 se grafica el ranking del mes de enero.

<div align="center">
<figure>
<img src="graficos/enero.png"
     alt="enero"
     class="center"     
     width="40%"
     height="40%"/>
 

<figcaption><p style="text-align: center;">Fig 1.  top 10 keywords más comentadas de enero</a></p></figcaption>   
</figure>
</div>
 <br />

<div align="center">
 <figure>
<img src="graficos/kw.png"
     alt="keywords evolution"
     class="center"     
     width="40%"
     height="40%"/>
 
<figcaption><p style="text-align: center;">Fig 2.  evolución de keywords entre enero y mayo 2017</a></p></figcaption>   
</figure>
</div>
 <br />

A continuación se muestran distintos histogramas de sentiment score para los comentarios de distintos articulos:

<div align="center">
<figure>
<img src="graficos/putin.png"
     alt="Sentiment Score putin"
     width="40%"
     height="40%"
     class="center"/>
 
<figcaption><p style="text-align: center;">Fig 3. Distribución de puntaje<a href="https://www.nytimes.com/2017/01/06/us/politics/donald-trump-wall-hack-russia.html"> "Putin Led Scheme to Aid Trump, Report Says"</a></p></figcaption>   
</figure>
</div>
<br />
  

<div align="center">
<figure>
<img src="graficos/politics.png"
     alt="Sentiment Score House G.O.P. Abandons Bid to Stifle Ethics Office"
     class="center"     
     width="40%"
     height="40%" />
 
<figcaption><p style="text-align: center;">Fig 4. Distribución de puntaje <a href="https://www.nytimes.com/2017/01/03/us/politics/trump-house-ethics-office.html">"House G.O.P. Abandons Bid to Stifle Ethics Office"</a></p></figcaption> 
</figure>
</div>
<br />


<div align="center">
<figure>
<img src="graficos/travel.png"
     alt="Sentiment Score travel"
     class="center"     
     width="40%"
     height="40%" />
 
<figcaption><p style="text-align: center;">Fig 5. Distribución de puntaje <a href="https://www.nytimes.com/2017/04/01/travel/vancouver-british-columbia-canada-unfolding-story-culture.html">"An Ever-Unfolding Story"  </a></p></figcaption>   
</figure>
</div>
<br />
  

<div align="center">
<figure>
<img src="graficos/husband.png"
     alt="Sentiment Score husband"
     class="center"     
     width="40%"
     height="40%"/>
 
<figcaption><p style="text-align: center;">Fig 6. Distribución de puntaje <a href="https://www.nytimes.com/2017/03/03/style/modern-love-you-may-want-to-marry-my-husband.html">"You May Want to Marry My Husband"  </a></p></figcaption>   
</figure>
</div>
  <br />
  
  
  
# Conclusiones y Aprendizajes


Los resultados obtenidos nos confirman que los artículos que atraen una mayor cantidad de comentarios son aquellos principalmente relacionados con política. Se nota una clara tendencia en las keywords, ya que, en promedio las diez primeras más comentadas para todos los meses analizados tienen que ver con el gobierno de U.S y/o política en general. En cuanto a los comentarios de noticias con estos tópicos, a pesar que el sentiment score promedio es cercano a 0, se puede ver una clara polaridad en las opiniones. Para otro tipo de artículos, como los de estilo de vida, se ve claramente que la valoración de sus comentarios tiende mucho más a ser positiva.

En cuanto a las herramientas utilizadas, notamos que en pyspark se hace más rápido escribir scripts comparado con su contraparte de Java, pero no está del todo preparado para procesar csv, en particular se tuvo problemas con los salto de líneas dentro de los comentarios por lo cual se tuvo que preprocesar esos comentarios.

La aplicación de procesamiento distribuido permitió realizar un análisis sobre los datos y obtener información no trivial de ellos. El uso de herramientas como Spark no sólo permite el que procesamiento sea viable al permitir procesar grandes tablas distribuidamente, sino que también permite que la especificación del tratamiento de los datos se realice en pocas instrucciones y luzca más declarativo. Existieron también problemas al aplicar procesamientos más pesados a los registros de la tablas. Primeramente al intentar utilizar librerías externas dentro de los nodos del cluster y al observar como el tiempo de ejecución crecía explosivamente. Si bien no fue posible realizar el análisis de opinión de forma global para todos los comentarios del dataset, creemos que realizarlo de manera distribuida sí permitió realizarlo rápidamente para artículos específicos, comparado con el procesamiento en un equipo individual.

