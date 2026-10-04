# Datos de entrada

El experimento requiere los dos cortes C095 / 1-250.dcm de
LDCT-and-Projection-Data (TCIA), ya reconstruidos:

- `data/sdct/1-250.dcm`: Full Dose Images.
- `data/ldct/1-250.dcm`: Low Dose Images.

Estos archivos se incluyen en el paquete local para reproducir el experimento,
pero `.gitignore` evita incorporarlos mediante `git add .` al repositorio nuevo.
Quien clone GitHub debe proporcionar estos dos DICOM, respetando las condiciones
de acceso del dataset, o ajustar sus rutas en `config/default.json`.

Las rutas del JSON son relativas a `config/`, independientemente de la terminal.
No sustituir los cortes si se quieren contrastar las cifras del informe.

SHA-256 de las entradas utilizadas:

| Entrada | SHA-256 |
|---|---|
| SDCT | `86196a8ae87a0860c327542c47dfe756781f3b9346438c0a364e1fa54fa34013` |
| LDCT | `0463186a016e9bddfd86617d56a435ae4fbb1655b8af9ccfea9b371db0259779` |
