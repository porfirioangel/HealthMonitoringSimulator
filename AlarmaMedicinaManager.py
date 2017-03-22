#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    ----------------------------------------------------------------------------
    Archivo: AlarmaMedicinaManager.py
    Capitulo: 3 Estilo Publica-Subscribe
    Autor(es): Porfirio Ángel Díaz Sánchez.
    Version: 1 - Marzo 2017
    ----------------------------------------------------------------------------
    Descripción:
    Esta clase define el rol de un suscriptor que consume los mensajes de una
    cola específica.
    ----------------------------------------------------------------------------
    Características:
    Suscriptor
        Responsabilidad:
            - Recibir mensajes
            - Notificar al monitor
            - Filtrar valores extremos de aceleración
        Propiedades:
            - Se suscribe a la cola 'direct_acelerometer'
            - Define un rango en la que la aceleración tiene valores válidos
            - Notifica al monitor un segundo después de recibir el mensaje
    ----------------------------------------------------------------------------
    Métodos de la clase:
    setUpManager()
        Parámetros: int: max
        Función: Establece el valor máximo permitido de la temperatura
    start_consuming()
        Parámetros: None
        Función:
            - Lee los argumentos con los que se ejecuta el programa para
            establecer el valor máximo que puede tomar la temperatura
            - Realiza la conexión con el servidor de RabbitMQ loca
            - Declara el tipo de intercambio y a qué cola se va a suscribir
            - Comienza a esperar los eventos
    callback()
        Parámetros:
            ch: propio de RabbitMQ
            method: propio de RabbitMQ
            properties: propio de RabbitMQ
            string: body
        Función:
            - Contiene la lógica de negocio
            - Se manda llamar cuando un evento ocurre
    ----------------------------------------------------------------------------
    NOTA: "propio de Rabbit" implica que se utilizan de manera interna para
    realizar de manera correcta la recepcion de datos, para éste ejemplo no
    hubo necesidad de utilizarlos y para evitar la sobrecarga de información
    se han omitido sus detalles. Para más información acerca del
    funcionamiento interno de RabbitMQ puedes visitar: https://www.rabbitmq.com/
    ----------------------------------------------------------------------------
'''

import pika
import sys
import json


class AlarmaMedicinaManager:
    horas_medicina = {}
    status = ""
    values_parameters = 0

    def setUpManager(self, horas_medicina):
        self.horas_medicina = horas_medicina

    def start_consuming(self):
        self.horas_medicina = json.loads(raw_input())
        # self.setUpManager(self.values_parameters)
        #   +--------------------------------------------------------------------------------------+
        #   | La siguiente linea permite realizar la conexión con el servidor que aloja a RabbitMQ |
        #   +--------------------------------------------------------------------------------------+
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        channel = connection.channel()
        #   +----------------------------------------------------------------------------------------+
        #   | La siguiente linea permite definir el tipo de intercambio y de que cola recibirá datos |
        #   +----------------------------------------------------------------------------------------+
        channel.exchange_declare(exchange='direct_alarma_medicina',
                                 type='direct')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        severity = 'alarma_hora'
        #   +----------------------------------------------------------------------------+
        #   | La siguiente linea permite realizar la conexión con la cola que se definio |
        #   +----------------------------------------------------------------------------+
        channel.queue_bind(exchange='direct_alarma_medicina',
                           queue=queue_name, routing_key=severity)
        print(
            ' [*] Inicio de monitoreo alarmas para tomar medicina. Presiona '
            'CTRL+C para finalizar el monitoreo')
        #   +----------------------------------------------------------------------------------------+
        #   | La siguiente linea permite definir las acciones que se realizarán al ocurrir un método |
        #   +----------------------------------------------------------------------------------------+
        channel.basic_consume(self.callback,
                              queue=queue_name,
                              no_ack=True)
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        separators = self.get_substring_indexes(body, '"')
        hora_key = body[separators[0] + 1:separators[1]]
        print 'Hora: ' + hora_key
        if hora_key in self.horas_medicina:
            print '    Es momento de: ' + self.horas_medicina[hora_key]
        else:
            print '    No hay medicinas programadas'

    def get_substring_indexes(self, string, substring):
        return [i for i in range(len(string)) if string.startswith(
            substring, i)]


test = AlarmaMedicinaManager()
test.start_consuming()
