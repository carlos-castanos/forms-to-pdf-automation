def combinar_publicador(respuestas, publicadores):

    datos_completos = {}

    for id_publicador in respuestas:

        datos_completos[id_publicador] = {}

        datos_completos[id_publicador].update(
            publicadores[id_publicador]
        )

        datos_completos[id_publicador].update(
            respuestas[id_publicador]
        )

    return datos_completos