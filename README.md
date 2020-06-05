# British Passport Abroad Dates Validator

This script helps with an application fo British Pasport / Citizenship.
This script helps with an application fo British Pasport / Citizenship.
There are several requirements for you if willing to apply.
In terms of your history of stay in the UK you must be:
  *   not more than **450 days** in total outside of the UK in **last 5 years**
  *   not more than **3 months** (~90 days) in total outside of the UK in **last 12 months**
  *   not more than **6 months** (~180 days) in total  outside of the UK in **ANY 12-month period within last 5 years**

This script calculates that for you. 

It needs both:
* a date of submitting your British Passport application, `DateApply` (line ~100 in the main script file) or run the script with the extra date argument in format `DDMMYY`, eg:
    <pre>$ python3 BPDateValidator.py <b>101220</b></pre>
* a CSV file (it should be in the same folder as the script) with a list  of your flights in format :

<pre><b>DepartDateTime</b>, DepartPlace, <b>IsUK</b>, ArrivePlace, <b>IsUK</b>, Airline, FlNumber, <b>WasCancelled</b></pre>

  where:
  
 * ***DepartDateTime*** => *using* `DD/MM/YY HH:MM` *or* `DD/MM/YY` *or* `DD/MM/YYYY` *format*

 * ***IsUK***, ***IsUK***, ***WasCancelled*** => *using* `"True"` *or* `"TRUE"` *or* `1` *for* `True`, *else* `False`

 * ***DepartPlace***, ***ArrivePlace***, ***Airline***, ***FlNumber*** => ***not critical** and will **NOT** change the result of the algorith, however, it can be usefull as it an additional information*

 example csv file, `example.csv`:
  
    17/05/10 10:40, LIS, FALSE, EDI, TRUE, RyanAir, FR1111, FALSE
    27/07/10 13:10, EDI, TRUE, GDN, FALSE, RyanAir, FR2222, FALSE
    02/05/11 10:50, WMI, FALSE, PIK, TRUE, RyanAir, FR3333, FALSE
    30/07/13 12:20, EDI, TRUE, LPA, FALSE, RyanAir, FR4444, FALSE
    07/08/13 10:10, LPA, FALSE, GLA, TRUE, WizzAir, FR5555, FALSE
