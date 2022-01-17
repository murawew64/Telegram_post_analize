# Прогнозирование стоимости акций в зависимости от новостной информации

## Стадии проекта

- collect telegram posts - сбор постов с новостями из телеграмма и создание набора новостных данных
- Tinoff api - сбор данных с Московской и Питерской биржи, создание датасета в котором каждому посту соотвествует информация о стоимости акции на момент публикации поста и значению акции через день, неделю, месяц после публикации
- forecast - итоговый этап проекта на котором по полученным данным обучается модель и оценивается ее точность

## collect telegram posts

Берутся только те посты, в которых был обнаружен тикер компании,
если таких тикеров несколько, то пост разбивается на составные части,
таким образом из одного создаются несколько постов с только одним тикером в каждом.

Из постов максимально удаляются лишние символы, убирается все,что точно не несет полезную информацию:
1. убираюся спец символы юникода в виде эмодзи
2. убираются ссылки
3. круглые скобки
4. подвал поста в виде #RDVweekly @AK47pfl
5. квадратные скобки

Обрабатывается ситуация, когда тикеры одинаковые.

**РЕЗУЛЬТАТ**
Получение файла с данными data.csv

## Tinkoff api

Количество запросов ограничено по данному API, поэтому была сделана система,
которая знает на каком моменте остановилось считывание в прошлый раз.

Количество запросов примерно 200 в минуту, при общем количестве записей примерно 6000
нужно 30 мин работы программы. Однако! Чтобы не налететь на штраф по времени программа
ждет минуту после того, как она выполнила лимитное число запросов.

Для каждой компании по тикеру запрашивается ее показатели на 1, 2, 3 и 4 недели

Есть 4 показателя - минимальная цена / максимальная цена, цена открытия / цена закрытия,
Так же делается небольшое редактирование постов.

Для применения Tikoff api нужно всего лишь во времени телеграмм поста заменить пробел на 'T'

Правила обработки:
- Записываются только посты, которые публиковались месяц назад (так как считывается информация на месяц вперед)
- Программа четко отслеживает на каком посте прекратилась обработка.

**РЕЗУЛЬТАТ**
Готовый датасет dataset.csv

## forecast

На данном этапе обрабатываются данные из датасета. 
Каждой записи присваивается дополнительное поле:
1 - если акция выросла
0 - если нет

Далее на данных обучается модель Логистической регрессии.

## Замечание

возможно стоит ввести промежуточный проект, который будет обрабатывать посты
и отсеивать лишнюю информацию или дополнить этим проект **create dataset**

