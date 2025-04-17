def procesar(segmentos, reqs, marcos_libres):
    PAGE_SIZE = 0x10
    
    tabla_paginas = {}
    fifo = []
    
    resultados = []
    
    for req in reqs:
        segmento_encontrado = None
        for (nombre, base, limite) in segmentos:
            if req >= base and req < base + limite:
                segmento_encontrado = (nombre, base, limite)
                break

        if segmento_encontrado is None:
            resultados.append((f"Req: {hex(req)}", f"Direccion Fisica: {hex(0x1ff)}", "Acción: Segmentation Fault"))
            break  
        
        nombre_seg, base_seg, _ = segmento_encontrado
        offset_total = req - base_seg
        num_page = offset_total // PAGE_SIZE
        offset = offset_total % PAGE_SIZE

        clave = (nombre_seg, num_page)
        
        if clave in tabla_paginas:
            marco = tabla_paginas[clave]
            accion = "Marco ya estaba asigando"
        else:
            if marcos_libres:
                marco = marcos_libres.pop()
                accion = "Marco libre asignado"
            else:
                victim_key = fifo.pop(0)
                marco = tabla_paginas[victim_key]
                del tabla_paginas[victim_key]
                accion = "Marco asignado"
            tabla_paginas[clave] = marco
            fifo.append(clave)
       
        direccion_fisica = marco * PAGE_SIZE + offset
        
        resultados.append((f"Req: {hex(req)}", f"Direccion Fisica: {hex(direccion_fisica)}", f"Acción: {accion}"))
    
    return resultados


if __name__ == "__main__":
    marcos_libres = [0x0, 0x1, 0x2]
    reqs = [0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A]
    segmentos = [
        ('.text', 0x00, 0x1A),
        ('.data', 0x40, 0x28),
        ('.heap', 0x80, 0x1F),
        ('.stack', 0xC0, 0x22),
    ]
    
    res = procesar(segmentos, reqs, marcos_libres)
    for r in res:
        print(r[0], r[1], r[2])
