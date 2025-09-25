# 🔴 Prueba tecnica SETI

Repositorio con la API planteada en la prueba tecnica Desarrollador Backend (Python).

> 🔩 Desarrollado con **Python 3.10** | **FastAPI** | **SQLite**.

## ▶️ Como ejecutarlo

Para ejecutar el proyecto, siga estos pasos:

1. Clone este repositorio en su maquina local.

```bash
git clone https://github.com/cristian1clj/prueba-tecnica-seti.git
```

2. Navegue al directorio del proyecto.

```bash
cd prueba-tecnica-seti
```

3. [RECOMENDADO] Cree un nuevo ambiente virtual y activelo.

```bash
python -m venv .venv
source .venv/bin/activate
```

4. Instale las dependencias.

```bash
pip install -r requirements.txt
```

5. Ejecute el proyecto.

```bash
uvicorn app.main:app --reload
```

6. Ahora podra acceder a la API a travez de ***localhost:8000*** o ***127.0.0.1:8000***. (la informacion de los endpoints se encuantra a continuacion)

## 📃 Documentacion(endpoints)

<table>
  <tr>
    <th>TAGS</th>
    <th>METODOS</th>
    <th>ENDPOINTS</th>
    <th>DESCRIPCION</th>
  </tr>
  <tr>
    <td rowspan="2">Messages</td>
    <td style="background-color: #61affe; color: white">GET</td>
    <td>/api/messages/{session_id}?limit={int}&offset={int}&sender={str}</td>
    <td>Obtiene todos los mensajes de acuerdo con la sesion especificada y los filtros adicionales</td>
  </tr>
  <tr>
    <td style="background-color: #49cc90; color: white">POST</td>
    <td>/api/messages</td>
    <td>Crear nuevo mensaje</td>
  </tr>
  <tr>
    <td rowspan="1">Documentacion</td>
    <td style="background-color: #61affe; color: white"></td>
    <td>/docs</td>
    <td>Accede a la documentacion generada por Swagger UI</td>
  </tr>
</table>