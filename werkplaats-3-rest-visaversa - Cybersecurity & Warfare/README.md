# werkplaats-3-rest-visaversa
werkplaats-3-rest-visaversa created by GitHub Classroom

## Jaad Asnafy (1063009):  
Kalender/rooster van: https://fullcalendar.io/  
Het gebruik en hoe je het in elkaar zet heb ik in de docs bekeken hier: https://fullcalendar.io/docs  
Eventueel errors, foutmeldingen, dingen die ik niet begreep heb ik op de internet gekeken (zoals Stack Overflow) voor de oplossing.

Ajax verversing opgezocht op ChatGPT voor hoe dat moest, bijvoorbeeld:  
setInterval(function() {  
    }, 1000);  
De setInterval functie is de ajax verversing, en de 1000 wilt zeggen elke 1000ms (1 seconde) ververst hij de functie.  
Zo hoef je de pagina niet te verversen om nieuwe data te zien.  

## Stan Verdoorn (1037079):  
static/js/Time.js - 1 t/m 27 - Chatgpt  
Regel 1 - Initialiseren van de functie  
Regel 2 - Roept de functie UpdateTime aan  
Regel 4 t/m 11 - Maakt meerdere variabele aan voor onder andere de huidige tijd, jaar, maand, dag, uren, minuten en seconden en haalt de huidige tijd uit de 'CurrentTime'.  
Regel 13 t/m 17 - Zorgt ervoor dat elke variable juist wordt weergegeven wanneer een maand kleiner is dan 10 wordt hiervoor eerst een 0 aan toegevoegd waardoor je bij cijfers onder de 10 bijvoorbeeld 01 of 02 krijgt.  
Regel 19 t/m 20 - String voor zowel tijd en datum om later te displayen  
Regel 22 t/m 22 - Selecteert het HTML element en haalt de waarde uit timestring en datestring om de juiste tijd en datum weer te geven op de pagina  
Regel 25 - Roept de functie update time aan zodat de tijd op de pagina elke seconde wordt bijgewerkt op de pagina  
Dit is hoe ik mijn Readme heb gemaakt  

## Alex Elwuar (1064050):
Hieronder heb ik code waar ik chatgpt voor gebruikt heb om een voorbeeld van het creeeren van een chart (grafiek) te krijgen. Deze heb ik uiteindelijk aangepast naar onze eigen specifieke doeleinden.    

**templates/hometeacher.html** **regel 42-96**    
```
<h1>Aantal studenten: {{ student_count }}</h1> **student_count is een variabel voor de data die ik heb benoemd in Python flask hier had ik een endpoint aangemaakt om de data van de chart op te kunnen halen**
<div id="chartContainer">    
    <canvas id="myChart"></canvas>                                 **Canvas word gebruikt zodat de chart word weergeven op de html pagina**    
  </div>  

  <script>    
                                **Dit creëert de grafiek**    
    var ctx = document.getElementById('myChart').getContext('2d');  

                                                                        ** HIeronder haalt de data op van de endpoint die ik in python flask heb gemaakt**  
    fetch('/chart-data')  
      .then(response => response.json())  
      .then(data => {  
        ** Dit maakt een array om de labels met aantallen op te slaan**  
        var labelsWithCount = data.labels.map((label, index) => {  
          if (label === 'Teachers') {  
            return label;  
          } else {  
            return label + " (" + data.student_counts[index] + ")";  
          }  
        });  

        var chart = new Chart(ctx, {  
          type: 'bar',  
          data: {  
            labels: labelsWithCount,       **Zodra de data beschikbaar is word er een array gemaakt genaamd "Labelswithcount" **  
    
                   **Hier worden ook de kleuren en de styling bepaald en de type van de diagram bijvoorbeeld een staafdiagram  , Je kan ook zien dat het 2 datasets heeft genaamd students en teachers**  
    
            datasets: [{  
              label: 'Students',  
              data: data.student_counts,  
              backgroundColor: 'rgba(0, 123, 255, 0.5)',      
              borderColor: 'rgba(0, 123, 255, 1)',            
              borderWidth: 1  
            },  
            {  
              label: 'Teachers',  
              data: data.teacher_counts,  
              backgroundColor: 'rgba(255, 255, 255, 0.5)',  
              borderColor: 'rgba(255, 255, 255, 1)',  
              borderWidth: 1  
            }]  
          },  
          options: {  
            scales: {  
              y: {                        **Dit zijn de opties voor de grafiek , zoals het aangeven wanneer de y as begint **  
                beginAtZero: true,  
                precision: 0  
              }  
            }  
          }  
        });  
      });  
  </script>  
  
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>  **Hier importeer ik de bibliotheek jquery**
  <script src="{{ url_for('static', filename='js/time.js') }}"></script>  **Hier importeer ik de bibliotheek Time.js**
  ```
  
Verder heb ik ook wat chatgpt gebruikt om te onderzoeken hoe AJAX precies werkte en wat voorbeeldcode net als Jaad.  

## Quincy Daflaar (1060742):  
chat gpt gebruikt alleen voor informatie, maar meest van de code is zelf geschreven. 
phind was ook gebruikt om een beter begrip te hebben van json ( jsonify) 
Een Modal gemaakt voor het maken van een database met SQLalchemy om met meer javascript te werken. (instance) 

https://i.gyazo.com/6971ee1348fd701b89389c38207973af.png (tabel zoekresultaten)
https://i.gyazo.com/b05a3abdfb3dcdd13e31f5165d540f15.png (user Delete Api using Ajax method, Add Users Approute, user profile modal) 

https://i.gyazo.com/b1f79cb9b8d97fae4c6241805c10c6ed.png (adding persons tabel) 


