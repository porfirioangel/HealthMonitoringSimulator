#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    ----------------------------------------------------------------------------
    Archivo: SensorAlarmaMedicina.py
    Capitulo: 3 Estilo Publica-Subscribe
    Autor(es): Porfirio Ángel Díaz Sánchez.
    Version: 1 - Marzo 2017
    ----------------------------------------------------------------------------
    Descripción:
    Esta clase define el rol de un publicador que envía mensajes a una cola
    específica.
    ----------------------------------------------------------------------------
    Características:
    Publicador
        Responsabilidad: Enviar mensajes
        Propiedades:
            - Se conecta a la cola 'direct_alarma_medicina'
            - Envía mensajes con la hora actual a la cola
    ----------------------------------------------------------------------------
    Métodos de la clase:
    start_service()
        Parámetros: None
        Función:
            - Realiza la conexión con el servidor de RabbitMQ local.
            - Define a qué cola enviará los mensajes.
            - Define qué tipo de publicación se utilizará.
    simulate_data()
        Parámetros: None
        Función: Genera una hora aleatoria entre 00:00 y 23:59
    ----------------------------------------------------------------------------
    NOTA: "propio de Rabbit" implica que se utilizan de manera interna para
    realizar de manera correcta la recepcion de datos, para éste ejemplo no
    hubo necesidad de utilizarlos y para evitar la sobrecarga de información
    se han omitido sus detalles. Para más información acerca del
    funcionamiento interno de RabbitMQ puedes visitar: https://www.rabbitmq.com/
    ----------------------------------------------------------------------------
'''

import pika
import random
import json

from TimeGenerator import TimeGenerator


class SensorAlarmaMedicina:
    def start_service(self):
        #   +--------------------------------------------------------------------------------------+
        #   | La siguiente linea permite realizar la conexión con el servidor que aloja a RabbitMQ |
        #   +--------------------------------------------------------------------------------------+
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        #   +----------------------------------------------------------------------------------------+
        #   | La siguiente linea permite definir el tipo de intercambio y de que cola recibirá datos |
        #   +----------------------------------------------------------------------------------------+
        channel.exchange_declare(exchange='direct_alarma_medicina',
                                 type='direct')
        severity = 'alarma_hora'
        hora_generada = self.simulate_data()
        mensaje = 'AL:med' + ':' + json.dumps(hora_generada)
        #   +----------------------------------------------------------------------------+
        #   | La siguiente linea permite enviar datos a la cola seleccionada.            |
        #   +----------------------------------------------------------------------------+
        channel.basic_publish(exchange='direct_alarma_medicina',
                              routing_key=severity, body=mensaje)
        print(
            '+---------------+--------------------+-------------------------------+-------+')
        print('|      HORA ENVIADA   |  ' + str(hora_generada) + '  |')
        print(
            '+---------------+--------------------+-------------------------------+-------+')
        print('')
        connection.close()

    def simulate_data(self):
        random_hour = random.randint(int(0), int(23))
        return TimeGenerator.generate_time_string(hour=random_hour, minute=0,
                                                  second=0, microsecond=0)
