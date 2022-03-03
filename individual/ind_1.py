#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import click
from dotenv import load_dotenv


@click.group()
def cli():
    pass


# Создаёт словарь "студент" и записывает его в файл
@cli.command()
@click.argument('file_name')
@click.option("-n", "--name")
@click.option("-g", "--group")
@click.option("-av", "--average_estimation")
def add(file_name, name, group, average_estimation):

    if os.path.exists(file_name):

        # Пакет dotenv
        load_dotenv()
        dotenv_path = os.getenv("STUDENTS_DATA")
        if not dotenv_path:
            click.secho('Такого файла нет', fg='red')
            sys.exit(1)

        if os.path.exists(dotenv_path):
            students = load_students(dotenv_path)
        else:
            students = []

        # Создать словарь.
        student = {
            'name': name,
            'group': group,
            'average_estimation': average_estimation,
        }
        students.append(student)

        with open(dotenv_path, "w", encoding="utf-8") as fout:
            json.dump(students, fout, ensure_ascii=False, indent=3)
    else:
        click.secho("Такого файла не существует")


# Выводит список студентов
@cli.command()
@click.argument("file_name")
def list(file_name):

    if os.path.exists(file_name):

        # Пакет dotenv
        load_dotenv()
        dotenv_path = os.getenv("STUDENTS_DATA")
        if not dotenv_path:
            click.secho('Такого файла нет', fg='red')
            sys.exit(1)

    with open(dotenv_path, "r", encoding="utf-8") as fin:
        staff = json.load(fin)

    if staff:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 8
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
                "No",
                "Ф.И.О.",
                "Группа",
                "Средняя оценка"
            )
        )
        print(line)

        # Вывести данные о всех студентах.
        for idx, student in enumerate(staff, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group', ''),
                    student.get('average_estimation', 0)
                )
            )

        print(line)

    else:
        print("Список пуст")


# Выводит справку о работе с программой
@cli.command()
def help():

    print("Список команд:\n")
    print("add - добавить студента;")
    print("list - вывести список студентов;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")


# Читает данные из файла
def load_students(file_name):
    with open(file_name, "r", encoding="utf-8") as fin:
        file = json.load(fin)
        return file


def main():
    cli()


if __name__ == '__main__':
    main()
