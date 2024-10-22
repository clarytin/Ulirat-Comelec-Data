# Comelec Web Scraper

This is a program that scrapes the **2022 Philippine Election** data from the [Comelec website](https://2022electionresults.comelec.gov.ph/#/coc/0)  at the Municipality level. It's formatted in one Excel file for each Province, and one worksheet for each municipality.

The scraped data is in the `/data` folder. Some of the files might be in `.numbers` instead of `.xlsx` because I accidentally saved them while verifying the contents.

To run the code, you'll have to download Google Chrome and the [webdriver](https://developer.chrome.com/docs/chromedriver/downloads) for your version of the browser.

Plug your path in the line `cService = webdriver.ChromeService(executable_path='your path here')` and then the Comelec website after `driver.get()`


**Some districts won't work out of the box.** These ones don't vote for a Provincial Governer, Vice-Governor, or Sangguniang Panlalawigan. Or they have extra Members of the House of Representatives. Or they're just special (looking at you, NCR - First District). 

One day, I'd like fix the code to handle these, but for now, you'll have to manually add the extra positions and run the program for the individual districts. This should cover the special cases, plus a few extras that failed on my first go:

    BARMM - Lanao Del Sur, Maguindanao
    CAR- Mountain Province, Benguet
    NCR - All of them
    Region I - Pangasinan
    Region II - Isabela
    Region III - Nueva Ecija, Pampanga, Zambales
    Region IV-A - Cavite, Quezon
    Region IV-B - Palawan
    Region V - Camarines Sur
    Region VI - Iloilo, Negros Occidental
    Region VII - Cebu
    Region VIII - Biliran, Leyte, Southern Leyte
    Region IX - Zamboanga del Sur, Zamboanga Sibugay
    Region X - Bukidnon, Lanao del Norte, Misamis Oriental
    Region XI - Davao del Sur
    Region XII - Sarangani, South Cotabato
    Region XIII - Agusan del Norte

