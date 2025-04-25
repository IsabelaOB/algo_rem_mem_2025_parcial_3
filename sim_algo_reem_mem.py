from collections import deque

def procesar(segmentos, reqs, marcos_libres):
    tabla_paginas = {}  
    cola_fifo = deque() 
    resultados = []

    def buscar_segmento(dir_virtual):
        for nombre, base, limite in segmentos:
            if base <= dir_virtual < base + limite:
                return nombre, base
        return None, None  

    for req in reqs:
        segmento, base = buscar_segmento(req)
        if segmento is None:
            resultados.append((req, 0x1FF, "Segmentation Fault"))
            break  

       
        pagina_virtual = req >> 4
        offset = req & 0xF

        if pagina_virtual in tabla_paginas:
            marco = tabla_paginas[pagina_virtual]
            direccion_fisica = (marco << 4) | offset
            resultados.append((req, direccion_fisica, "Marco ya estaba asignado"))
        else:
            if marcos_libres:
                marco = marcos_libres.pop(0)
                tabla_paginas[pagina_virtual] = marco
                cola_fifo.append(pagina_virtual)
                direccion_fisica = (marco << 4) | offset
                resultados.append((req, direccion_fisica, "Marco libre asignado"))
            else:
                pagina_vieja = cola_fifo.popleft()  
                marco = tabla_paginas.pop(pagina_vieja)
                tabla_paginas[pagina_virtual] = marco
                cola_fifo.append(pagina_virtual)
                direccion_fisica = (marco << 4) | offset
                resultados.append((req, direccion_fisica, "Marco asignado"))

    return resultados

marcos_libres = [0x0, 0x1, 0x2]
reqs = [0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A]
segmentos = [
    ('.text', 0x00, 0x1A),
    ('.data', 0x40, 0x28),
    ('.heap', 0x80, 0x1F),
    ('.stack', 0xC0, 0x22),
]

resultados = procesar(segmentos, reqs, marcos_libres)

for req, dir_fis, accion in resultados:
    print(f"Req: {hex(req)} Direccion Fisica: {hex(dir_fis)} Acción: {accion}")
