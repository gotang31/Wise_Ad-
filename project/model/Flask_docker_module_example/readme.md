# How to Test
python main.py<br>

**result:**
```bash
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://10.64.157.30:5000
Press CTRL+C to quit
```

in Windows :(in case using other os, use curl)<br>
open powershell

```bash
$params = @{"param1"="5"; "param2"="11";}
Invoke-WebRequest -Uri http://127.0.0.1:5000/add_multiply -Method POST -Body ($params|ConvertTo-Json) -ContentType "application/json"
```

**result:**
```bash
StatusCode        : 200
StatusDescription : OK
Content           : [16,55]

RawContent        : HTTP/1.1 200 OK
                    Connection: close
                    Content-Length: 8
                    Content-Type: application/json
                    Date: Thu, 14 Dec 2023 09:45:25 GMT
                    Server: Werkzeug/3.0.1 Python/3.11.6

                    [16,55]

Forms             : {}
Headers           : {[Connection, close], [Content-Length, 8], [Content-Type, application/json], [Date, Thu, 14 Dec 202
                    3 09:45:25 GMT]...}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 8
```