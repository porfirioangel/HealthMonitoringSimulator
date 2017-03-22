#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    ----------------------------------------------------------------------------
    Archivo: TimeGenerator.py
    Capitulo: 3 Estilo Publica-Subscribe
    Autor(es): Porfirio Ángel Díaz Sánchez.
    Version: 1 - Marzo 2017
    ----------------------------------------------------------------------------
    Descripción:
    Esta clase no define ningún rol dentro del estilo publica-suscribe,
    pero es utilizada para la generación de datos de tiempo en formato
    humanamente legible
    ----------------------------------------------------------------------------
    Características:
    Interpretador de tiempo
        Responsabilidad
            - Crear objetos datetime a partir de parámetros de día,
            mes, año, hora, etc.
            - Crear representaciones como cadena de texto de un objeto datetime
        Propiedades:
            - Recibe parámetros datetime o numéricos
            - Realiza la creación de objetos datetime o cadena de texto
            - Devuelve los resultados a la entidad que lo solicita
    ----------------------------------------------------------------------------
    Métodos de la clase:
    generar_datetime()
        Parámetros: int: day, int: month, int: year, int: hour, int: second,
        int:microsecond
        Función: Crea un objeto datetime a partir de los parámetros dados,
        si alguno se omite, se tomará el de la fecha actual, por ejemplo,
        el tiempo actual es 22/03/2017 15:49:51, entonces si se manda
        llamar el método de la siguiente manera
        generar_datetime(day=30, year=2000), se devolverá el datetime
        actual con esos parámetros modificados, es decir:
        30/03/2000 15:49:51
    convert_datetime_to_time_string()
        Parámetros: datetime: datetime
        Función: Crea una cadena de texto con la hora establecida en el
        objeto datetime pasado como parámetro
    generate_time_string()
        Parámetros: day, int: month, int: year, int: hour, int: second,
        int:microsecond
        Función: Genera una cadena de texto con la hora a partir de los
        parámetros que recibe el método, tomando los de la fecha actual si
        son omitidos
    ----------------------------------------------------------------------------
'''

from datetime import datetime


class TimeGenerator:
    @staticmethod
    def generar_datetime(day=-1, month=-1, year=-1, hour=-1, minute=-1,
                         second=-1, microsecond=-1):
        today = datetime.today()
        day = today.day if day == -1 else day
        month = today.month if month == -1 else month
        year = today.year if year == -1 else year
        hour = today.hour if hour == -1 else hour
        minute = today.minute if minute == -1 else minute
        second = today.second if second == -1 else second
        microsecond = today.microsecond if microsecond == -1 else microsecond
        modificada = today.replace(day=day, month=month, year=year, hour=hour,
                                   minute=minute, second=second,
                                   microsecond=microsecond)
        return modificada

    @staticmethod
    def convert_datetime_to_time_string(datetime):
        hour = str(datetime.hour) if datetime.hour >= 10 else '0' + str(
            datetime.hour)
        minute = str(datetime.minute) if datetime.minute >= 10 else '0' + str(
            datetime.minute)
        second = str(datetime.second) if datetime.second >= 10 else '0' + str(
            datetime.second)
        fecha_str = hour + ':' + minute + ':' + second
        return fecha_str

    @staticmethod
    def generate_time_string(day=-1, month=-1, year=-1, hour=-1, minute=-1,
                             second=-1, microsecond=-1):
        datetime = TimeGenerator.generar_datetime(day, month, year, hour,
                                                  minute, second, microsecond)
        return TimeGenerator.convert_datetime_to_time_string(datetime)
