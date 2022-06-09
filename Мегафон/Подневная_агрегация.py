import pandas as pd
import os

root = os.getcwd()
filename = os.listdir(root)

"""
Мы используем только один сгенерированный датасет "events", 
т.к. для задачи №1 датасеты "Абоненты/Пользователи" и "Тариф"  не нужны.
"""
events = pd.read_csv(os.path.join(root, filename[2]))


def day_agg(df):
    """
    Input: Функция получает на вход датафрейм
    Output: Тот же датафрейм, но с подневной агрегацией,
            а также возвращается длина датафрейма, которую применяем в Unit-тесте
    """
    df['Дата'] = pd.to_datetime(df['Метка_времени']).dt.date

    df = df.pivot_table(index=['id_абонента', 'Дата'],
                        columns='Тип_услуги_звонок_смс_трафик',
                        values='Объем_затраченных_единиц', aggfunc='sum')
    df.columns = ['Потрачено_минут', 'Потрачено_смс', 'Потрачено_трафика']
    df = df.fillna(0)
    return df, len(df)


def test_day_agg(test, answer):
    """
    Для наглядности и удобсвтва проверки будем оценивать по длине
    полученного датафрейма. Т.е. если дана таблица длинной 10 строк
    и в ней столько же уникальных id абонентов, то датафрейм после агрегации
    также будет длиной 10
    """
    agg_test = day_agg(test)[1]
    error_str = 'Test failed!\nInput (length): {0}\nOutput (length): {1}\nCorrect (length) output: {2}'
    assert agg_test == answer, error_str.format(len(test), agg_test, answer)


def run_unit_test():
    """
    В нашем случае для проверки возьмем первые 10 строк
    сгенерированного датафрейма "events". Длина после агрегации также 10.
    Можно наглядно убедиться в этом, вызвав к датафрейму метод ".head(10)"
    """
    test_day_agg(events[:10], 10)
    print('Unit test passed!')


def main():
    run_unit_test()


if __name__ == '__main__':
    main()

print(day_agg(events)[0])
