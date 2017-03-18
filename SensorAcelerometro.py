#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    ----------------------------------------------------------------------------
    Archivo: SensorAcelerometro.py
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
            - Se conecta a la cola 'direct_acelerometer'
            - Envía datos de aceleración al acelerómetro
    ----------------------------------------------------------------------------
    Métodos de la clase:
    __init__()
        Parámetros: String: nombre
        Función: Inicializa los valores de nombre e id
    set_id()
        Parámetros: None
        Función: Genera de manera aleatora el id del usuario
    get_name()
        Parámetros: None
        Función: Devuelve el nombre del usuario al cual fue asignado el sensor
    start_service()
        Parámetros: None
        Función:
            - Realiza la conexión con el servidor de RabbitMQ local.
            - Define a qué cola enviará los mensajes.
            - Define qué tipo de publicación se utilizará.
    simulate_data()
        Parámetros: None
        Función: Genera un número aleatorio entre 0 y 20
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


class SensorAcelerometro:
    nombre = None
    id = 0

    def __init__(self, nombre):
        self.nombre = nombre
        self.id = int(self.set_id())

    def set_id(self):
        return random.randint(1000, 5000)

    def get_name(self):
        return self.nombre

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
        channel.exchange_declare(exchange='direct_acelerometer', type='direct')
        severity = 'aceleracion_movimiento'
        aceleracion_generada = self.simulate_data()
        mensaje = 'AC:' + str(self.id) + ':' + self.nombre + \
                  ':' + json.dumps(aceleracion_generada)
        #   +----------------------------------------------------------------------------+
        #   | La siguiente linea permite enviar datos a la cola seleccionada.            |
        #   +----------------------------------------------------------------------------+
        channel.basic_publish(exchange='direct_acelerometer',
                              routing_key=severity, body=mensaje)
        print(
            '+---------------+--------------------+-------------------------------+-------+')
        print('|      ' + str(
            self.id) + '     |     ' + self.nombre + '     |   ACELERACIÓN '
                                                     'ENVIADA   '
                                                     '|  '
              + str(aceleracion_generada) + '  |')
        print(
            '+---------------+--------------------+-------------------------------+-------+')
        print('')
        connection.close()

    def simulate_data(self):
        return {'x': random.random() * 20, 'y': random.random() * 20,
                'z': random.random() * 20}
